#!/usr/bin/env python3
"""
Load Testing Script for Orçamento Endpoint
Performs concurrent requests to test the performance of the orçamento (budget) generation endpoint.
"""
import asyncio
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import os
import sys
from dataclasses import dataclass, asdict
from statistics import mean, median, stdev

import httpx
import click


@dataclass
class LoadTestConfig:
    """Configuration for load testing."""
    base_url: str = "http://localhost:8000"
    username: str = "admin@test.com"  # Use email as username
    password: str = "senha123"
    total_requests: int = 100
    concurrent_users: int = 10
    request_delay: float = 0.1  # seconds between requests per user
    timeout: float = 30.0
    ordem_servico_ids: Optional[List[str]] = None


@dataclass
class RequestResult:
    """Result of a single request."""
    success: bool
    status_code: int
    response_time: float
    error: Optional[str] = None
    response_data: Optional[Dict] = None


@dataclass
class LoadTestResults:
    """Aggregated results of load testing."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_time: float
    avg_response_time: float
    median_response_time: float
    min_response_time: float
    max_response_time: float
    response_time_stddev: float
    requests_per_second: float
    status_codes: Dict[int, int]
    errors: Dict[str, int]


class LoadTester:
    """Main load testing class."""
    
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.session_token: Optional[str] = None
        self.results: List[RequestResult] = []
        
    async def authenticate(self) -> bool:
        """Authenticate and get access token."""
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            try:
                response = await client.post(
                    f"{self.config.base_url}/auth/token",
                    data={
                        "username": self.config.username,
                        "password": self.config.password
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.session_token = token_data.get("access_token")
                    print(f"✅ Authentication successful for user: {self.config.username}")
                    return True
                else:
                    print(f"❌ Authentication failed: {response.status_code} - {response.text}")
                    return False
                    
            except Exception as e:
                print(f"❌ Authentication error: {str(e)}")
                return False

    async def get_available_ordens_servico(self) -> List[str]:
        """Get available ordem_servico IDs for testing."""
        headers = {"Authorization": f"Bearer {self.session_token}"}
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            try:
                response = await client.get(
                    f"{self.config.base_url}/ordens-servico/",
                    headers=headers
                )
                
                if response.status_code == 200:
                    ordens = response.json()
                    if ordens:
                        ids = [os.get("id") for os in ordens if os.get("id")]
                        print(f"📋 Found {len(ids)} available ordem_servico IDs")
                        return ids[:10]  # Limit to first 10 for testing
                    else:
                        print("⚠️  No ordem_servico found, will use dummy IDs")
                        return ["test-os-1", "test-os-2", "test-os-3"]
                else:
                    print(f"⚠️  Could not fetch ordens_servico: {response.status_code}")
                    return ["test-os-1", "test-os-2", "test-os-3"]
                    
            except Exception as e:
                print(f"⚠️  Error fetching ordens_servico: {str(e)}")
                return ["test-os-1", "test-os-2", "test-os-3"]

    async def make_orcamento_request(self, ordem_servico_id: str) -> RequestResult:
        """Make a single orçamento request."""
        headers = {"Authorization": f"Bearer {self.session_token}"}
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            try:
                response = await client.get(
                    f"{self.config.base_url}/ordens-servico/{ordem_servico_id}/orcamento",
                    headers=headers
                )
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    return RequestResult(
                        success=True,
                        status_code=response.status_code,
                        response_time=response_time,
                        response_data=response.json()
                    )
                else:
                    return RequestResult(
                        success=False,
                        status_code=response.status_code,
                        response_time=response_time,
                        error=f"HTTP {response.status_code}: {response.text[:200]}"
                    )
                    
            except httpx.TimeoutException:
                response_time = time.time() - start_time
                return RequestResult(
                    success=False,
                    status_code=0,
                    response_time=response_time,
                    error="Request timeout"
                )
            except Exception as e:
                response_time = time.time() - start_time
                return RequestResult(
                    success=False,
                    status_code=0,
                    response_time=response_time,
                    error=str(e)
                )

    async def worker(self, worker_id: int, ordem_servico_ids: List[str], requests_per_worker: int):
        """Worker coroutine that makes requests."""
        print(f"🔄 Worker {worker_id} starting with {requests_per_worker} requests")
        
        for i in range(requests_per_worker):
            # Round-robin through available ordem_servico IDs
            os_id = ordem_servico_ids[i % len(ordem_servico_ids)]
            
            result = await self.make_orcamento_request(os_id)
            self.results.append(result)
            
            # Print progress for every 10 requests
            if (i + 1) % 10 == 0:
                print(f"Worker {worker_id}: {i + 1}/{requests_per_worker} requests completed")
            
            # Add delay between requests
            if self.config.request_delay > 0:
                await asyncio.sleep(self.config.request_delay)

    async def run_load_test(self) -> LoadTestResults:
        """Run the complete load test."""
        print("🚀 Starting load test...")
        print(f"Target URL: {self.config.base_url}")
        print(f"Total requests: {self.config.total_requests}")
        print(f"Concurrent users: {self.config.concurrent_users}")
        print(f"Request delay: {self.config.request_delay}s")
        
        # Authenticate
        if not await self.authenticate():
            raise Exception("Authentication failed")
        
        # Get available ordem_servico IDs
        if self.config.ordem_servico_ids:
            ordem_servico_ids = self.config.ordem_servico_ids
        else:
            ordem_servico_ids = await self.get_available_ordens_servico()
            
        if not ordem_servico_ids:
            raise Exception("No ordem_servico IDs available for testing")
        
        print(f"🎯 Using ordem_servico IDs: {ordem_servico_ids}")
        
        # Calculate requests per worker
        requests_per_worker = self.config.total_requests // self.config.concurrent_users
        
        # Start the load test
        start_time = time.time()
        
        # Create worker tasks
        tasks = []
        for worker_id in range(self.config.concurrent_users):
            task = asyncio.create_task(
                self.worker(worker_id + 1, ordem_servico_ids, requests_per_worker)
            )
            tasks.append(task)
        
        # Wait for all workers to complete
        await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        print(f"✅ Load test completed in {total_time:.2f}s")
        
        return self._analyze_results(total_time)

    def _analyze_results(self, total_time: float) -> LoadTestResults:
        """Analyze the test results."""
        successful_results = [r for r in self.results if r.success]
        failed_results = [r for r in self.results if not r.success]
        
        # Response times
        response_times = [r.response_time for r in self.results]
        
        # Status codes
        status_codes = {}
        for result in self.results:
            status_codes[result.status_code] = status_codes.get(result.status_code, 0) + 1
        
        # Errors
        errors = {}
        for result in failed_results:
            if result.error:
                errors[result.error] = errors.get(result.error, 0) + 1
        
        return LoadTestResults(
            total_requests=len(self.results),
            successful_requests=len(successful_results),
            failed_requests=len(failed_results),
            total_time=total_time,
            avg_response_time=mean(response_times) if response_times else 0,
            median_response_time=median(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            response_time_stddev=stdev(response_times) if len(response_times) > 1 else 0,
            requests_per_second=len(self.results) / total_time if total_time > 0 else 0,
            status_codes=status_codes,
            errors=errors
        )

    def print_results(self, results: LoadTestResults):
        """Print formatted test results."""
        print("\n" + "="*60)
        print("📊 LOAD TEST RESULTS")
        print("="*60)
        
        print(f"Total Requests:        {results.total_requests}")
        print(f"Successful Requests:   {results.successful_requests}")
        print(f"Failed Requests:       {results.failed_requests}")
        print(f"Success Rate:          {(results.successful_requests/results.total_requests)*100:.2f}%")
        print(f"Total Time:            {results.total_time:.2f}s")
        print(f"Requests per Second:   {results.requests_per_second:.2f}")
        
        print("\n📈 RESPONSE TIMES")
        print("-"*40)
        print(f"Average:    {results.avg_response_time*1000:.2f}ms")
        print(f"Median:     {results.median_response_time*1000:.2f}ms")
        print(f"Min:        {results.min_response_time*1000:.2f}ms")
        print(f"Max:        {results.max_response_time*1000:.2f}ms")
        print(f"Std Dev:    {results.response_time_stddev*1000:.2f}ms")
        
        print("\n📋 STATUS CODES")
        print("-"*40)
        for status_code, count in sorted(results.status_codes.items()):
            print(f"HTTP {status_code}:     {count}")
        
        if results.errors:
            print("\n❌ ERRORS")
            print("-"*40)
            for error, count in results.errors.items():
                print(f"{error}: {count}")
        
        print("\n" + "="*60)

    def save_results_json(self, results: LoadTestResults, filename: Optional[str] = None):
        """Save results to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"load_test_results_{timestamp}.json"
        
        # Convert results to dict for JSON serialization
        results_dict = asdict(results)
        results_dict['timestamp'] = datetime.now().isoformat()
        results_dict['config'] = asdict(self.config)
        
        with open(filename, 'w') as f:
            json.dump(results_dict, f, indent=2, default=str)
        
        print(f"💾 Results saved to: {filename}")


@click.command()
@click.option('--url', default="http://localhost:8000", help='Base URL of the API')
@click.option('--username', default="admin@test.com", help='Username (email) for authentication')
@click.option('--password', default="senha123", help='Password for authentication')
@click.option('--requests', '-r', default=100, help='Total number of requests')
@click.option('--concurrent', '-c', default=10, help='Number of concurrent users')
@click.option('--delay', '-d', default=0.1, help='Delay between requests per user (seconds)')
@click.option('--timeout', '-t', default=30.0, help='Request timeout (seconds)')
@click.option('--output', '-o', help='Output file for results (JSON)')
@click.option('--os-ids', help='Comma-separated list of ordem_servico IDs to test')
def main(url, username, password, requests, concurrent, delay, timeout, output, os_ids):
    """
    Load Testing Script for Tech Challenge Orçamento Endpoint
    
    This script performs concurrent load testing against the orçamento generation endpoint.
    It authenticates with the API, fetches available ordem_servico IDs, and then performs
    multiple concurrent requests to measure performance.
    
    Example usage:
    
    \b
    # Basic load test
    python load_test_orcamento.py
    
    \b
    # Custom configuration
    python load_test_orcamento.py --requests 200 --concurrent 20 --delay 0.05
    
    \b
    # Test against specific ordem_servico IDs
    python load_test_orcamento.py --os-ids "os1,os2,os3"
    
    \b
    # Save results to file
    python load_test_orcamento.py --output results.json
    """
    try:
        # Parse ordem_servico IDs if provided
        ordem_servico_ids = None
        if os_ids:
            ordem_servico_ids = [id.strip() for id in os_ids.split(',')]
        
        # Create configuration
        config = LoadTestConfig(
            base_url=url,
            username=username,
            password=password,
            total_requests=requests,
            concurrent_users=concurrent,
            request_delay=delay,
            timeout=timeout,
            ordem_servico_ids=ordem_servico_ids
        )
        
        # Run load test
        tester = LoadTester(config)
        results = asyncio.run(tester.run_load_test())
        
        # Print results
        tester.print_results(results)
        
        # Save results if output file specified
        if output:
            tester.save_results_json(results, output)
        
        # Exit with error code if too many failures
        if results.failed_requests / results.total_requests > 0.1:  # >10% failure rate
            print("\n⚠️  Warning: High failure rate detected!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Load test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Load test failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
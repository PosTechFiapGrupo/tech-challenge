import re

def validate_vehicle_plate(plate: str) -> bool:
    """
    Validate Brazilian vehicle plate formats:
    - Old format: ABC-1234
    - Mercosul format: ABC1D23
    """
    plate = plate.upper().strip()

    old_format_pattern = r'^[A-Z]{3}-\d{4}$'
    mercosur_format_pattern = r'^[A-Z]{3}\d[A-Z]\d{2}$'

    if re.match(old_format_pattern, plate):
        return True
    if re.match(mercosur_format_pattern, plate):
        return True
    return False

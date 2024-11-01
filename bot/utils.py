from typing import Dict, List


def validate_incoming_data(
    data: Dict[str, any], required_keys: List[str], allowed_keys: List[str] = []
) -> List[Dict[str, str]]:
    """
    Validate the given data against the required and allowed keys.

    Args:
        data (Dict[str, any]): The data to validate.
        required_keys (List[str]): The required keys.
        allowed_keys (List[str], optional): The allowed keys. Defaults to [].

    Returns:
        List[Dict[str, str]]: A list of errors.
    """

    errors: List[Dict[str, str]] = []

    for key in required_keys:
        if key not in data:
            errors.append({key: "This is a required key."})

    for key in data:
        if key not in required_keys + allowed_keys:
            errors.append({"unexpected_key": key})

    return errors

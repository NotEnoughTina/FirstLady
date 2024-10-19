import configparser

def load_config_section(section, config_path="config.ini"):
    """
    Loads a specified section from the config file.

    Args:
        section (str): The section to load from the config file.
        config_path (str): The path to the config file (default is 'config.ini').

    Returns:
        dict: A dictionary containing the key-value pairs from the section.
    """
    # Disable interpolation by using 'RawConfigParser'
    config = configparser.RawConfigParser()
    config.read(config_path)

    if section not in config:
        raise ValueError(f"Section '{section}' not found in {config_path}")

    section_data = {key: value.strip() for key, value in config.items(section)}

    # Parse comma-separated values into lists where needed
    for key, value in section_data.items():
        if ',' in value:  # Handle screen positions or comma-separated values
            section_data[key] = [item.strip() for item in value.split(',')]
    
    return section_data

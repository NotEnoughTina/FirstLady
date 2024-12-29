# main.py

import logging
from logging_config import applicant_logger

from utils.adb_utils import click_at_location, get_connected_devices, select_device, get_screen_size
from utils.config_utils import load_config, load_config_section
from utils.game_utils import (
    check_game_status,
    handle_applicants,
    launch_secretary_screen,
)
from utils.utils import check_time_passed, random_sleep, convert_percentage_positions

# Get the logger for this module
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting application...")
    devices = get_connected_devices()
    if not devices:
        logger.error("No devices connected.")
        raise Exception("No devices connected.")

    device_id = select_device(devices)
    logger.info(f"Using device: {device_id}")

    # Load the entire configuration
    config = load_config()

    # Load configuration sections
    templates = load_config_section(config, 'templates')
    options = load_config_section(config, 'options')
    positions = load_config_section(config, 'positions')

    # Get screen size
    screen_width, screen_height = get_screen_size(device_id)
    
    # Determine which secretary positions to use
    secretary_positions = positions.get('secretaryPositions', {})
    alternate_positions = positions.get('secretaryPositionsAlt', {})
    button_positions = positions.get('buttonPositions', {})

    # Convert positions from percentages to pixels
    secretary_positions = convert_percentage_positions(secretary_positions, screen_width, screen_height)
    alternate_positions = convert_percentage_positions(alternate_positions, screen_width, screen_height)
    button_positions = convert_percentage_positions(button_positions, screen_width, screen_height)

    last_status_check = None
    last_reset = None
    is_alternate = None

    while True:
        try:
            # Check game and secretary screen status every 10 minutes
            needs_status_check, last_status_check = check_time_passed(last_status_check, options['statusCheckTimer'])
            needs_reset, last_reset = check_time_passed(last_status_check, options['resetTimer'])
            if needs_reset or is_alternate is None:
                logger.info("Forcing reset.")
                is_alternate = launch_secretary_screen(device_id, options, templates, button_positions)

            if needs_status_check:
                is_secretary_screen = check_game_status(device_id, options, templates)
                if not is_secretary_screen:
                    logger.info("Launching secretary screen.")
                    is_alternate = launch_secretary_screen(device_id, options, templates, button_positions)

            # Handle each position in the secretary positions list
            positions = alternate_positions if is_alternate else secretary_positions

            for name, secretary_position in secretary_positions.items():
                accepted = handle_applicants(
                    device_id,
                    secretary_position,
                    button_positions,
                    options,
                    templates
                )
                if accepted > 0:
                    applicant_logger.info(
                        f"Accepted {accepted} applicants for {name}."
                    )
            random_sleep(options.get('sleep', 5))  # Main loop delay
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
            random_sleep(5)  # Delay before retrying

if __name__ == '__main__':
    main()

# utils/game_utils.py

import logging
import random
import time

from logging_config import status_logger
from .adb_utils import (
    capture_screenshot,
    click_at_location,
    get_current_running_app,
    get_screen_size,
    launch_package,
    send_back_press,
    swipe,
    swipe_down,
    swipe_up,
)
from .image_processing import find_on_screen
from .utils import random_sleep
from logging_config import applicant_logger  # For logging applicant acceptances

logger = logging.getLogger(__name__)

def check_game_status(device_id, options, templates):
    """
    Checks if the game and secretary screen are running.
    """
    package_name = options['packageName']
    is_game_running = get_current_running_app(device_id) == package_name
    if is_game_running:
        status_logger.debug(f"Game is running on device {device_id}.")
        screenshot_path = capture_screenshot(device_id)
        template_position = find_on_screen(
            screenshot_path,
            templates['firstLady'],
            threshold=float(options.get('imageMatchThreshold', 0.8)),
        )
        if template_position:
            status_logger.info("Secretary screen is active.")
            return True
        else:
            status_logger.info("Secretary screen is not active.")
    else:
        status_logger.info(f"Game is not running on device {device_id}.")
    return False

def clear_notifications(device_id, templates, sleep_timer=3, max_attempts=10):
    """
    Sends back press events to clear notifications until the home screen is visible.
    
    Parameters:
        device_id (str): The device ID.
        templates (dict): Dictionary of image templates for screen elements.
        sleep_timer (int): Time in seconds to sleep between actions.
        max_attempts (int): Maximum number of back press attempts before stopping.
    
    Returns:
        bool: True if notifications were cleared successfully, False if max attempts were reached.
    """
    attempts = 0
    
    while attempts < max_attempts:
        status_logger.info("Sending back press event to clear notifications.")
        
        # Press back and wait briefly
        send_back_press(device_id)
        random_sleep(sleep_timer)
        
        # Capture a screenshot and check for the quit button
        screen_shot = capture_screenshot(device_id)
        quit_button = find_on_screen(screen_shot, templates['quit'])
        
        # If the quit button is found, exit the loop
        if quit_button is not None:
            status_logger.info("Quit button found, clearing the last notification.")
            send_back_press(device_id)  # Final back press to confirm navigation
            random_sleep(sleep_timer)
            return True  # Notifications cleared successfully
        
        attempts += 1
        status_logger.info(f"Back press attempt {attempts} of {max_attempts}.")

    status_logger.warning("Reached max attempts to clear notifications; continuing with caution.")
    return False  # Max attempts reached without clearing notifications


def launch_secretary_screen(device_id, options, templates, button_positions):
    """
    Launches the game and navigates to the secretary screen.
    """
    package_name = options['packageName']
    boot_timer = options.get('bootTimer', 120)
    sleep_timer = options.get('sleep', 3)

    status_logger.info(f"Launching the game package: {package_name}.")
    launch_package(device_id, package_name)
    time.sleep(boot_timer)
    status_logger.info(f"Waited {boot_timer} seconds for the game to boot.")
    
    clear_notifications(device_id, templates, sleep_timer)
    random_sleep(sleep_timer)

    # open the profile screen
    click_at_location(
        button_positions['profile'][0],
        button_positions['profile'][1],
        device_id
    )
    random_sleep(sleep_timer)
    
    # ensure there is no likes
    screen_shot = capture_screenshot(device_id)
    like_accept_location = find_on_screen(screen_shot, templates['awesome'])
    if like_accept_location is not None:
        click_at_location(
            like_accept_location[0],
            like_accept_location[1],
            device_id
        )
        random_sleep(sleep_timer)
 
    # Open the positions menu
    click_at_location(
        button_positions['secrataryMenu'][0],
        button_positions['secrataryMenu'][1],
        device_id
    )

    #check if aternate positon
    random_sleep(sleep_timer)
    screen_shot = capture_screenshot(device_id)
    conquerer_position = find_on_screen(screen_shot, templates['conquerer'])
    if conquerer_position:
        # Sroll to bottom
        swipe_up(device_id, 3)

    random_sleep(sleep_timer)

    return conquerer_position is not None


def open_position_menu(device_id, secretary_position, button_positions, options):
    """
    Opens the position menu and position list for the given secretary.
    """
    sleep_interval = options['sleep']
    click_at_location(secretary_position[0], secretary_position[1], device_id)
    random_sleep(sleep_interval)
    click_at_location(
        button_positions['list'][0],
        button_positions['list'][1],
        device_id
    )
    random_sleep(sleep_interval)

def close_menu(device_id, button_positions, options):
    """
    Closes the current menu by clicking the close button twice with a delay.
    """
    sleep_interval = options['sleep']
    for _ in range(2):
        click_at_location(
            button_positions['close'][0],
            button_positions['close'][1],
            device_id
        )
        random_sleep(sleep_interval)


def accept_applicants(device_id, templates, options, max_accepts=5):
    """
    Captures and clicks on accept icons up to a maximum count.
    """
    accept_counter = 0
    sleep_interval = options['sleep']
    threshold = float(options['imageMatchThreshold'])

    while accept_counter < max_accepts:
        screenshot_path = capture_screenshot(device_id)
        icon_position = find_on_screen(
            screenshot_path,
            templates['accept'],
            threshold=threshold,
        )
        if icon_position:
            click_at_location(icon_position[0], icon_position[1], device_id)
            accept_counter += 1
            random_sleep(sleep_interval)
            applicant_logger.info(f"Accepted applicant #{accept_counter} at position {icon_position}.")
        else:
            break
    if accept_counter == 0:
        applicant_logger.info("No applicants to accept.")
    return accept_counter

def handle_applicants(device_id, secretary_position, button_positions, options, templates):
    """
    Opens the position menu, checks for applicants, accepts them, and closes the menu.
    """
    sleep_interval = options['sleep']
    threshold = float(options['imageMatchThreshold'])

    applicant_logger.info(f"Handling applicants for secretary at position {secretary_position}.")
    open_position_menu(device_id, secretary_position, button_positions, options)

    # Check if there are any applicants
    initial_screenshot = capture_screenshot(device_id)
    has_applicants = find_on_screen(
        initial_screenshot,
        templates['accept'],
        threshold=threshold,
    )

    if not has_applicants:
        applicant_logger.info("No applicants found for this secretary.")
        close_menu(device_id, button_positions, options)
        return 0

    # Swipe to the top of the list
    swipe_down(device_id, 10)

    # Process accept icons
    applicants_accepted = accept_applicants(device_id, templates, options)

    # Close position and menu
    close_menu(device_id, button_positions, options)
    applicant_logger.info(f"Finished handling applicants. Total accepted: {applicants_accepted}.")

    return applicants_accepted


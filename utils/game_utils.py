import time
from utils.adb_utils import capture_screenshot
from utils.image_processing import find_icon_on_screen


def is_home_screen(device_id, target_icon, threshold=0.75, debug=False):
    """
    Checks if the home screen is displayed by detecting the mail icon, and presses the back button
    until the mail icon is found or a max number of attempts is reached.
    
    Args:
        device_id (str): The ID of the device.
        config (dict): Configuration dictionary containing icon paths.
        max_attempts (int): The maximum number of back presses to attempt. Default is 10.
        delay (int): Delay in seconds between each check. Default is 2 seconds.
        threshold (float): Confidence threshold for template matching. Default is 0.8.
        debug (bool): If True, enables debug mode for more output. Default is False.
    
    Returns:
        bool: True if the mail icon is found (indicating the home screen), False if not found after max_attempts.
    """

    # Capture the current screen
    screenshot_path = capture_screenshot(device_id)

    print(screenshot_path)

    # Check if the mail icon is present on the screen
    if find_icon_on_screen(screenshot_path, target_icon, threshold=threshold, debug=debug):
        return True  # Mail icon found, home screen detected
    
    return False  # Mail icon not found after max_attempts
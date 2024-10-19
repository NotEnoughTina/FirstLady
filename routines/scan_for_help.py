import os
import time
import random
from utils.adb_utils import capture_screenshot, click_at_location
from utils.image_processing import find_icon_on_screen

def scan_for_help(device_id, button_icon_path):
    """
    Continuously scans the screen for a specific button and clicks it when detected.
    Counts how many people you have helped and slightly alters the click location each time.
    
    Args:
        device_id (str): The ID of the target device.
        button_icon_path (str): Path to the button icon image to look for on the screen.
    """
    people_helped = 0  # Counter for how many people you've helped
    print('Starting help scanner')
    try:
        while True:
            screenshot_path = capture_screenshot(device_id, filename="screenshot_button.png")
            print(screenshot_path)
            if screenshot_path and os.path.exists(screenshot_path):  # Ensure the file exists
                button_location = find_icon_on_screen(screenshot_path, button_icon_path, 0.7)
                if button_location:
                    # Slightly randomize the click location to avoid bot-like behavior
                    random_offset_x = random.randint(-5, 5)
                    random_offset_y = random.randint(-5, 5)
                    click_x = button_location[0] + random_offset_x
                    click_y = button_location[1] + random_offset_y
                    
                    click_at_location(click_x, click_y, device_id)
                    people_helped += 1
                    print(f"Helped {people_helped} people.")
                else:
                    print("No button found");    
            else:
                print(f"Screenshot path does not exist: {screenshot_path}")
            
            time.sleep(5)  # Sleep for a short period before checking again
    except Exception as e:
        print(f"Error in button scanning thread: {e}")

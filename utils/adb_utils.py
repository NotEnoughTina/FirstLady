import os
import tempfile
import subprocess
import re

def capture_screenshot(device_id, filename="screenshot.png"):
    """
    Captures a screenshot using ADB from a specific device and saves it to a file in the system temp directory.
    
    Args:
        device_id (str): The ID of the target device.
        filename (str): The file to save the screenshot to (filename only, will save to the system's temp folder).
    
    Returns:
        str: The path to the saved screenshot in the temp folder.
    """
    temp_dir = tempfile.gettempdir()  # Use the system's temporary directory
    path = os.path.join(temp_dir, filename)  # Construct the full path for the screenshot
    
    try:
        os.system(f"adb -s {device_id} exec-out screencap -p > {path}")
        return path
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def get_screen_size(device_id):
    """
    Retrieves the real-time screen size (width, height) of the device using ADB.
    
    Args:
        device_id (str): The ID of the target device.
        
    Returns:
        tuple: Screen width and height in pixels.
    """
    try:
        # Using 'adb dumpsys display' to get the actual screen size
        result = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'dumpsys', 'display'],
            stdout=subprocess.PIPE
        )
        output = result.stdout.decode('utf-8')

        # Look for the line that contains the logical frame or physical frame size
        viewport_match = re.search(r'logicalFrame=Rect\(\d+, \d+ - (\d+), (\d+)\)', output)
        if viewport_match:
            width = int(viewport_match.group(1))
            height = int(viewport_match.group(2))
            return width, height

        # As a fallback, try searching for deviceWidth and deviceHeight
        device_size_match = re.search(r'deviceWidth=(\d+), deviceHeight=(\d+)', output)
        if device_size_match:
            width = int(device_size_match.group(1))
            height = int(device_size_match.group(2))
            return width, height

        print("Error: Could not find screen size in dumpsys output.")
        return None, None

    except Exception as e:
        print(f"Error getting screen size: {e}")
        return None, None

def click_at_location(x, y, device_id):
    """
    Simulates a tap on the screen using ADB at the given (x, y) coordinates.
    If x or y are given as percentages (e.g., '50%'), they will be converted to absolute pixel values.
    
    Args:
        x (str or int): X-coordinate to tap. Can be an int (absolute pixels) or str ('50%').
        y (str or int): Y-coordinate to tap. Can be an int (absolute pixels) or str ('50%').
        device_id (str): The ID of the target device.
    """
    try:
        # Get screen size
        screen_width, screen_height = get_screen_size(device_id)
        
        if screen_width is None or screen_height is None:
            print("Could not retrieve screen size. Aborting click action.")
            return
        
        # Convert percentage to absolute pixels if x or y are given as strings
        if isinstance(x, str) and x.endswith('%'):
            x = int(screen_width * (float(x.strip('%')) / 100))
        if isinstance(y, str) and y.endswith('%'):
            y = int(screen_height * (float(y.strip('%')) / 100))

        # Execute ADB tap command
        os.system(f"adb -s {device_id} shell input tap {x} {y}")

    except Exception as e:
        print(f"Error clicking at location ({x}, {y}): {e}")

def get_connected_devices():
    """
    Returns a list of connected device IDs from `adb devices`.
    """
    try:
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
        lines = result.stdout.decode('utf-8').strip().split('\n')[1:]  # Skip the header line
        
        devices = [line.split()[0] for line in lines if 'device' in line]
        
        if len(devices) == 0:
            print("No devices found. Ensure that an emulator or device is running and connected.")
        else:
            print(f"Connected devices: {devices}")

        return devices
    except Exception as e:
        print(f"Error retrieving connected devices: {e}")
        return []

def select_device(devices):
    """
    Selects the first emulator or device, or prompts the user to choose if multiple are available.
    
    Args:
        devices (list): List of connected device IDs.
        
    Returns:
        str: The selected device ID.
    """
    if len(devices) == 1:
        return devices[0]  # If only one device is connected, return it
    else:
        print("Multiple devices detected. Please choose a device:")
        for i, device in enumerate(devices):
            print(f"{i}: {device}")
        choice = int(input("Enter the number of the device to use: "))
        return devices[choice]

def send_event(event, device_id):
    """
    Sends a key event to the specified device using ADB.
    
    Args:
        event (str): The name of the event to send. Supported events: 'back', 'home', 'recents', 'power', 'volume_up', 'volume_down'.
        device_id (str): The ID of the target device.
    """
    key_events = {
        'back': 4,  # KEYCODE_BACK
        'home': 3,  # KEYCODE_HOME
        'recents': 187,  # KEYCODE_APP_SWITCH
        'power': 26,  # KEYCODE_POWER
        'volume_up': 24,  # KEYCODE_VOLUME_UP
        'volume_down': 25  # KEYCODE_VOLUME_DOWN
    }

    if event in key_events:
        keycode = key_events[event]
        try:
            os.system(f"adb -s {device_id} shell input keyevent {keycode}")
        except Exception as e:
            print(f"Error sending {event} event to device {device_id}: {e}")
    else:
        print(f"Unsupported event: {event}. Supported events: {list(key_events.keys())}")

def convert_percentage_to_pixels(x_percentage, y_percentage, device_id):
    """
    Converts percentage values for x and y into pixel values based on screen size.
    
    Args:
        x_percentage (str): X-coordinate as a percentage string (e.g., '5%').
        y_percentage (str): Y-coordinate as a percentage string (e.g., '5%').
        device_id (str): The ID of the device.
        
    Returns:
        tuple: The (x, y) coordinates in pixels.
    """
    screen_width, screen_height = get_screen_size(device_id)
    
    x_pixel = int(screen_width * (float(x_percentage.strip('%')) / 100))
    y_pixel = int(screen_height * (float(y_percentage.strip('%')) / 100))
    
    return x_pixel, y_pixel
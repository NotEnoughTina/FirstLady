
from utils.adb_utils import (
    capture_screenshot,
    click_at_location,
    get_connected_devices,
    select_device,
)
from utils.config_utils import load_config_section
from utils.image_processing import find_icon_on_screen
from utils.utils import get_timestamp, random_sleep


def main():
    devices = get_connected_devices()
    if len(devices) == 0:
        raise Exception("No devices connected.")

    device_id = select_device(devices)
    print(f"Using device: {device_id}")

    icons = load_config_section('Icons')
    #secretary_positions = load_config_section('SecretaryPositions')
    secretary_positions = load_config_section('SecretaryPositions2')

    sleep_interval = 7
    list_position = ['85%', '85%']
    close_position = ['88.5%', '12.5%']

    while True:
        for name, secretary_position in secretary_positions.items():
            print(f"{get_timestamp()} Checking {name}")

            # Open the Position Menu
            click_at_location(secretary_position[0], secretary_position[1], device_id)
            random_sleep(sleep_interval)

            # Open the Position List
            click_at_location(list_position[0], list_position[1], device_id)
            random_sleep(sleep_interval)

            # Initialize counter for the number of accepts
            accept_counter = 0
            max_accepts = 5  # Maximum number of accepts per position

            # Capture a screenshot and attempt to find the icon
            while accept_counter < max_accepts:
                screenshot_path = capture_screenshot(device_id)
                icon_position = find_icon_on_screen(
                    screenshot_path,
                    icons['accept'],
                    threshold=0.65,
                    scale_range=(0.7, 1.3),
                    debug=False  # Enable debugging
                )

                if icon_position:
                    # Perform the click action
                    click_at_location(icon_position[0], icon_position[1], device_id)
                    accept_counter += 1  # Increment the counter
                    random_sleep(sleep_interval)
                else:
                    break  # Exit the loop when no more icons are found

                # Optional sleep before rechecking
                random_sleep(sleep_interval)

            if accept_counter > 0:
                print(f"\tAccepted {accept_counter} people for {name}.")

            # Close the list
            click_at_location(close_position[0], close_position[1], device_id)
            random_sleep(sleep_interval)

            # Close the position menu
            click_at_location(close_position[0], close_position[1], device_id)
            random_sleep(sleep_interval)

        random_sleep(5)  # Add random sleep to main loop

if __name__ == "__main__":
    main()

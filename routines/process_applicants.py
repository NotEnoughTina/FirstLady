import time
from utils.adb_utils import capture_screenshot, click_at_location
from utils.applicant_processing import check_blacklist, click_applicant_checkbox
from utils.image_processing import find_icon_on_screen

def process_applicants_thread(device_id, icon_paths, blacklist):
    """
    Continuously scans for icons related to applicants, checks them against the blacklist, 
    and interacts with them if necessary.
    
    Args:
        device_id (str): The ID of the target device.
        icon_paths (list): List of paths to the icon images to look for on the screen.
        blacklist (dict): Dictionary containing blacklisted names and alliance tags.
    """
    try:
        while True:
            print("Starting applicant processing cycle...")
            screenshot_path = capture_screenshot(device_id, filename="screenshot_applicants.png")
            if screenshot_path:
                process_applicants(screenshot_path, icon_paths, blacklist)
            time.sleep(150)  # Wait 2.5 minutes before next cycle
    except Exception as e:
        print(f"Error in applicant processing thread: {e}")

def process_applicants(screenshot_path, icon_paths, blacklist):
    """
    Processes applicants by finding relevant icons on the screen, and checks them against the blacklist.
    
    Args:
        screenshot_path (str): Path to the captured screenshot.
        icon_paths (list): List of paths to the icons to check.
        blacklist (dict): Dictionary containing blacklisted names and tags.
    """
    for icon_path in icon_paths:
        icon_location = find_icon_on_screen(screenshot_path, icon_path)
        if icon_location:
            click_at_location(icon_location[0], icon_location[1])
            time.sleep(2)

            # Click section to view applicants (static coordinates)
            click_at_location(500, 1500)  # Example coordinates
            time.sleep(2)

            # Example applicants; these would be extracted from the UI
            applicants = [
                {"name": "John Doe", "alliance_tag": "XYZ"},
                {"name": "Jane Smith", "alliance_tag": "DEF"},
                {"name": "Alice Johnson", "alliance_tag": "ABC"}
            ]

            # Process each applicant and click green checkbox if not blacklisted
            for i, applicant in enumerate(applicants):
                name = applicant['name']
                alliance_tag = applicant['alliance_tag']

                if not check_blacklist(name, alliance_tag, blacklist):
                    click_applicant_checkbox(i)
                else:
                    print(f"Skipping blacklisted applicant: {name} (Alliance: {alliance_tag})")

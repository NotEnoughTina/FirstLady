from typing import Tuple
import cv2
from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.logging import app_logger
from src.core.config import CONFIG
from src.core.image_processing import find_template, find_all_templates, wait_for_image, find_and_tap_template
from src.core.device import take_screenshot
from src.core.adb import get_screen_size, press_back
from src.game.controls import human_delay, humanized_tap, handle_swipes
from src.core.text_detection import (
    extract_text_from_region, 
    get_text_regions, 
    log_rejected_alliance,
    CONTROL_LIST
)
from src.core.audio import play_beep
import numpy as np

class SecretaryRoutine(TimeCheckRoutine):
    force_home: bool = True

    def __init__(self, device_id: str, interval: int, last_run: float = None, automation=None):
        super().__init__(device_id, interval, last_run, automation)
        self.secretary_types = ["strategy", "security", "development", "science", "interior"]
        self.additionalTypes = ["military", "administrative"]
        self.capture = None
        self.manual_deny = False

    def _execute(self) -> bool:
        
        """Start secretary automation sequence"""
        return self.execute_with_error_handling(self._execute_internal)
    
    def _execute_internal(self) -> bool:
        """Internal execution logic"""
        self.automation.game_state["is_home"] = False
        self.open_profile_menu(self.device_id)
        if not find_and_tap_template(
            self.device_id,
            "capitol_menu",
            error_msg="Failed to find capitol menu",
            critical=True
        ):  
            return False
        handle_swipes(self.device_id, direction="down", num_swipes=1)
        return self.process_all_secretary_positions()

    def find_accept_buttons(self) -> list[Tuple[int, int]]:
        """Find all accept buttons on the screen and sort by Y coordinate"""
        try:
            matches = find_all_templates(
                self.device_id,
                "accept"
            )
            if not matches:
                return []
            
            # Sort by Y coordinate (ascending) and X coordinate (ascending) for same Y
            sorted_matches = sorted(matches, key=lambda x: (x[1], x[0]))
            if sorted_matches:
                app_logger.debug(f"Found {len(sorted_matches)} accept buttons")
                app_logger.debug(f"Topmost button at coordinates: ({sorted_matches[0][0]}, {sorted_matches[0][1]})")
            return sorted_matches
        
        except Exception as e:
            app_logger.error(f"Error finding accept buttons: {e}")
            return []

    def find_reject_buttons(self) -> list[Tuple[int, int]]:
        """Find all reject buttons on the screen and sort by Y coordinate"""
        try:
            matches = find_all_templates(
                self.device_id,
                "reject"
            )
            if not matches:
                return []
            
            # Sort by Y coordinate (ascending) and X coordinate (ascending) for same Y
            sorted_matches = sorted(matches, key=lambda x: (x[1], x[0]))
            if sorted_matches:
                app_logger.debug(f"Found {len(sorted_matches)} reject buttons")
                app_logger.debug(f"Topmost button at coordinates: ({sorted_matches[0][0]}, {sorted_matches[0][1]})")
            return sorted_matches
        
        except Exception as e:
            app_logger.error(f"Error finding reject buttons: {e}")
            return []
    
    def open_profile_menu(self, device_id: str) -> bool:
        """Open the profile menu"""
        try:
            width, height = get_screen_size(device_id)
            profile = CONFIG['ui_elements']['profile']
            profile_x = int(width * float(profile['x'].strip('%')) / 100)
            profile_y = int(height * float(profile['y'].strip('%')) / 100)
            humanized_tap(device_id, profile_x, profile_y)

            # Look for notification indicators
            notification = wait_for_image(
                device_id,
                "awesome",
                timeout=CONFIG['timings']['menu_animation'],
            )
            
            if notification:
                humanized_tap(device_id, notification[0], notification[1])
                press_back(device_id)
                human_delay(CONFIG['timings']['menu_animation'])

            return True
        except Exception as e:
            app_logger.error(f"Error opening profile menu: {e}")
            return False

    def exit_to_secretary_menu(self) -> bool:
        """Exit back to secretary menu"""
        try:
            max_attempts = 10
            for _ in range(max_attempts):
                if self.verify_secretary_menu():
                    return True
                    
                press_back(self.device_id)
                human_delay(CONFIG['timings']['menu_animation'])
                
            app_logger.error("Failed to return to secretary menu")
            return False
            
        except Exception as e:
            app_logger.error(f"Error exiting to secretary menu: {e}")
            return False
    
    def verify_secretary_menu(self) -> bool:
        """Verify we're in the secretary menu"""
        return wait_for_image(
            self.device_id,
            "president",
            timeout=CONFIG['timings']['menu_animation']
        ) is not None
    
    def process_secretary_position(self, name: str) -> bool:
        """Process a single secretary position"""
        try:        
            # Find and click secretary position
            if not find_and_tap_template(
                self.device_id,
                name,
                error_msg=f"Could not find {name} secretary position",
                critical=True
            ):
                return True  # Continue with next position
            
            human_delay(CONFIG['timings']['tap_delay'])
            
            # Find and click list button
            if not find_and_tap_template(
                self.device_id,
                "list",
                error_msg="List button not found",
                critical=True,
                timeout=CONFIG['timings']['list_timeout']
            ):
                return False

            accept_locations = self.find_accept_buttons()
            if accept_locations:
                # Scroll to top if needed
                if len(accept_locations) > 5:
                    handle_swipes(self.device_id, direction="up")
                    human_delay(CONFIG['timings']['settle_time'] * 2)
                    accept_locations = self.find_accept_buttons()
                
                processed = 0
                accepted = 0
                
                while processed < 5:  # Max 8 applicants
                    accept_locations = self.find_accept_buttons()
                    if not accept_locations:
                        break
                    
                    topmost_accept = accept_locations[0]
                    
                    if len(CONTROL_LIST['whitelist']['alliance']) > 0:
                        if not take_screenshot(self.device_id):
                            break

                        current_screenshot = cv2.imread('tmp/screen.png')
                        if current_screenshot is None:
                            break

                        alliance_region, name_region, screenshot = get_text_regions(
                            topmost_accept,
                            self.device_id,
                            existing_screenshot=current_screenshot
                        )

                        if screenshot is None:
                            continue

                        alliance_text, original_text = extract_text_from_region(
                            self.device_id,
                            alliance_region,
                            languages='eng',
                            img=screenshot
                        )

                        if alliance_text in CONTROL_LIST['whitelist']['alliance']:
                            humanized_tap(self.device_id, topmost_accept[0], topmost_accept[1])
                            app_logger.debug(f"Tapping accept at coordinates: ({topmost_accept[0]}, {topmost_accept[1]})")
                            app_logger.info(f"Accepted candidate with alliance: {alliance_text} for {name}")
                            accepted += 1
                        else:
                            # Handle rejection
                            app_logger.info(f"Rejecting candidate with alliance: {alliance_text} for {name}")
                            log_rejected_alliance(alliance_text, original_text)
                            
                            if self.manual_deny:
                                play_beep()
                                input('Press Enter to continue...')
                            
                            # Try reject button first
                            reject_buttons = self.find_reject_buttons()
                            if reject_buttons:
                                # Get topmost reject button
                                reject_button = reject_buttons[0]
                                # Verify it's aligned with our accept button vertically
                                if abs(reject_button[1] - topmost_accept[1]) <= 10:  # 10 pixel tolerance
                                    humanized_tap(self.device_id, reject_button[0], reject_button[1])
                                    app_logger.debug(f"Tapping reject at coordinates: ({reject_button[0]}, {reject_button[1]})")
                                    if not find_and_tap_template(
                                        self.device_id,
                                        "confirm",
                                        error_msg="Failed to find confirm button",
                                        critical=True
                                    ):
                                        continue
                            else:
                                # No reject buttons found, try confirm
                                if not find_and_tap_template(
                                    self.device_id,
                                    "confirm",
                                    error_msg="Failed to find confirm button",
                                    critical=True
                                ):
                                    continue
                    else:
                        # No whitelist - accept all
                        humanized_tap(self.device_id, topmost_accept[0], topmost_accept[1])
                    
                    processed += 1
                    human_delay(CONFIG['timings']['settle_time'])
                                
            # Exit menus with verification
            if not self.exit_to_secretary_menu():
                app_logger.error("Failed to exit to secretary menu")
                return False
            
            return True
            
        except Exception as e:
            app_logger.error(f"Error processing secretary position: {e}")
            if not self.exit_to_secretary_menu():
                app_logger.error("Failed to exit to secretary menu after error")
                return False
            return True
        
    def find_positions_with_applicants(self) -> list[str]:
        """Find all secretary positions that have applicants"""
        try:
            positions_to_process = []
            
            # Find all secretary positions
            all_positions = {}
            secretary_types = self.secretary_types + self.additionalTypes
            for position_type in secretary_types:
                positions = find_all_templates(
                    self.device_id,
                    position_type
                )
                if positions:
                    all_positions[position_type] = positions[0]  # Take first match for each type
                    app_logger.debug(f"Found {position_type} position at ({positions[0][0]}, {positions[0][1]})")
            # Find all applicant icons
            applicant_locations = find_all_templates(
                self.device_id,
                "has_applicant"
            )
            
            if not applicant_locations:
                app_logger.debug("No applicant icons found")
                return []
            
            app_logger.debug(f"Found {len(applicant_locations)} applicant icons:")
            for i, (x, y) in enumerate(applicant_locations):
                app_logger.debug(f"  Applicant {i+1}: ({x}, {y})")
            
            # For each position, check if there's an applicant icon nearby
            for position_type, pos_loc in all_positions.items():
                pos_x, pos_y = pos_loc
                
                # Check each applicant icon
                for app_x, app_y in applicant_locations:
                    x_diff = app_x - pos_x
                    y_diff = app_y - pos_y
                    # Check if applicant icon is within 100 pixels horizontally and 25 pixels vertically
                    if abs(x_diff) <= 100 and abs(y_diff) <= 28:
                        positions_to_process.append(position_type)
                        app_logger.info(f"Found applicant for {position_type} position")
                        break
            
            return positions_to_process
            
        except Exception as e:
            app_logger.error(f"Error finding positions with applicants: {e}")
            return []

    def process_all_secretary_positions(self) -> bool:
        """Process all secretary positions that have applicants"""
        positions_to_process = self.find_positions_with_applicants()
        
        if not positions_to_process:
            app_logger.info("No positions with applicants found")\
            # ensure the game is not glitched and we can still access the secretary menu
            if not find_and_tap_template(
                self.device_id,
                self.secretary_types[0],
                error_msg=f"Could not find {self.secretary_types[0]} secretary position",
                critical=True
            ):
                raise RuntimeError('secretary not accessible')
            
            human_delay(CONFIG['timings']['tap_delay'])
            
            # Find list button
            if not find_template(
                self.device_id,
                "list",
            ):
                raise RuntimeError('secretary not accessible')
            
            return True
        
        for name in positions_to_process:
            if not self.process_secretary_position(name):
                return False
        return True
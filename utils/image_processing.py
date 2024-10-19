import cv2
import numpy as np

def find_icon_on_screen(screenshot_path, icon_path, threshold=0.8, scale_range=(0.7, 1.3), debug=False):
    """
    Find the position of a specific icon in a screenshot using multi-scale template matching.

    Args:
        screenshot_path (str): The path to the screenshot image.
        icon_path (str): The path to the icon template image.
        threshold (float): Matching threshold (0 to 1). Default is 0.8.
        scale_range (tuple): The range of scales to test. Default is (0.7, 1.3).
        debug (bool): If True, enables debug mode to display intermediate results.

    Returns:
        (int, int) or None: The (x, y) coordinates of the top-left corner of the matched region with the smallest y coordinate, or None if no match is found.
    """
    try:
        # Load images
        screenshot = cv2.imread(screenshot_path)
        icon = cv2.imread(icon_path)

        if screenshot is None:
            raise ValueError(f"Screenshot image not found at {screenshot_path}")
        if icon is None:
            raise ValueError(f"Icon image not found at {icon_path}")

        icon_height, icon_width = icon.shape[:2]

        # Initialize list to store all potential matches
        all_matches = []

        # Loop over different scales of the icon
        scales = np.linspace(scale_range[0], scale_range[1], 20)
        for scale in scales:
            # Resize the icon template
            resized_icon = cv2.resize(icon, (int(icon_width * scale), int(icon_height * scale)))
            resized_height, resized_width = resized_icon.shape[:2]

            # Perform template matching
            result = cv2.matchTemplate(screenshot, resized_icon, cv2.TM_CCOEFF_NORMED)

            # Find locations where the matching result is above the threshold
            locations = np.where(result >= threshold)
            matches = list(zip(*locations[::-1]))  # Convert to (x, y) coordinates

            # Adjust match coordinates for the current scale and collect them
            for pt in matches:
                x, y = pt
                all_matches.append({
                    'x': x,
                    'y': y,
                    'w': resized_width,
                    'h': resized_height,
                    'scale': scale,
                    'score': result[y, x]
                })

            if debug and matches:
                print(f"Scale {scale:.2f}: Found {len(matches)} matches.")

        if all_matches:
            # Select the match with the smallest y coordinate
            best_match = min(all_matches, key=lambda m: m['y'])

            if debug:
                print(f"Best match at (x={best_match['x']}, y={best_match['y']}) with scale {best_match['scale']} and score {best_match['score']}")
                top_left = (best_match['x'], best_match['y'])
                bottom_right = (top_left[0] + best_match['w'], top_left[1] + best_match['h'])
                cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                cv2.imshow('Best Match', screenshot)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return (best_match['x'], best_match['y'])
        else:
            if debug:
                print("No matches found.")
            return None

    except Exception as e:
        print(f"Error finding icon on screen: {e}")
        return None

def check_blacklist(applicant_name, alliance_tag, blacklist):
    """
    Checks if an applicant or their alliance tag is in the blacklist.
    
    Args:
        applicant_name (str): The name of the applicant.
        alliance_tag (str): The alliance tag of the applicant.
        blacklist (dict): Dictionary containing blacklisted names and alliance tags.
    
    Returns:
        bool: True if the applicant's name or alliance tag is in the blacklist, False otherwise.
    """
    if applicant_name in blacklist['names']:
        print(f"Applicant '{applicant_name}' is in the blacklist.")
        return True
    if alliance_tag in blacklist['tags']:
        print(f"Alliance tag '{alliance_tag}' is in the blacklist.")
        return True
    return False

def click_applicant_checkbox(index):
    """
    Simulates clicking the checkbox next to an applicant.
    
    Args:
        index (int): The index of the applicant in the list (used to calculate position).
    """
    checkbox_x = 800  # Example X-coordinate for the checkboxes
    checkbox_y = 300 + (index * 150)  # Y-coordinate changes for each applicant
    from utils.adb_utils import click_at_location
    click_at_location(checkbox_x, checkbox_y)

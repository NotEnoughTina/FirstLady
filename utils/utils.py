import time
import random
from datetime import datetime

def random_sleep(base_interval, variation=0.5):
    """
    Sleep for a random amount of time, adding a slight variation to the base interval.
    """
    time.sleep(random.uniform(base_interval - variation, base_interval + variation))

def get_timestamp():
    """
    Returns the current timestamp as a formatted string.
    """
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

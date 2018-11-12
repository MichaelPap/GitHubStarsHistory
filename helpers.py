import os
import json
from properties import ResultsDir

def print_usage():
    """
    Prints the usage information of this python file.
    """
    print("Usage: python starsHistoryCalculator.py arg")
    print("where arg can be the following:")
    print("   github url (e.g. https://github.com/user/repo)")
    
def write_results_to_disk(stars_info, name):
    """
    Writes the stars calculation results to disk.
    
    :param stars_info: the calculated stars information.
    :param name: the name of the file.
    """
    
    with open(os.path.join(ResultsDir, name), 'w') as outfile:
        json.dump(stars_info, fp = outfile, sort_keys = True, indent = 3)
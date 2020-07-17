import os

"""
  PANDORA PALETTIZER
  First written for use in PANDORA

  Author: Disyer
  Date: 2020/07/17
"""

def search_for_file_in(directory, filename):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == filename:
                return os.path.abspath(os.path.join(root, file))

def next_power_of_2(x):
    return 1 if x == 0 else 2**(x - 1).bit_length()

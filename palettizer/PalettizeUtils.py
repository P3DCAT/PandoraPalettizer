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
    return 1 if x == 0 else 1<<(x - 1).bit_length()

def previous_power_of_2(x):
    return next_power_of_2(x) // 2

def closest_power_of_2(x, threshold):
    """
    Returns the closest power of two of a number.
        :x: The number to compare against.
        :threshold: A float number between 1.0 and 2.0.
            If threshold is 1.0, the power of two will always be downscaled.
            If threshold is 1.5, the power of two will be rounded.
            If threshold is 2.0, the power of two will always be upscaled.
    """
    next_power = next_power_of_2(x)
    previous_power = next_power // 2
    return next_power if (x / previous_power) >= threshold else previous_power

def get_power_of_2(x, power_type, threshold):
    if x & (x - 1) == 0:
        # We are already a power of two!
        return x

    if power_type == 'upscale':
        return next_power_of_2(x)
    elif power_type == 'downscale':
        return previous_power_of_2(x)
    else:
        return closest_power_of_2(x, threshold)

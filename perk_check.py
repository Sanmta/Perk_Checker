import cv2
import os
import numpy as np

# function to check if the perks in the build exist
def check_perks(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, detected_build_survivor_4, expected_build):
    if ((sorted(detected_build_survivor_1) == sorted(expected_build)) == True):
        return True
    elif ((sorted(detected_build_survivor_2) == sorted(expected_build)) == True):
        return True
    elif ((sorted(detected_build_survivor_3) == sorted(expected_build)) == True):
        return True
    elif ((sorted(detected_build_survivor_4) == sorted(expected_build)) == True):
        return True
    else:
        return False

def find_partial_builds(detected_build_survivor_1, detected_build_survivor_2, detected_build_survivor_3, expected_build):
    if (any(detected_build_survivor_1) == any(expected_build)):
        return find_non_matching_values(detected_build_survivor_1, expected_build)

    elif (any(detected_build_survivor_2) == any(expected_build)):
        return find_non_matching_values(detected_build_survivor_1, expected_build)

    elif (any(detected_build_survivor_3) == any(expected_build)):
        return find_non_matching_values(detected_build_survivor_1, expected_build)

    else:
        return find_non_matching_values(detected_build_survivor_1, expected_build)

# additional function to get the differences between two builds
def find_non_matching_values(detected, expected):
    non_matching_values = []
    for i, item in enumerate(expected):
        if item not in detected:
            non_matching_values.append((i+1, item))
    return non_matching_values
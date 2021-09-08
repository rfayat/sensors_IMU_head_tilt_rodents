"""A few numpy helper functions for the processing pipelines.

Author: Romain Fayat, March 2021
"""
import numpy as np


def index_true_intervals(arr):
    "Return the left and right idx of the True intervals of a 1D bool array."
    left_boundaries = np.append(arr[0], (~arr[:-1]) & arr[1:])
    left_boundaries_idx = np.where(left_boundaries)[0]
    right_boundaries = np.append(arr[:-1] & (~arr[1:]), arr[-1])
    right_boundaries_idx = np.where(right_boundaries)[0]
    return left_boundaries_idx, right_boundaries_idx


def dilate_boolean(arr, width):
    "Apply a dilation operation (sim. to image analysis) on a 1D bool array."
    out = arr.copy()
    left_boundaries_idx, right_boundaries_idx = index_true_intervals(arr)

    for l_bound in left_boundaries_idx:
        out[max(l_bound - width, 0): l_bound] = True
    for r_bound in right_boundaries_idx:
        out[(r_bound + 1):min(r_bound + 1 + width, len(arr))] = True
    return out


def erode_boolean(arr, width):
    "Apply an erosion operation (sim. to image analysis) on a 1D bool array."
    out = arr.copy()
    left_boundaries_idx, right_boundaries_idx = index_true_intervals(arr)

    for l_bound in left_boundaries_idx:
        out[l_bound:min(l_bound + width, len(arr))] = False
    for r_bound in right_boundaries_idx:
        out[max(r_bound + 1 - width, 0):r_bound + 1] = False
    return out


def erode_dilate(arr, width):
    "Apply an erosion followed by a dilation on a 1D bool array."
    return dilate_boolean(erode_boolean(arr, width=width), width=width)


def dilate_erode(arr, width):
    "Apply an dilation followed by an erosion on a 1D bool array."
    return erode_boolean(dilate_boolean(arr, width=width), width=width)

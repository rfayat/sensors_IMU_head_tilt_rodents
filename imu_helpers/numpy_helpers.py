"""A few numpy and scipy helper functions for the processing pipelines.

Author: Romain Fayat, March 2021
"""
import numpy as np
from scipy.signal import butter, filtfilt


def butter_lowpass(cutoff, fs, order=2):
    "Create a lowpass filter."
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    "Apply a lowpass filter to a time series."
    b, a = butter_lowpass(cutoff, fs, order=order)
    # Forward and backward filtering to preserve the phase of the signal
    y = filtfilt(b, a, data)
    return y


def index_true_intervals(arr):
    "Return the left and right idx of the True intervals of a 1D bool array."
    left_boundaries = np.append(arr[0], (~arr[:-1]) & arr[1:])
    left_boundaries_idx = np.where(left_boundaries)[0]
    right_boundaries = np.append(arr[:-1] & (~arr[1:]), arr[-1])
    right_boundaries_idx = np.where(right_boundaries)[0]
    return left_boundaries_idx, right_boundaries_idx


def get_interval_number(arr):
    """From an array of boolean, attribute a number to each True interval.

    This function returns an array of integers of same length as arr with the,
    with the interval number of each element. False values are set to -1.

    Example:
    -------
    >>> get_interval_number(np.array([False, False, True, True, False, True],
                            dtype=bool))
    array([-1, -1, 0, 0, -1, 1])

    """
    interval_number = np.full(len(arr), -1, dtype=int)
    left_boundaries_idx, right_boundaries_idx = index_true_intervals(arr)
    intervals_durations = right_boundaries_idx - left_boundaries_idx + 1
    interval_number[arr] = np.repeat(np.arange(len(intervals_durations)),
                                     intervals_durations)
    return interval_number


def apply_function_to_intervals(X, condition, f, **kwargs):
    """Apply f to X for each interval of contiguous True values of condition.

    Example:
    -------
    >>> apply_function_to_intervals(np.arange(5),
    ...                             np.array([1, 1, 0, 1, 0]),
    ...                             np.mean)
    array([0.5, 3. ])

    """
    boundaries = index_true_intervals(condition)
    n_intervals = len(boundaries[0])
    output = np.full(n_intervals, np.nan)
    # Loop over each interval of True values
    for i, (start, stop) in enumerate(zip(*boundaries)):
        output[i] = f(X[start:stop + 1], **kwargs)
    return output


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

"""Helpers for computing immobility periods.

Author: Romain Fayat, July 2021
"""
import numpy as np
from .numpy_helpers import dilate_erode, erode_dilate
from scipy.ndimage import gaussian_filter


def get_immobility(gyr_norm, sr=300, treshold=12.,
                   merging_time=.1, minimal_duration=.5):
    """Compute the immobility periods from the gyroscope norm.

    After applying a `threshold` to the gyroscope norm (`gyr_norm`, in deg/s,
    sampled at `sr` Herz), the resulting intervals closer in time than
    `merging_time` seconds are merged to discard short outliers during
    immobility. Periods of immobility lasting less than `minimal_duration`
    seconds are then ignored.

    Inputs
    ------
    gyr_norm : array, shape = (n_samples,)
        The euclidean norm of the gyroscope data (in deg/s).
    sr : float (default: 300.)
        The sampling rate of the time series, in Herz.
    threshold : float (default: 12.)
        The threshold, in deg/s, applied to the norm of the gyroscope data.
    merging_time : float (default: .1)
        The duration (in seconds) used for merging immobility periods close
        in time. Periods of immobility closer in time than this value will be
        merged.
    minimal_duration : float (default: .5)
        The minimal duration of immobility periods (in seconds), periods of
        immobility lasting less than this value will be ignored.

    Returns
    -------
    is_immobile : array, shape = (n_samples,)
        An array of booleans indicating if each sample belongs to an immobility
        period.

    Notes
    -----
    This function implements the method described  and used for the data
    analysis in Fayat et al., 2021. An alternative method allowing to set only
    two parameters (instead of three) would be to simply first smooth the
    gyroscope norm time series using a Gaussian kernel before applying a
    threshold on the result (cf get_immobility_smooth).

    """
    is_immobile = gyr_norm < treshold

    # Merge immobility periods close in time
    merging_idx = int(merging_time * sr)
    is_immobile = dilate_erode(is_immobile, width=int(merging_idx / 2))

    # Remove short immobility periods
    minimal_duration_idx = int(minimal_duration * sr)
    is_immobile = erode_dilate(is_immobile,
                               width=int(minimal_duration_idx / 2))
    return is_immobile


def get_immobility_smooth(gyr_norm, sr=300, threshold=12., sigma=.5):
    """Compute the immobility periods from the smoothed gyroscope norm.

    The gyroscope norm is smoothed using a gaussian kernel, the function then
    returns an array indicating for which samples the result is below an
    input threshold.

    Inputs
    ------
    gyr_norm : array, shape = (n_samples,)
        The euclidean norm of the gyroscope data (in deg/s).
    sr : float (default: 300.)
        The sampling rate of the time series, in Herz.
    threshold : float (default: 12.)
        The threshold in deg/s, applied to the smoothed norm of the gyr data.
    sigma : float (default: .5)
        The standard deviation of the gaussian kernel used for smoothing the
        gyroscope norm, in seconds.

    Returns
    -------
    is_immobile : array, shape = (n_samples,)
        An array of booleans indicating if each sample belongs to an immobility
        period.

    """
    sigma_bins = int(sigma * sr)
    gyr_norm_smoothed = gaussian_filter(gyr_norm, sigma_bins)
    return gyr_norm_smoothed < threshold

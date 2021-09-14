"""Code allowing to estimate offsets of an inertial sensor.

Author: Romain Fayat, December 2020
"""
import numpy as np
import scipy.optimize
from .numpy_helpers import apply_function_to_intervals
from .immobility_detection import get_immobility_smooth


class IMU_Calibrator:
    "Objects used for computing accelerometer and gyroscope offsets."

    def __init__(self,
                 acc_offsets=np.full(3, np.nan),
                 gyr_offsets=np.full(3, np.nan),
                 sr=300.,
                 n_static_positions=3):
        "Create the calibrator and store calibaration parameters."
        self._validate_input_arrays(acc_offsets, gyr_offsets)
        self.acc_offsets = acc_offsets
        self.gyr_offsets = gyr_offsets
        self.sr = float(sr)
        self.n_static_positions = int(n_static_positions)

    def _validate_input_arrays(self, acc_offsets, gyr_offsets):
        "Make sure the input offset values are valid (arrays of length 3)."
        for arr, name in zip([acc_offsets, gyr_offsets], ["Acc", "Gyr"]):
            try:
                assert isinstance(arr, np.ndarray) and acc_offsets.shape == (3,)  # noqa E501
            except AssertionError:
                raise ValueError(f"{name} offsets must be an array of len 3.")

    def compute_offsets(self, acc, gyr, immobility_threshold=5.):
        "Compute both acc and gyr offsets from a multi-point tumble test."
        # Find the immobility periods by applying a threshold on the gyr norm
        gyr_norm = np.linalg.norm(gyr, axis=1)
        is_immobile = get_immobility_smooth(gyr_norm,
                                            threshold=immobility_threshold,
                                            sr=self.sr)
        # Computation of the gyroscope offsets
        self.gyr_offsets = np.median(gyr[is_immobile], axis=0)
        # Select the n_static_positions longest intervals
        interval_lengths = apply_function_to_intervals(acc, is_immobile, len)
        idx_interval_selected = np.argsort(interval_lengths)[-self.n_static_positions:]  # noqa E501
        # Compute the mean accelerometer values during each immobile interval
        # and use the values corresponding to the n_static_positions longest
        # to compute the acc offsets
        binned_acc = apply_function_to_intervals(acc, is_immobile,
                                                 np.mean, axis=0)
        self.acc_offsets = get_offset(binned_acc[idx_interval_selected],
                                      expected_norm=1)


def cost_function_offset(offsets, data, expected_norm=1.):
    """Error given a 2d array of data and a set of offset values.

    The cost is computed by comparing the norm of the corrected data to the
    `expected_norm` as :
        mean((||data - offsets|| - expected_norm)**2)

    """
    corrected = data - offsets
    corrected_norm = np.linalg.norm(corrected, axis=1)
    return np.mean((corrected_norm - expected_norm)**2)


def get_offset(data, expected_norm, x0=np.zeros(3), **kwargs):
    "Return the offsets computed from data to match a target norm."
    res = scipy.optimize.minimize(cost_function_offset,
                                  args=(data, expected_norm),
                                  x0=x0, **kwargs)
    return res.x

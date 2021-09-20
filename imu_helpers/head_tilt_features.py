"""Functions for computing IMU-extracted features describing postural deficits.

Author: Romain Fayat, July 2021
"""
import numpy as np
from scipy.spatial.transform import Rotation as R


def get_angle_x_to_xz(v, degrees=True):
    "Return the angle of the rotation around x that puts v in the xz plane."
    # Compute the two possible angles between z and v
    theta1 = np.arctan2(-v[1], v[2])
    theta2 = np.arctan2(v[1], -v[2])

    # Select the one with the smallest absolute value
    theta = theta1 if np.abs(theta1) < np.abs(theta2) else theta2

    # Return the result in degrees or radians
    if degrees:
        return np.degrees(theta)
    else:
        return theta


def Q_inv_rotate_V(Q, V):
    """Rotate each element of V by the inverse of the corresponding quat of Q.

    Inputs
    ------
    Q: array, shape=(n_samples, 4)
        The quaternions to invert before rotating the elements of V.
        The columns correspond to qw, qx, qy, qz.
    V: array, shape=(n_samples, 3)
        The vectors to rotate
    """
    r = R.from_quat(Q[:, [1, 2, 3, 0]])
    return r.inv().apply(V)

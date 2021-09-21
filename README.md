# Inertial measurement of head tilt in rodents: principles and applications to vestibular research

This repository contains code examples and preprocessed data samples allowing to replicate the main analysis pipelines presented in [**Fayat et al., 2021 (DOI:10.3390/s21186318)**](https://www.mdpi.com/1424-8220/21/18/6318), published in the [special issue dedicated to "Advances in Inertial Sensors" by the journal Sensors](https://www.mdpi.com/journal/sensors/special_issues/iertial_sensors).

If you use parts of this code in a scientific publication, please be kind enough to include a citation of the original paper:

```bibtex
@Article{s21186318,
AUTHOR = {Fayat, Romain and Delgado Betancourt, Viviana and Goyallon, Thibault and Petremann, Mathieu and Liaudet, Pauline and Descossy, Vincent and Reveret, Lionel and Dugué, Guillaume P.},
TITLE = {Inertial Measurement of Head Tilt in Rodents: Principles and Applications to Vestibular Research},
JOURNAL = {Sensors},
VOLUME = {21},
YEAR = {2021},
NUMBER = {18},
ARTICLE-NUMBER = {6318},
URL = {https://www.mdpi.com/1424-8220/21/18/6318},
ISSN = {1424-8220},
ABSTRACT = {Inertial sensors are increasingly used in rodent research, in particular for estimating head orientation relative to gravity, or head tilt. Despite this growing interest, the accuracy of tilt estimates computed from rodent head inertial data has never been assessed. Using readily available inertial measurement units mounted onto the head of freely moving rats, we benchmarked a set of tilt estimation methods against concurrent 3D optical motion capture. We show that, while low-pass filtered head acceleration signals only provided reliable tilt estimates in static conditions, sensor calibration combined with an appropriate choice of orientation filter and parameters could yield average tilt estimation errors below 1.5∘ during movement. We then illustrate an application of inertial head tilt measurements in a preclinical rat model of unilateral vestibular lesion and propose a set of metrics describing the severity of associated postural and motor symptoms and the time course of recovery. We conclude that headborne inertial sensors are an attractive tool for quantitative rodent behavioral analysis in general and for the study of vestibulo-postural functions in particular.},
DOI = {10.3390/s21186318}
}
```

If you find a bug or want me to add code for an additional specific pipeline presented in the paper, feel free to open an issue on github, I'll do my best to process your request in a reasonable amount of time.

## Installation
Download the repository using git and change your working directory to  the resulting folder as follows :
```bash
$ git clone --recursive https://github.com/rfayat/sensors_IMU_head_tilt_rodents.git
$ cd sensors_IMU_head_tilt_rodents
```
The `--recursive` tag added to the `git clone` command ensures the content of the submodules will also be downloaded.

### Installation of the requirements
The submodule `angle_visualization` depends on [cartopy](https://scitools.org.uk/cartopy/docs/latest/) which might require a few extra steps before running the installation (i.e. installation of geos, see for instance [here](https://stackoverflow.com/a/56956172/12841990)).

It is recommended to use a dedicated [conda](https://docs.conda.io) environment to handle the installation of the requirements. The installation of [cartopy](https://scitools.org.uk/cartopy/docs/latest/) with pip is known to sometimes cause issues (see [here](https://stackoverflow.com/a/53745635/12841990) for instance).

From the cloned repository's folder, create a conda environment, activate it and install the additional submodules as follows:

```bash
$ # Create an environment from the environment.yml file
$ conda env create
$ conda activate fayat_et_al
$ # Compilation of the cython code
$ cd madgwick_imu
$ python setup.py build_ext --inplace
$ cd ..
$ # Installation of the standalone packages
$ pip install ./madgwick_imu ./SphereProba ./angle_visualization
```

### Testing the installation
WIP: Clean tests still need to be written for the submodules, for now you can test your installation by running the example notebooks.

## Code overview

### Independent packages
To ensure reproducibility, the modules written for this work were added as frozen submodules in their current states here but you can also feel free to have a look at or contribute to the respective corresponding repositories.

#### [rfayat/angle_visualization](https://github.com/rfayat/angle_visualization)
A few python tools for visualizing 3D angles, shapes and histograms on the unit sphere with matplotlib. This package was in particular developed for computing head tilt maps and allowing visualize them in 3D as well as projected in 2D using [cartopy](https://scitools.org.uk/cartopy/docs/latest/).

#### [rfayat/SphereProba](https://github.com/rfayat/SphereProba)
Fit and manipulate a few probability distribution functions on the unit S2 sphere. This packages was developed in particular for fitting a [von Mises-Fisher distribution](https://en.wikipedia.org/wiki/Von_Mises-Fisher_distribution) on the head tilt maps by computing the mean direction of the head tilt distribution on a triangulated sphere, weighted by the number of times the head tilt belonged to each one of the resulting facets.


#### [Mayitzin/ahrs](https://github.com/Mayitzin/ahrs) and its fork [rfayat/ahrs](https://github.com/rfayat/ahrs)
The [ahrs package](https://ahrs.readthedocs.io), developped by [Mayitzin](https://github.com/Mayitzin) is a great, extensive and amazingly documented collection of Attitude and Heading Reference Systems (AHRS) filters in pure python. Its vocation is more educational than focused on efficiency, resulting in a very readable pure python implementation whose execution is relatively slow for long times series (`for` loops over the time series for the iterative filters).

In order to perform the parameter optimization presented in the paper for the [Madgwick](https://ahrs.readthedocs.io/en/latest/filters/madgwick.html), [Mahony](https://ahrs.readthedocs.io/en/latest/filters/mahony.html) and [EKF](https://ahrs.readthedocs.io/en/latest/filters/ekf.html) filters in a reasonable amount of time given the size of the dataset (~1M data samples) while leveraging [ahrs](https://ahrs.readthedocs.io)'s great python API, the code for these filters was wrapped in a custom [numba jitclass](https://numba.pydata.org/numba-doc/latest/user/jitclass.html), enabling code compilation and thus sizeable shrinkage of the execution time, to the cost of adding an overhead to the computations (a bit more information,  execution time benchmarking, and also the reasons for not opening a pull request to [Mayitzin/ahrs](https://github.com/Mayitzin/ahrs), can be found [here](https://github.com/Mayitzin/ahrs/discussions/35)).

The resulting fork of ahrs can be found [here](https://github.com/rfayat/ahrs). However, even if wrapping [Mayitzin](https://github.com/Mayitzin)'s code in a  [numba jitclass](https://numba.pydata.org/numba-doc/latest/user/jitclass.html) perfectly fitted our needs for the analysis presented in this work (one-shot execution over a relatively large dataset), I would advise you **against using [rfayat/ahrs](https://github.com/rfayat/ahrs) for your routine analysis** as the [numba's jitclass](https://numba.pydata.org/numba-doc/latest/user/jitclass.html) feature is still experimental and the implemented wrappers were for instance broken by the latest updates of [numpy](https://numba.pydata.org/numba-doc/latest/user/jitclass.html).

#### [rfayat/madgwick_imu](https://github.com/rfayat/madgwick_imu)
This package consists in a Cython (i.e. compiled) implementation of the Madgwick filter, wrapped in [ahrs](https://ahrs.readthedocs.io/en/latest/filters/madgwick.html)'s API. It can be seen as an easy-to-install (with pip) and easy-to-use (with python) alternative to the [ahrs package](https://ahrs.readthedocs.io) for routine computation of the [Madgwick filter](https://ahrs.readthedocs.io/en/latest/filters/madgwick.html) with performance approaching low-level language implementations of the algorithm.


Some of the credit for this package goes to [ghyomm](https://github.com/ghyomm), who provided his custom Rcpp implementation used as a starting point for writting the Cython code as well as to the [original C++](https://github.com/xioTechnologies/Fusion) code from which this implementation derives.

### Additional code used for the analysis
A few additional functions / classes are available in the [imu_helpers](imu_helpers) folder. To use it, simply work from the repositories folder or add it to your python path environment variable.

#### Offset values estimates
After performing a multi-point tumble test, as described in the paper, the corresponding data can be feed to `IMU_Calibrator` defined in [imu_helpers.offset_computation](imu_helpers/offset_computation.py) to compute an estimate of the accelerometer and gyroscope offsets using the optimization pipeline described in the paper as follows:

```python
from imu_helpers import IMU_Calibrator
# n_static_positions is an integer corresponding to the number of orientations
# in which the sensor was left static during calibration
c = IMU_Calibrator(sr=...,  # Sampling rate, in Hz
                   n_static_positions=...)
# Compute the offsets from the multi-point tumble test inertial data
c.compute_offsets(acc, gyr)
# The acc and gyr offset estimates are now properties of `c`
print(c.acc_offsets, c.gyr_offsets)
```

#### Detection of active/immobile periods
The `get_immobility` function implements the pipeline for detecting immobility periods presented in the original article, have a look at [its documentation](imu_helpers/immobility_detection.py) for more.

```python
import numpy as np
from imu_helpers import get_immobility
SR = 300.  # sampling rate in Herz
# gyr is a (n_samples, 3) array of x, y, z gyroscope values
# degrees by seconds
gyr_norm = np.linalg.norm(gyr, axis=1)
is_immobile = get_immobility(gyr_norm, sr=SR)
```

Alternatively, you can detect immobility periods using a threshold on the smoothed gyroscope norm using the `get_immobility_smooth` function. This method has the advantage of having only two parameters to set (instead of 3 for `get_immobility`) and to avoid potential false positive in particular during episodes yielding relatively high-frequency signals. These advantages however come to the cost of having boundaries a bit less sharp due to the Gaussian kernel applied to the gyroscope norm. I personally recommend you using `get_immobility_smooth` rather than `get_immobility` if you don't mind systematically adding a *safety margin* around active periods.

#### Extraction of features describing lesion-induced deficits
A few helper functions for dealing with 3D angles are available in [head_tilt_features.py](imu_helpers/head_tilt_features.py), example use is shown in [the corresponding notebook](notebooks/head_tilt_features.ipynb).

## Examples of processing pipelines on data samples
A few notebooks along with short data sequences are available in the [notebooks](notebooks) folder. These notebooks are designed to illustrate how the main analysis pipelines presented in the paper can be used on your own data but **not to replicate the exact panels of the article** (you can get in touch with me if you want more information, code for the full analysis pipelines including the preprocessing or a more complete dataset).

The [notebooks](notebooks) folder contains, in addition to a folder for the data samples:

- **[head_tilt_maps.ipynb](notebooks/head_tilt_maps.ipynb)**, code examples for estimating the gravitational component of 3-axis accelerometer data with [rfayat/madgwick_imu](https://github.com/rfayat/madgwick_imu),  generating head-tilt maps (i.e. histograms on the sphere) using [rfayat/angle_visualization](https://github.com/rfayat/angle_visualization) and fitting a von Mises-Fisher distribution on the result with [rfayat/SphereProba](https://github.com/rfayat/SphereProba).
- **[offset_computation.ipynb](notebooks/offset_computation.ipynb)**, code example for estimating accelerometer and gyroscope offsets from data corresponding to a multi-point tumble test using `IMU_Calibrator` from [imu_helpers.offset_computation](imu_helpers/offset_computation.py).
- **[head_tilt_features.ipynb](notebooks/head_tilt_features.ipynb)**, examples of a few IMU-based metrics for measuring the impact of a lesion on the animal's posture / behavior.

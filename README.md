# Inertial measurement of head tilt in rodents: principles and applications to vestibular research

This repository contains code examples and preprocessed data samples allowing to replicate the main analysis pipelines presented in **Fayat et al., 2021**, published in the [special issue dedicated to "Advances in Inertial Sensors" by the journal Sensors](https://www.mdpi.com/journal/sensors/special_issues/iertial_sensors).

If you use parts of this code in a scientific publication, please be kind enough to include a citation of the original paper:

```bibtex
Bibtex reference, to be done upon publication
```
## Installation
### Installation of the requirements

### Testing the installation

### Troubleshooting


## Code overview

### Independent packages
To ensure reproducibility, the modules written for this work were added as frozen submodules in their current states here but you can also feel free to have a look at or contribute to the respective corresponding repositories.

#### [rfayat/angle_visualization](https://github.com/rfayat/angle_visualization)
A few python tools for visualizing 3D angles, shapes and histograms on the unit sphere with matplotlib. This package was in particular developed for computing head tilt maps and allowing visualize them in 3D as well as projected in 2D using [cartopy](https://scitools.org.uk/cartopy/docs/latest/).

#### [rfayat/SphereProba](https://github.com/rfayat/SphereProba)
Fit and manipulate a few probability distribution functions on the unit S2 sphere. This packages was developed in particular for fitting a [von Mises-Fisher distribution](https://en.wikipedia.org/wiki/Von_Mises-Fisher_distribution) on the head tilt maps by computing the mean direction of the head tilt distribution on a triangulated sphere, weighted by the number of times the head tilt belonged to each one of the resulting facets.


#### [Mayitzin/ahrs](https://github.com/Mayitzin/ahrs) and its fork [rfayat/ahrs](https://github.com/rfayat/ahrs)
The [ahrs package](https://ahrs.readthedocs.io), developped by [Mayitzin](https://github.com/Mayitzin) is a great, extensive and amazingly documented collection of Attitude and Heading Reference Systems (AHRS) filters in pure python. Its vocation is more educational than focused on efficiency, resulting in a pure python implementation which makes it painfully slow for long times series (it is based on simple `for` loops over the time series for the iterative filters).

In order to perform the parameter optimization presented in the paper for the [Madgwick](https://ahrs.readthedocs.io/en/latest/filters/madgwick.html), [Mahony](https://ahrs.readthedocs.io/en/latest/filters/mahony.html) and [EKF](https://ahrs.readthedocs.io/en/latest/filters/ekf.html) filters in a reasonable amount of time given the size of the dataset (~1M data samples) while leveraging [ahrs](https://ahrs.readthedocs.io)'s great python API, the code for these filters was wrapped in a custom [numba jitclass](https://numba.pydata.org/numba-doc/latest/user/jitclass.html), enabling code compilation and thus sizeable shrinkage of the execution time, to the cost of adding an overhead to the computations (a bit more information,  execution time benchmarking, and also the reasons for not opening a pull request to [Mayitzin/ahrs](https://github.com/Mayitzin/ahrs), can be found [here](https://github.com/Mayitzin/ahrs/discussions/35)).

The resulting fork of ahrs can be found [here](https://github.com/rfayat/ahrs). However, even if wrapping [Mayitzin](https://github.com/Mayitzin)'s code in a  [numba jitclass](https://numba.pydata.org/numba-doc/latest/user/jitclass.html) perfectly fitted our needs for the analysis presented in this work (one-shot execution over a relatively large dataset), I would advise you **against using [rfayat/ahrs](https://github.com/rfayat/ahrs) for your routine analysis** as the [numba's jitclass](https://numba.pydata.org/numba-doc/latest/user/jitclass.html) feature is still experimental and the implemented wrappers were for instance broken by the latest updates of [numpy](https://numba.pydata.org/numba-doc/latest/user/jitclass.html).

#### [rfayat/madgwick_imu](https://github.com/rfayat/madgwick_imu)
This package consists in a Cython (i.e. compiled) implementation of the Madgwick filter, wrapped in [ahrs](https://ahrs.readthedocs.io/en/latest/filters/madgwick.html)'s API. It can be seen as an easy-to-install (with pip) and easy-to-use (with python) alternative to the [ahrs package](https://ahrs.readthedocs.io) for routine computation of the [Madgwick filter](https://ahrs.readthedocs.io/en/latest/filters/madgwick.html) with performance approaching low-level language implementations of the algorithm.


Some of the credit for this package goes to [ghyomm](https://github.com/ghyomm), who provided his custom Rcpp implementation used as a starting point for writting the Cython code as well as to the [original C++](https://github.com/xioTechnologies/Fusion) code from which this implementation derives.

### Additional code used for the analysis
#### Numerical optimization of accelerometer offset values
#### Detection of active/immobile periods
#### Extraction of features describing lesion-induced deficits


## Examples of processing pipelines on data samples
### Accelerometer and gyroscope offset computation
### Comparison of mocap and IMU-based head-tilt estimates
### Plotting Head-tilt maps
### IMU-extracted features describing lesion-induced deficits

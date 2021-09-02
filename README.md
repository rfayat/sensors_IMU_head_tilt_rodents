# Inertial measurement of head tilt in rodents: principles and applications to vestibular research

This repository contains code examples and preprocessed data samples allowing to replicate the main analysis pipelines presented in **Fayat et al., 2021**, published in the [special issue dedicated to "Advances in Inertial Sensors" by the journal Sensors](https://www.mdpi.com/journal/sensors/special_issues/iertial_sensors).

If you use parts of this code in a scientific publication, please be kind enough to include a citation of the original paper:

```bibtex
Bibtex reference, to be done upon publication
```
## Installation
### Installation of the requirements

### Testing the installation

### Troubleshooting


## Code overview

### Independent packages
To ensure reproducibility, the modules written for this work were added as frozen submodules in their current states here but you can also feel free to have a look at or contribute to the respective corresponding repositories.

#### [rfayat/angle_visualization](https://github.com/rfayat/angle_visualization)

#### [rfayat/SphereProba](https://github.com/rfayat/SphereProba)

#### [Mayitzin/ahrs](https://github.com/Mayitzin/ahrs) and its fork [rfayat/ahrs](https://github.com/rfayat/ahrs)

#### [rfayat/madgwick_imu](https://github.com/rfayat/madgwick_imu)

### Additional code used for the analysis
#### Numerical optimization of accelerometer offset values
#### Detection of active/immobile periods
#### Extraction of features describing lesion-induced deficits


## Examples of processing pipelines on data samples
### Accelerometer and gyroscope offset computation
### Comparison of mocap and IMU-based head-tilt estimates
### Plotting Head-tilt maps
### IMU-extracted features describing lesion-induced deficits

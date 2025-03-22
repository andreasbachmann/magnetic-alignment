# Pipeline to determine the body-axis of animals
This pipeline streamlines the calculation of body-axis for animals in specific segments of drone footage based on their exhibited behavioural bouts. It was developed for the bachelor thesis 'Exploring the alignment of the Grévy's Zebra, _Equus grevyi_, with Earth's magnetic field. A drone-based observational approach.'.
The raw data, numpy arrays containing UTC coordinates of every animal in every frame of drone footage, has been provided by X.

## orientation-calc.py
Calculates every individuals' orientation vector during specified behavioral bouts. Requires pandas, os, numpy and math libraries.

**Takes:**
- numpy array containing the UTC coordinates for every animal in every frame of the observation
- csv/excel file of what behavioural bouts can be observed at what timestamps in the observation
- csv/excel file of what frame of the array is the start/end time of the video to relate numpy array to video times

**Output:**
- excel file containing rows for every individuals orientation vector within the specified segments of the observations


## annotations.py
A script to account for the magnetic declination (obtained by using the [MagGeo Annotation Program](https://github.com/MagGeo/MagGeo#readme)).

**Input:**
- output of orientation-calc.py

**Output:**
- csv file containing the orientation data, but accounted for magnetic declination

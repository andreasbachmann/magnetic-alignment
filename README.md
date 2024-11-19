# Pipeline to determine the body-axis of animals. Developed for the bachelor thesis 'Exploring the alignment of the Grévy's Zebra, _Equus grevyi_, with Earth's magnetic field. A drone-based observational approach.'
This pipeline streamlines the calculation of body-axis for animals in specific segments of drone footage based on their exhibited behavioural bouts.


## orientation-calc.py
A script to calculate every individuals' orientation vector (for every n'th frame) within specified segments of identified behavior. Uses the pandas, os, numpy and math libraries.

**Input:**
- numpy array for an observation (:= coherent drone footage, an observation might span multiple videos) containing the UTC coordinates for every animal (at least 2 posture keypoints per animal) in every frame of the observation
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

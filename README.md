# Pipeline to determine the body-axis of animals. Developed for the bachelor thesis 'Exploring the alignment of the Grévy's Zebra, _Equus grevyi_, with Earth's magnetic field. A drone-based observational approach.'
This pipeline streamlines the calculation and analysis of body-axis for animals in specific segments of drone footage based on their exhibited behavioural bouts.


## orientation-calc.py
Script to calculate every individuals' orientation vector (for every n'th frame) within specified segments of identified behavior. Uses the pandas, os, numpy and math libraries.

**Input:**
- array for an observation (:= coherent drone footage) containing the UTC coordinates for every animal in every frame of the observation.
- csv/excel file of what behavioural bouts can be observed at what timestamps in the observation.
- csv/excel file of what frame of the array is the start/end time of the video observation to relate array to video times.

**Output:**
- excel file containing rows for every individuals orientation vector within the specified segments of the observations.


## annotations.py
Contains a script to account for the magnetic declination (obtained by using the [MagGeo Annotation Program](https://github.com/MagGeo/MagGeo#readme)). It writes this new dataframe into a new CSV file.

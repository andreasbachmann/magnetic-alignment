# Overview of code snippets used for the project
Short explanations for the code snippets used to complete the calculation and analysis of the project. 


## orientation-calc.py
Contains the script to calculate every individuals' orientation vector (for every n'th frame) within segments of identified behavior. Uses the pandas, os, numpy and math libraries.

**Input:** excel file containing video time and segment behavior information. 

**Output:** excel file containing rows for every individuals orientation vector within the specified segments of the observations.


## transformations.py
Contains a script to calculate additional data from the orientation (such as relating the orientation to north direction instead of east) and account for the magnetic declination (obtained by using the [MagGeo Annotation Program](https://github.com/MagGeo/MagGeo#readme)). It writes this new dataframe into a new CSV file.

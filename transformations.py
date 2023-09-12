import pandas as pd

#  load orientation data; contains orientation data processed from orientation-calc.py
df_orientation = pd.read_excel('excels/orientation_data_test.xlsx')

#  load declination data; contains magnetic declination data from an MagGeo Annotation Program
df_declination = pd.read_csv('excels/declination_data.csv')

#  create a dictionary to map video number to declination values (approxmiation)
observation_declination_dict = df_declination.set_index('video_id')['D'].to_dict()

#  calculate orientation with respect to geographic north (0-360 degrees)
df_orientation['orientation_north'] = (90 - df_orientation['orientation']) % 360

#  map declination values to the orientation dataframe based on observation ids
df_orientation['declination'] = df_orientation['observation'].map(observation_declination_dict)

#  calculate magnetic orientation by subtracting declination from geographic north orientation
df_orientation['magnetic_orientation'] = df_orientation['orientation_north'] - df_orientation['declination']

#  calculate axial orientation
df_orientation['axial_orientation'] = df_orientation['magnetic_orientation'] % 180

#  save the dataframe with annotated orientation data to a new csv file
df_orientation.to_csv('excels/annotated_orientation_data_test.csv', index=False)

import pandas as pd
import os
import numpy as np
import math

#   frames_df loads the first and last frames of the video at which its data array starts; to relate the defined sections of interest within the array with the video time
#   behavior_df loads the starting and ending times of the segments of observed behaviors within the videos
behavior_df = pd.read_excel('excels/behavior_segments.xlsx')
frames_df = pd.read_excel('excels/start_frames.xlsx')
dataframes = []
video_frame_rate = 60
numpy_frame_rate = 30

#  postural information (data array) for each observation
postures = np.load(f'posture_data_utms/observation{observation}-postures.npy')

#  for each row in the behavior_df (contains segment of determined behavior with start/end times)
for _, row in behavior_df.iterrows():

    #  get basic information
    n = 30
    observation, original_video_num = row['observation'].split('-')
    behavior = row['behavior']
    video_start_time = row['start']
    video_end_time = row['end']
    species = row['species']
    bout_id = observation + '.' + original_video_num.zfill(2)   

    #  for every video in the observation load the first and last frames into a dictionary
    video_first_frame_nums = {}
    video_last_frame_nums = {}
    for video_num in ['01', '02', '03']:
        frame_filter = frames_df['flight'] == f'ob{observation}-{video_num}'
        if frame_filter.any():  
            video_first_frame_nums[video_num] = frames_df.loc[frame_filter, 'first_frame'].iloc[0]
            if 'last_frame' in frames_df.columns and not frames_df.loc[frame_filter, 'last_frame'].isnull().all():
                video_last_frame_nums[video_num] = frames_df.loc[frame_filter, 'last_frame'].iloc[0]
            else:
                video_last_frame_nums[video_num] = None
        else:
            video_first_frame_nums[video_num] = None
            video_last_frame_nums[video_num] = None  

    #  relate the posture data array to the videos in case the observation spans multiple videos
    numpy_first_frame_num_02 = None
    numpy_first_frame_num_03 = None
    if video_first_frame_nums['01'] is not None and video_last_frame_nums['01'] is not None:
        numpy_first_frame_num_02 = int(((video_last_frame_nums['01'] - video_first_frame_nums['01']) / (video_frame_rate / numpy_frame_rate)) + 1)
    if video_first_frame_nums['01'] is not None and video_last_frame_nums['01'] is not None and video_first_frame_nums['02'] is not None and video_last_frame_nums['02'] is not None:
        numpy_first_frame_num_03 = int((((video_last_frame_nums['01'] - video_first_frame_nums['01']) + (video_last_frame_nums['02'] - video_first_frame_nums['02'])) / (video_frame_rate / numpy_frame_rate)) + 1)

    #  determine start and end frames in the numpy data array based on the video the behavior originates from
    if original_video_num == '01':
        start_frame = int((video_start_time * video_frame_rate - video_first_frame_nums[original_video_num]) / (video_frame_rate / numpy_frame_rate))
        end_frame = int((video_end_time * video_frame_rate - video_first_frame_nums[original_video_num]) / (video_frame_rate / numpy_frame_rate))
    elif original_video_num == '02':
        start_frame = int(((video_start_time * video_frame_rate - video_first_frame_nums[original_video_num]) / (video_frame_rate / numpy_frame_rate)) + numpy_first_frame_num_02)
        end_frame = int(((video_end_time * video_frame_rate - video_first_frame_nums[original_video_num]) / (video_frame_rate / numpy_frame_rate)) + numpy_first_frame_num_02)
    elif original_video_num == '03':
        start_frame = int(((video_start_time * video_frame_rate - video_first_frame_nums[original_video_num]) / (video_frame_rate / numpy_frame_rate)) + numpy_first_frame_num_03)
        end_frame = int(((video_end_time * video_frame_rate - video_first_frame_nums[original_video_num]) / (video_frame_rate / numpy_frame_rate)) + numpy_first_frame_num_03)
    else:
        print('Incorrect video number')

    #  function to calculate angle from east using tail and neck coordinates
    def angle_from_east(tail, neck):    
        delta_easting = neck[0] - tail[0]
        delta_northing = neck[1] - tail[1]
        angle_rad = math.atan2(delta_northing, delta_easting)
        angle_deg = math.degrees(angle_rad)
        return (angle_deg + 360) % 360

    #  extract neck and tail key points for every n'th frame within the array for the defined segment of interest
    neck_points = postures[:, start_frame:end_frame:n, 3]
    tail_points = postures[:, start_frame:end_frame:n, 8]

    #  calculate angles from east for each of those frames
    angles_from_east = [[round(angle_from_east(tail_points[i, j], neck_points[i, j]), 1) for j in range(tail_points.shape[1])] for i in range(tail_points.shape[0])]

    #  prepare data for df
    data = []
    for i, animal_angles in enumerate(angles_from_east):
        for j, angle in enumerate(animal_angles):
            if not math.isnan(angle):
                numpy_frame_num = start_frame + j * n
                frame_num = observation + '-' + str(numpy_frame_num)
                individual_id = observation + '-' + str(i)
                data.append([observation + '-' + original_video_num, bout_id, behavior, species, individual_id, frame_num, angle])

    #  create df with orientations and all relevant information for the current behavior segment and add to the list
    df = pd.DataFrame(data, columns=['observation', 'bout_id', 'behavior', 'species', 'individual_id', 'frame_num', 'orientation'])
    dataframes.append(df)

#  combine all dfs in the list
df_combined = pd.concat(dataframes)

#  save the combined df to an excel file; if file already exists, combine and save
output_filename = 'excels/orientation_data.xlsx'

if os.path.exists(output_filename):
    df_existing = pd.read_excel(output_filename, dtype=np.object_)
    df_combined = pd.concat([df_existing, df_combined])
    duplicates = df_combined[df_combined.duplicated(keep='last')]
    df_combined.to_excel(output_filename, index=False)
else:
    df_combined.to_excel(output_filename, index=False)

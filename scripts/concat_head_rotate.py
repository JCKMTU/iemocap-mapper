import os
import tf
import csv
import sys
import numpy as np

iemo_dir = './IEMOCAP_full_release/'
combined_dir = './IEMOCAP_train_data/'
retargeted_dir = './MOCAP_retargeted/'

if not os.path.exists(retargeted_dir):
    print 'retargeted csv files missing.'
    sys.exit(1)

if not os.path.exists(combined_dir):
    os.mkdir(combined_dir)

sessions = [dirname for dirname in os.listdir(iemo_dir) if dirname.startswith('Session')]
sessions.sort()

for session in sessions:
    if not os.path.exists(retargeted_dir + '/' + session + '/'):
        print 'could not find %r in retargeted dir. Skipping...' % session
    else:
        session_dir = iemo_dir + '/' + session + '/dialog/MOCAP_head/'
        head_files = [f for f in os.listdir(session_dir) if f.endswith('.txt')]
        head_files.sort()

        if not os.path.exists(combined_dir + session + '/'):
            os.mkdir(combined_dir + session + '/')

        for file in head_files:
            file_name = file.split('.')[0]

            # Open MOCAP_head data
            head_data = np.loadtxt(iemo_dir + session + '/dialog/MOCAP_head/' + file, delimiter=' ', skiprows=2)
            head_frames = len(head_data)

            # Open MOCAP_rotated data
            rota_data = np.loadtxt(retargeted_dir + session + '/' + file_name + '.txt.c3d.csv', delimiter=',', skiprows=0)
            rota_frames = len(rota_data)

            assert head_frames == rota_frames, "Frame count doe not much"

            # Open file to be written
            comb_file = open(combined_dir + session + '/' + file_name + '.dat', 'w')
            writer = csv.writer(comb_file, delimiter=',')

            for frame in range(head_frames):
                roll = np.deg2rad(head_data[frame][2])
                pitch = np.deg2rad(-head_data[frame][4])
                yaw = np.deg2rad(head_data[frame][3])
                quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

                row = [0] * 14
                row[0] = quaternion[0]
                row[1] = quaternion[1]
                row[2] = quaternion[2]
                row[3] = quaternion[3]

                row_data = rota_data[frame] * .01
                row_data = np.minimum(1.0, row_data)
                row_data = np.delete(row_data, np.s_[13:27], axis=0)

                row = np.append(row, row_data)
                writer.writerow(row)

            print file_name, 'completed.'
            comb_file.close()

import os
import csv
import sys


EMOTIONS ={'neu': 'Neutral',
           'ang': 'Anger',
           'fru': 'Frustration',
           'sad': 'Sadness',
           'sur': 'Surprise',
           'exc': 'Excited',
           'hap': 'Happy',
           'fea': 'Fearful',
           'dis': 'Disgusted',
           'oth': 'Other',
           'xxx': 'Undefined'}


try:
    input_dir = sys.argv[1]
except:
    print 'Specify iemocap home directory.'
    sys.exit(1)

try:
    output_dir = sys.argv[2]
except:
    print "Output directory is not specified."
    output_dir = './IEMOCAP_train_data/'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    print "Folder 'emo_csv' is created."

# There are 5 sessions in total in iemocap data.
sessions = [dirname for dirname in os.listdir(input_dir) if dirname.startswith('Session')]
sessions.sort()

prev_emotion = 'neu'
curr_emotion = 'neu'

print sessions
for session in sessions:

    if not os.path.exists(output_dir + '/' + session):
        os.mkdir(output_dir + '/' + session)
    # Obtain directories for necessary files.
    emo_eval_dir = input_dir + '/' + session + '/dialog/EmoEvaluation/'
    mocap_sess_dir = input_dir + '/' + session + '/dialog/MOCAP_rotated/'

    emo_eval_files = [f for f in os.listdir(emo_eval_dir) if f.endswith('.txt')]
    emo_eval_files.sort()
    print 'Looking up', session, '...'

    for i in emo_eval_files:
        emo_eval_fd = open(emo_eval_dir + i)
        emo_eval_data = list(emo_eval_fd)[2:]

        if not os.path.exists(mocap_sess_dir + i):
            print 'Could not find', mocap_sess_dir + i
        else:
            total_frames = sum(1 for row in open(mocap_sess_dir + i)) - 2
            print total_frames



            # Create new csv file
            emo_csv_fd = open(output_dir + '/' + session + '/' + i.split('.')[0] + '.emo', 'w')
            writer = csv.writer(emo_csv_fd)

            current_pos = 0 # Current position in file
            # Trim emo_eval_data to extract time intervals and emotion
            for line in emo_eval_data:
                if line.startswith('['):
                    line = line.split('\t')

                    # Get start frame and end frame of sentences
                    time = line[0].split(' - ')

                    s_frame = float(time[0].replace('[', '')) * 120
                    e_frame = float(time[1].replace(']', '')) * 120

                    s_frame = int(s_frame)
                    e_frame = int(e_frame)

                    # Get emo
                    prev_emotion = curr_emotion
                    curr_emotion = line[2]


                    inbetween_frame = (s_frame - current_pos) / 2
                    while inbetween_frame > current_pos:
                        writer.writerow([EMOTIONS[prev_emotion]])
                        current_pos += 1

                    while  e_frame > current_pos:
                        writer.writerow([EMOTIONS[curr_emotion]])
                        current_pos += 1

            inbetween_frame = (total_frames - current_pos) / 2
            while inbetween_frame > current_pos:
                writer.writerow([EMOTIONS[curr_emotion]])
                current_pos += 1

            while total_frames > current_pos:
                writer.writerow([EMOTIONS['neu']])
                current_pos += 1

            prev_emotion = 'neu'
            curr_emotion = 'neu'
            emo_csv_fd.close()
        emo_eval_fd.close()
        print i, 'completed.'

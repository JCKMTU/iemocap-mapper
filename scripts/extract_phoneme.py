import os
import sys
import csv

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
    print "Folder 'IEMOCAP_train_data' is created."

# There are 5 sessions in total in iemocap data.
sessions = [dirname for dirname in os.listdir(input_dir) if dirname.startswith('Session')]
sessions.sort()

for session in sessions:
    if not os.path.exists(output_dir + '/' + session):
        os.mkdir(output_dir + '/' + session)

    dat_dir = input_dir + session + '/dialog/MOCAP_rotated/'
    emo_dir = input_dir + session + '/dialog/EmoEvaluation/'
    pho_dir = input_dir + session + '/sentences/ForcedAlignment/'

    file_list = os.listdir(emo_dir)
    for _ in file_list:
        if _.endswith('.txt'):
            name = os.path.splitext(_)[0]

            emo_fd = open(emo_dir + _, 'r')
            emo_data = list(emo_fd)
            emo_data = emo_data[2:]

            if os.path.exists(dat_dir + _):
                mocap_fd = open(dat_dir + _, 'r')
                mocap_data = list(mocap_fd)
                frames = len(mocap_data) - 2

                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)

                if not os.path.exists(output_dir + session + '/'):
                    os.mkdir(output_dir + session + '/')

                ph_fd = open(output_dir + session + '/' + name + '.pho', 'w')
                writer = csv.writer(ph_fd)

                current_pos = 0
                for line in emo_data:
                    if line.startswith('['):
                        line = line.split('\t')

                        time = line[0].split(' - ')
                        start = float(time[0].replace('[', '')) * 120
                        end = float(time[1].replace(']', '')) * 120

                        start = int(start)
                        end = int(end)

                        while start > current_pos:
                            writer.writerow(['SIL', 'SIL', 'SIL', 'SIL'])
                            current_pos += 1

                        file_name = line[1]

                        if not os.path.exists(pho_dir + name + '/' + file_name + '.phseg'):
                            print 'Could not find', pho_dir + name + '/' + file_name + '.phseg'
                            print 'Filling with SIL...'
                        else:
                            phseg_fd = open(pho_dir + name + '/' + file_name + '.phseg')
                            phseg_data = list(phseg_fd)
                            phseg_data = phseg_data[2:-1]
                            for each in phseg_data:
                                each = each.replace('\t', '')
                                sframe = int(each[2:5])
                                eframe = int(each[8:11])
                                phone = each[22:].replace('\n', '')
                                phone = phone.split(' ')
                                while start + eframe > current_pos:
                                    if len(phone) == 1:
                                        writer.writerow([phone[0],phone[0],phone[0],phone[0]])
                                    else:
                                        writer.writerow(phone)
                                    current_pos += 1
                                    phseg_fd.close()
                while current_pos < frames:
                    writer.writerow(['SIL', 'SIL', 'SIL', 'SIL'])
                    current_pos += 1
                ph_fd.close()
            else:
                print dat_dir + _, "does not exist. skipping...."

            emo_fd.close()
            mocap_fd.close()

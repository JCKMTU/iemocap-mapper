import sys
import c3d
import numpy as np

input_filename = sys.argv[1]
output_filename = input_filename.split(".")[1] + ".c3d"

# Get the labels from the first line in the file
line = open(input_filename).readline()
labels = line[:-2].split(" ")[2:]

# Left pad them for C3D writer
aligned = []
for label in labels:
    aligned.append(label.ljust(8))
labels = aligned

# Load the data
data = np.genfromtxt(input_filename, skip_header=2)
# Invert all coordinates...
data = 1 - data

# Pad with two zero columns per point for error and nr_cams
reshaped_data = data[:,2:].reshape([-1,55,3])
padding_data = np.zeros([reshaped_data.shape[0],55,2])
points = np.concatenate([reshaped_data,padding_data], axis=2)

# Write the file
writer = c3d.Writer()

for frame in points:
    writer.add_frames([frame])

with open(output_filename, 'wb') as h:
    writer.write(h, labels)

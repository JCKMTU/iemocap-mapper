import c3d
import numpy as np


"""
set point rate (1200)


"""
line = open('data.csv').readline()
labels = line[:-2].split(" ")[2:]

plonk = []

for hu in labels:
    plonk.append(hu.ljust(8))

labels = plonk

data = np.genfromtxt("./data.csv", skip_header=2)

data = 1 - data

foo = data[:,2:].reshape([-1,55,3])
bar = np.zeros([foo.shape[0],55,2])

yolo = np.concatenate([foo,bar], axis=2)

swag = yolo.reshape([foo.shape[0],-1])

writer = c3d.Writer()

for frame in yolo:
    writer.add_frames([frame])

with open('conv-points.c3d', 'wb') as h:
    writer.write(h, labels)

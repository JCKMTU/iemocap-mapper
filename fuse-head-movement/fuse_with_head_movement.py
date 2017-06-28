import numpy as np
import tf

shpkeys = np.loadtxt("./blender-output.csv", delimiter=",")

data = np.genfromtxt("./data.csv", skip_header=2)

angles = data[:,2:5]
quaternions = []


for frame in angles:
   """
    frame is     pitch roll yaw in deg
    func takes   roll pitch yaw in rad

    THIS IS UNTESTED AND PROBABLY WRONG.
   """
   roll = np.deg2rad(-frame[1])
   pitch = np.deg2rad(-frame[0])
   yaw = np.deg2rad(frame[2])
   quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
   quaternions.append([quaternion[0],quaternion[1],quaternion[2],quaternion[3]])


print len(quaternions)

print len(shpkeys)

output = np.concatenate([quaternions, shpkeys[1:,4:]], axis=1)
print output.shape
np.savetxt("output.csv", output, delimiter=",")

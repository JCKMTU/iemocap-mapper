import numpy as np

input_dir = [{ 'x': 0, 'y': 1, 'z': 1}, { 'x': 1, 'y': 2, 'z': 2}]
# output_dir

# Shapekeys and blender position
shapekey_list = []

for _in in input_dir:
    tmp_list = []
    for _cord in _in:
        #tmp_list.append(_in[_cord])
        shapekey_list.append(_in[_cord])
    #shapekey_list.append(tmp_list)
print(shapekey_list)

# Weights and biases with random values in normal distribution
mean, variance = 0, 1
weights = np.random.normal(loc=mean, scale=np.sqrt(variance), size=len(shapekey_list))
biases = np.random.normal(loc=mean, scale=np.sqrt(variance), size=len(shapekey_list))

# Calculate sum(shapekey_i * weights_i) + bias
output = np.add(np.matmul(shapekey_list, weights), biases)

# Apply activation function
#output = np.relu(output)
output = output * (output > 0)

# Sum of array in given axis
output = np.sum(output)

# Fitness function
#fitness = np.sqrt(np.pow(shapekeys - blender_pos, 2))

print output

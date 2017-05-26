import numpy as np

# input_dir
# output_dir

# Shapekeys and blender position
shapekeys = []
blender_pos = []

# Weights and biases with random values in normal distribution
mean, variance = 0, 1
weights = np.random.normal(loc=mean, scale=np.sqrt(variance), size=20)
biases = np.random.normal(loc=mean, scale=np.sqrt(variance), size=20)

# Calculate sum(shapekey_i * weights_i) + bias
output = np.add(np.matmul(shapekeys, weights), biases)

# Apply activation function
output = np.relu(output)

# Sum of array in given axis
#output = np.sum(output)

# Fitness function
fitness = np.sqrt(np.pow(shapekeys - blender_pos, 2))

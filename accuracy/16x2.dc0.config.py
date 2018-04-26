from collections import namedtuple

__all__ = ['configuration']

Config = namedtuple('Config', ['block_sizes', 'pruning_rates'])

configuration = {
    "vgg16": Config(
        block_sizes=[
            (16, 1, 0, 0), (16, 2, 0, 0), # conv1
            (16, 2, 0, 0), (16, 2, 0, 0), # conv2
            (16, 2, 0, 0), (16, 2, 0, 0), (16, 2, 0, 0), # conv3
            (16, 2, 0, 0), (16, 2, 0, 0), (16, 2, 0, 0), # conv4
            (16, 2, 0, 0), (16, 2, 0, 0), (16, 2, 0, 0), # conv5
            (16, 16), (16, 16), (16, 20) # fc
        ],
        pruning_rates = [
            0.42, 0.78, # conv1
            0.66, 0.64, # conv2
            0.47, 0.76, 0.58, # conv3
            0.68, 0.78, 0.66, # conv4
            0.65, 0.71, 0.64, # conv5
            0.96, 0.96, 0.77, # fc
        ]
    )
}
            
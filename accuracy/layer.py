import torch
import torch.nn as nn
from torch.nn.parameter import Parameter
from torch.nn import functional as F

from compress import blocksparse

class BlocksparseConv(nn.Module):
    def __init__(self, conv2d, block_sizes, pruning_rate):
        super(BlocksparseConv, self).__init__()

        self.block_sizes = block_sizes
        self.pruning_rate = pruning_rate

        self.in_channels = conv2d.in_channels
        self.out_channels = conv2d.out_channels
        self.kernel_size = conv2d.kernel_size
        self.stride = conv2d.stride
        self.padding = conv2d.padding
        self.dilation = conv2d.dilation
        self.transposed = conv2d.transposed
        self.output_padding = conv2d.output_padding
        self.groups = conv2d.groups
        
        self.weight = Paramater(conv2d.weight.data)
        if conv2d.bias:
            self.bias = Parameter(conv2d.bias.data)
        else:
            self.register_parameter('bias', None)

        self.orders, self.mask = blocksparse(self.weight.data.numpy(), block_sizes, pruning_rate)
        self.mask = torch.from_numpy(self.mask)

    def forward(x):
        weight = self.weight * self.mask
        return F.conv2d(x, weight, self.bias, self.stride, self.padding, self.dilation, self.groups)


class BlocksparseLinear(nn.Module):
    def __init__(self, linear, block_size, pruning_rate):
        super(BlocksparseLinear, self).__init__()
        
        self.block_sizes = block_sizes
        self.pruning_rate = pruning_rate

        self.in_features = linear.in_features
        self.out_features = linear.out_features
        self.weight = Parameter(linear.weight.data)
        if linear.bias:
            self.bias = Parameter(linear.bias.data)
        else:
            self.register_parameter('bias', None)

        self.orders, self.mask = blocksparse(self.weight.data.numpy(), block_sizes, pruning_rate)
        self.mask = torch.from_numpy(self.mask)

    def forward(x):
        weight = self.weight * self.mask
        return F.linear(x, self.weight, self.bias)
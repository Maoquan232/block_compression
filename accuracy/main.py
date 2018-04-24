import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models


from layer import BlocksparseConv, BlocksparseLinear

class BlocksparseModel(nn.Module):
    def __init__(self, model, block_sizes, pruning_rates):
        super(BlocksparseModel, self).__init__()

        features = []
        sparse_index = 0
        for layer in model.features:
            if type(layer) is nn.Conv2d:
                features.append(BlocksparseConv(layer, block_sizes[sparse_index], pruning_rates[sparse_index]))
                sparse_index += 1
            else:
                features.append(layer)

        classifier = []
        for layer in model.classifier:
            if type(layer) is nn.Linear:
                classifier.append(BlocksparseLinear(layer, block_sizes[sparse_index], pruning_rates[sparse_index]))
                sparse_index += 1
            else:
                classifier.append(layer)

        self.features = nn.Sequential(*features)
        self.classifier = nn.Sequential(*classifier)

    def forward(self, x):
        f = self.features(x)
        f = f.view(f.size(0), -1)
        y = self.classifier(f)
        return y

block_sizes = [
    (0, 0, 16, 128), (0, 0, 16, 128), # conv1
    (0, 0, 16, 128), (0, 0, 16, 128), # conv2
    (0, 0, 16, 128), (0, 0, 16, 128), (0, 0, 16, 128), # conv3
    (0, 0, 16, 128), (0, 0, 16, 128), (0, 0, 16, 128), # conv4
    (0, 0, 16, 128), (0, 0, 16, 128), (0, 0, 16, 128), # conv5
    (128, 128), (128, 128), # fc
]

pruning_rate = [
    0.4, 0.5,
    0.5, 0.5, 
    0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    0.7, 0.7
]

model = models.vgg16(pretrained=True)
sparse_model = BlocksparseModel(model, block_sizes, pruning_rates)

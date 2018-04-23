import torch
import sys
import time

# cudnn is tooooo fast!! it has too many in house optimization. we use cublas as baseline
torch.backends.cudnn.enabled = False

batch_size = 256
image_width = 28 
image_height = 28 
input_channel = 512 
output_channel = 512 
kernel_width = 3 
kernel_height = 3 
times = 10

conv = torch.nn.Conv2d(input_channel, output_channel, kernel_size=(kernel_width, kernel_height), stride=(1, 1), padding=(kernel_width/2, kernel_height/2)).cuda()
x = torch.autograd.Variable(torch.randn(batch_size, input_channel, image_width, image_height)).cuda()
# run once for initialization overhead
y = conv(x)
torch.cuda.synchronize()
begin = time.time()
for i in range(times):
    y = conv(x)
torch.cuda.synchronize()
end = time.time()

print((end - begin) / times)


import imageio
import os

fileList = []
for file in os.listdir('output/'):
    complete_path = 'output/' + file
    fileList.append(complete_path)
    kargs = {'macro_block_size': 1}
    writer = imageio.get_writer('test.mp4', fps=10, **kargs)

for im in fileList:
    writer.append_data(imageio.imread(im))
writer.close()



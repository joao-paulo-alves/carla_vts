import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import math
from sklearn.preprocessing import scale

fig, ax1 = plt.subplots()

# ax = fig.add_subplot(111)

f = open("KeyFrameTrajectory.txt", "r")
lines = f.readlines()
resultx = []
resulty = []
resultz = []
for x in lines:
    resultx.append(x.split(' ')[1])
    resulty.append(x.split(' ')[3])
    #resultz.append(x.split(',')[2])
f.close()


resultx = numpy.asarray(resultx).astype(numpy.float)
resulty = numpy.asarray(resulty).astype(numpy.float)
fresultx = resultx - numpy.mean(resultx)
fresulty = resulty - numpy.mean(resulty)

plt.plot(resultx, resulty, color="g")
plt.axis('equal')



f = open("GT_coordinates.txt", "r")
lines = f.readlines()
resultx = []
resulty = []
resultz = []
for x in lines:
    resultx.append(x.split(',')[0])
    resulty.append(x.split(',')[1])
    #resultz.append(x.split(',')[2])
f.close()

resultx = numpy.asarray(resultx).astype(numpy.float)
resulty = numpy.asarray(resulty).astype(numpy.float)
fresultx = resultx - numpy.mean(resultx)
fresulty = resulty - numpy.mean(resulty)

plt.plot(resultx, resulty, color="r")
plt.axis('equal')

plt.show()

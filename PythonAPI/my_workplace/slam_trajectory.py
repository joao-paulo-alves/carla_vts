import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import math
from sklearn.preprocessing import minmax_scale

fig, (ax1, ax2) = plt.subplots(2)

# ax = fig.add_subplot(111)

f = open("GT_coordinates.txt", "r")
lines = f.readlines()
resultx = []
resulty = []
resultz = []
for x in lines:
    resultx.append(x.split(',')[1])
    resulty.append(x.split(',')[2])
    #resultz.append(x.split(',')[2])
f.close()

resultx = numpy.asarray(resultx).astype(numpy.float)
resulty = numpy.asarray(resulty).astype(numpy.float)

min_x = min(resultx)
max_x = max(resultx)

min_y = min(resulty)
max_y = max(resulty)

print(len(resultx))

fresultx = resultx - numpy.mean(resultx)
fresulty = resulty - numpy.mean(resulty)

ax1.plot(resultx, resulty, color="r")
ax1.axis('equal')

# f = open("KeyFrameTrajectory.txt", "r")
# lines = f.readlines()
# resultx = []
# resulty = []
# resultz = []
# for x in lines:
#     resultx.append(x.split(' ')[1])
#     resulty.append(x.split(' ')[3])
#     #resultz.append(x.split(',')[2])
# f.close()


print(len(resultx))
resultx = numpy.asarray(resultx).astype(numpy.float)
resulty = numpy.asarray(resulty).astype(numpy.float)

# resultx = minmax_scale(resultx, feature_range=(min_x,max_x))
# resulty = minmax_scale(resulty, feature_range=(min_y,max_y))

fresultx = resultx - numpy.mean(resultx)
fresulty = resulty - numpy.mean(resulty)

# resultx = resultx[-300:]
# resulty = resulty[-300:]
ax2.plot(resultx, resulty, color="g")
ax2.axis('equal')






plt.show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import math
from sklearn.preprocessing import scale

fig, ax1 = plt.subplots()

# ax = fig.add_subplot(111)

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

# for x in range(len(fresultx)):


# f = open("KeyFrameTrajectory1.txt", "r")
# lines = f.readlines()
# resultx = []
# resulty = []
# resultz = []
# for x in lines:
#     resultx.append(x.split()[1])
#     resultz.append(x.split(' ')[3])
#
# f.close()

# resultx = numpy.asarray(resultx).astype(numpy.float)
# resultz = numpy.asarray(resultz).astype(numpy.float)
# rresultx = resultx - numpy.mean(resultx)
# rresultz = resultz - numpy.mean(resultz)

# x = numpy.arange(0, math.pi,0.01)
# y= numpy.sin(x)
# z = numpy.cos(x)
#
# rresultx = scale(rresultx, axis=0, with_mean=True, with_std=True, copy=True)
# rresultz = scale(rresultz, axis=0, with_mean=True, with_std=True, copy=True)
# fresultx = scale(fresultx, axis=0, with_mean=True, with_std=True, copy=True)
# fresultz = scale(fresultz, axis=0, with_mean=True, with_std=True, copy=True)

plt.plot(resultx, resulty, color="r")
plt.axis('equal')


# plt.plot(rresultx, rresultz,color="b", marker='o')


# color = 'tab:red'
# ax1.set_xlabel('X-axis')
# ax1.set_ylabel('Y1-axis', color=color)
# ax1.plot(rresultx, fresultz, color=color)
# ax1.tick_params(axis='y', labelcolor=color)
#
# # Adding Twin Axes to plot using dataset_2
# ax2 = ax1.twinx()
#
# color = 'tab:green'
# ax2.set_ylabel('Y2-axis', color=color)
# ax2.plot(rresultx, rresultz, color=color)
# ax2.tick_params(axis='y', labelcolor=color)
#
# # Adding title
# plt.title('Use different y-axes on the left and right of a Matplotlib plot', fontweight="bold")

# Show plot
plt.show()

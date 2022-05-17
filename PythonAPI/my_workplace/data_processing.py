import math
import numpy


class Quaternions:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z


class Euler:
    def __init__(self, yaw, roll, pitch):
        self.yaw = yaw
        self.roll = roll
        self.pitch = pitch


class Data:
    def __init__(self, x, y, z, yaw, roll, pitch):
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.roll = roll
        self.pitch = pitch


class Norm:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


f = open("KeyFrameTrajectory.txt", "r")

lines = f.readlines()
q_result = []
e_result = []
time = []
orb_data = []

for c,i in enumerate(lines):
    q_result.append(
        Quaternions(float(i.split(' ')[4]), float(i.split(' ')[5]), float(i.split(' ')[6]), float(i.split(' ')[7])))
    time.append(float(i.split(' ')[0]))

    x1 = float(i.split(' ')[1])
    y1 = float(i.split(' ')[2])
    z1 = float(i.split(' ')[3])

    w = float(i.split(' ')[4])
    x = float(i.split(' ')[5])
    y = float(i.split(' ')[7])
    z = float(i.split(' ')[6])

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.degrees(math.atan2(t3, t4))

    e_result.append(Euler(yaw_z, roll_x, pitch_y))
    orb_data.append(Data(x1, y1, z1, yaw_z,
                         pitch_y, roll_x))
    print(yaw_z, pitch_y, roll_x, time[c])


f.close()

f = open("GT_coordinates.txt", "r")
new_f = open("new_GT.txt", "w")
lines = f.readlines()
gt_data = []

for x in lines:
    for y in time:
        if float(x.split(',')[0]) == y:
            new_f.write("%s" % x)
            gt_data.append(
                Data(float(x.split(',')[1]), float(x.split(',')[2]), float(x.split(',')[3]), float(x.split(',')[4]),
                     float(x.split(',')[5]), float(x.split(',')[6])))

f.close()
new_f.close()

gt_norm = []
orb_norm = []

elapsed_distance_gt = 0
elapsed_distance_orb = 0
scale_factor = 0

for i in gt_data:
    vector = numpy.array([i.x, i.y, i.z])
    elapsed_distance_gt += numpy.linalg.norm(vector)


for i in orb_data:
    vector = numpy.array([i.x, i.y, i.z])
    elapsed_distance_orb += numpy.linalg.norm(vector)

scale_factor = elapsed_distance_gt/elapsed_distance_orb

for c, i in enumerate(orb_data):
    orb_data[c] = Data(i.x * scale_factor, i.y * scale_factor, i.z * scale_factor, i.yaw, i.roll, i.pitch)


import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(2)

ax1.plot([i.x for i in orb_data], [i.z for i in orb_data], color="r")
ax1.axis('equal')

ax2.plot([i.x for i in gt_data], [i.y for i in gt_data], color="g")
ax2.axis('equal')

plt.show()

# print("%f || %f" % (gt_norm[1].y, orb_norm[1].y))

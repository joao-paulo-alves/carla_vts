import math
import numpy


class Quaternions:
    def __init__(self, x, y, z, w):
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
# i = 0

for x in lines:
    q_result.append(
        Quaternions(float(x.split(' ')[4]), float(x.split(' ')[5]), float(x.split(' ')[6]), float(x.split(' ')[7])))
    time.append(float(x.split(' ')[0]))
    x1 = float(x.split(' ')[1])
    y1 = float(x.split(' ')[2])
    z1 = float(x.split(' ')[3])
    y = float(x.split(' ')[6])
    z = float(x.split(' ')[7])
    w = float(x.split(' ')[4])
    x = float(x.split(' ')[5])

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

    # print("%s, %f, %f, %f \n" % (time[i], yaw_z, pitch_y, roll_x))
    # i = i + 1

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

for x in gt_data:
    vector = numpy.array([x.x, x.y, x.z])
    unit_vector = vector / numpy.linalg.norm(vector)
    gt_norm.append(Norm(unit_vector[0],unit_vector[1],unit_vector[2]))

for x in orb_data:
    vector = numpy.array([x.x, x.y, x.z])
    unit_vector = vector / numpy.linalg.norm(vector)
    orb_norm.append(Norm(unit_vector[0],unit_vector[1],unit_vector[2]))


print("%f || %f" % (gt_norm[1].y,orb_norm[1].y))
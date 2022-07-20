import math
from copy import deepcopy

import numpy
import numpy as np
from scipy.spatial.transform import Rotation as R

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


class Error:
    def __init__(self, first_frame, r_err, t_err, l, s):
        self.first_frame = first_frame
        self.r_err = r_err
        self.t_err = t_err
        self.len = l
        self.speed = s


f = open("KeyFrameTrajectory.txt", "r")

lines = f.readlines()
q_result = []
e_result = []
time = []
orb_data = []

for c, i in enumerate(lines):
    q_result.append(
        Quaternions(float(i.split(' ')[4]), float(i.split(' ')[5]), float(i.split(' ')[6]), float(i.split(' ')[7])))
    time.append(float(i.split(' ')[0]))

    x1 = float(i.split(' ')[1])
    y1 = float(i.split(' ')[3])
    z1 = float(i.split(' ')[2])

    w = float(i.split(' ')[4])
    x = float(i.split(' ')[5])
    y = float(i.split(' ')[6])
    z = float(i.split(' ')[7])

    t0 = +2.0 * (w * z + x * y)
    t1 = +1.0 - 2.0 * (z * z + x * x)
    roll_x = math.atan2(t0,t1)

    t2 = +2.0 * (w * x - y * z)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * x + z * y)
    t4 = +1.0 - 2.0 * (y * y + x * x)
    yaw_z = math.atan2(t3,t4)
    r = R.from_quat([w, y, z, x])
    xyz = r.as_euler('zyx', degrees=True)
    e_result.append(Euler(yaw_z, roll_x, pitch_y))
    orb_data.append(Data(x1, y1, z1, xyz[0],
                         xyz[1], xyz[2]))
    # print(yaw_z, pitch_y, roll_x, time[c])


f.close()

f = open("GT_coordinates.txt", "r")
new_f = open("new_GT.txt", "w")
lines = f.readlines()
gt_data = []

for i in lines:
    for j in time:
        if float(i.split(',')[0]) == j:
            new_f.write("%s" % i)
            gt_data.append(
                Data(float(i.split(',')[1]), float(i.split(',')[2]), float(i.split(',')[3]), float(i.split(',')[4]),
                     0, 0))
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

scale_factor = elapsed_distance_gt / elapsed_distance_orb

for c, i in enumerate(orb_data):
    orb_data[c] = Data(i.x * scale_factor, i.y * scale_factor, i.z * scale_factor, i.yaw, i.roll, i.pitch)

new_f = open("new_orb.txt", "w")
for i in orb_data:
    new_f.write("%f, %f, %f, %f, %f, %f\n" % (i.x, i.y, i.z, i.yaw, i.roll, i.pitch))
new_f.close()

gt_rot_mat = numpy.zeros((4, 4))
gt_rot_mat[3][3] = 1
orb_rot_mat = numpy.zeros((4, 4))
orb_rot_mat[3][3] = 1
orb_collector = []
gt_collector = []

for c, i in enumerate(gt_data):
    gt_rot_mat_new = deepcopy(gt_rot_mat)
    gt_rot_mat_new[0][0] = 1#math.cos(i.pitch) * math.cos(i.yaw)
    gt_rot_mat_new[0][1] = 0#math.sin(i.roll) * math.sin(i.pitch) * math.cos(i.yaw) - math.cos(i.roll) * math.sin(i.yaw)
    gt_rot_mat_new[0][2] = 0#math.cos(i.roll) * math.sin(i.pitch) * math.cos(i.yaw) + math.sin(i.roll) * math.sin(i.yaw)
    gt_rot_mat_new[0][3] = i.x
    gt_rot_mat_new[1][0] = 0#math.cos(i.pitch) * math.sin(i.yaw)
    gt_rot_mat_new[1][1] = 1#math.sin(i.roll) * math.sin(i.pitch) * math.sin(i.yaw) + math.cos(i.roll) * math.cos(i.yaw)
    gt_rot_mat_new[1][2] = 0#math.cos(i.roll) * math.sin(i.pitch) * math.sin(i.yaw) - math.sin(i.roll) * math.cos(i.yaw)
    gt_rot_mat_new[1][3] = i.y
    gt_rot_mat_new[2][0] = 0#(-1) * math.sin(i.pitch)
    gt_rot_mat_new[2][1] = 0#math.sin(i.roll) * math.cos(i.pitch)
    gt_rot_mat_new[2][2] = 1#math.cos(i.roll) * math.cos(i.pitch)
    gt_rot_mat_new[2][3] = 0
    gt_collector.append(gt_rot_mat_new)

for c, i in enumerate(orb_data):
    orb_rot_mat_new = deepcopy(orb_rot_mat)
    orb_rot_mat_new[0][0] = 1#math.cos(i.pitch) * math.cos(i.yaw)
    orb_rot_mat_new[0][1] = 0#math.sin(i.roll) * math.sin(i.pitch) * math.cos(i.yaw) - math.cos(i.roll) * math.sin(i.yaw)
    orb_rot_mat_new[0][2] = 0#math.cos(i.roll) * math.sin(i.pitch) * math.cos(i.yaw) + math.sin(i.roll) * math.sin(i.yaw)
    orb_rot_mat_new[0][3] = i.x
    orb_rot_mat_new[1][0] = 0#math.cos(i.pitch) * math.sin(i.yaw)
    orb_rot_mat_new[1][1] = 1#math.sin(i.roll) * math.sin(i.pitch) * math.sin(i.yaw) + math.cos(i.roll) * math.cos(i.yaw)
    orb_rot_mat_new[1][2] = 0#math.cos(i.roll) * math.sin(i.pitch) * math.sin(i.yaw) - math.sin(i.roll) * math.cos(i.yaw)
    orb_rot_mat_new[1][3] = i.y
    orb_rot_mat_new[2][0] = 0#(-1) * math.sin(i.pitch)
    orb_rot_mat_new[2][1] = 0#math.sin(i.roll) * math.cos(i.pitch)
    orb_rot_mat_new[2][2] = 1#math.cos(i.roll) * math.cos(i.pitch)
    orb_rot_mat_new[2][3] = 0
    orb_collector.append(orb_rot_mat_new)
# ________________Evaluation__________________
err = []
step_size = 10
#length = [25,50, 75, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500, 600, 700, 800]
length = [50,100,150, 200,250, 300,350, 400, 450]
#length = [100, 200, 300, 400, 500, 600, 700]
#length = [i * 1 for i in range(1, 70,5)]

dist = []
dist.append(0)

errado = []

for c, i in enumerate(gt_collector):
    if c + 1 > len(gt_collector) - 1:
        break

    P1 = numpy.zeros((4, 4))
    P2 = numpy.zeros((4, 4))

    P1 = gt_collector[c]
    P2 = gt_collector[c + 1]

    dx = P1[0][3] - P2[0][3]
    dy = P1[1][3] - P2[1][3]
    dz = P1[2][3] - P2[2][3]
    dist.append(dist[c] + math.sqrt(dx * dx + dy * dy + dz * dz))

for first_frame in range(0, len(gt_collector), step_size):
    for i,c in enumerate(length):
        travelled_distance = length[i]
        for l in range(first_frame, len(dist)):
            if dist[l] > dist[first_frame] + travelled_distance:
                last_frame = l
                dist_final = dist[l]
                dist_init = dist[first_frame]
                break
            last_frame = -1
        if last_frame == -1:
            continue

        pose_delta_gt = np.dot(np.linalg.inv(gt_collector[first_frame]), gt_collector[last_frame])
        pose_delta_result = np.dot(np.linalg.inv(orb_collector[first_frame]), orb_collector[last_frame])
        pose_error = np.dot(np.linalg.inv(pose_delta_result), pose_delta_gt)

        # Rotation Error
        a = pose_error[0][0]
        b = pose_error[1][1]
        c = pose_error[2][2]
        d = 0.5 * (a + b + c - 1.0)
        rot_err = math.acos(max(min(d, 1.), -1.))

        dx = pose_error[0][3]
        dy = pose_error[1][3]
        dz = pose_error[2][3]
        t_err = math.sqrt(dx * dx + dy * dy + dz * dz)

        num_frames = last_frame - first_frame + 1
        speed = travelled_distance / (0.1 * num_frames)

        rot_err = rot_err / travelled_distance
        t_err = t_err / travelled_distance
   #     print(t_err)
        err.append(Error(first_frame, rot_err, t_err, travelled_distance, speed))

        #print("De %f a %f o erro é: %f com o travelled_distance: %f" % (dist[first_frame], dist[l], t_err, travelled_distance))

f = open("Final_Evaluation.txt", "w")
for i in err:
    f.write("%f, %f, %f, %f, %f\n" % (i.first_frame, i.r_err, i.t_err, i.len, i.speed))
f.close()

step_size = 3
f = open("traj.txt", "w")
for c, i in enumerate(range(0, len(gt_collector), step_size)):
    matrix1 = gt_collector[c]
    matrix2 = orb_collector[c]
    f.write("%f, %f, %f, %f\n" % (matrix1[0][3], matrix1[1][3], matrix2[0][3], matrix2[1][3]))
f.close()
#print("----------------------------------------------")
l = 0
new_r = []
new_t = []
loc = []
f = open("tests/tlen.txt", "w")
for c, i in enumerate(length):
    t_err = 0
    r_err = 0
    num = 0
    for j in err:
        if math.fabs(j.len - length[c]) < 1.0:
            #print("Distance Travelled: %f, ou seja, de %f a %f. Valor: %f " % (j.len, dist[j.first_frame],dist[j.first_frame]+length[c], j.t_err))
            #print("%f - %f < 1.0. Valor: %f " % (j.len, length[c], j.t_err))
            t_err += j.t_err
            r_err += j.r_err
            num += 1
    if num > 2.5:
        new_t.append(t_err / num * 100)
        new_r.append(r_err / num)
        loc.append(length[c])

        f.write("%f\n" % (t_err / num * 100))
        l += 1
f.close()
speed_range = np.arange(0, 100, 5)
speed_results = []
error_results = []
f = open("tests/tspee.txt", "w")
for i in speed_range:
    t_err = 0
    r_err = 0
    num = 0
    for j in err:
        if math.fabs(j.speed-i)<2.0:
            t_err += j.t_err
            r_err += j.r_err
            num += 1

    if num>2.5:
        speed_results.append(i)
        error_results.append(t_err/num*100)
        f.write("%f\n" % (t_err/num*100))

f.close()




import matplotlib.pyplot as plt

fig1 = plt.figure(figsize=(10, 10))
plt.plot([i.x for i in orb_data], [i.y for i in orb_data], color="r", linestyle="dotted",label="Visual Odometry")
plt.axis('equal')
plt.plot([i.x for i in gt_data], [i.y for i in gt_data], color="g",label="Ground Truth")
plt.plot(gt_data[0].x,gt_data[0].y,color="black",marker = 's', markerfacecolor = 'white',label="Sequence Start")
plt.axis('equal')
plt.legend(loc="upper right")
plt.savefig('./tests/trajectory.png')

fig2 = plt.figure()
plot_y = [i for i in new_t]
plot_x = [i for i in loc]
plt.plot(plot_x, plot_y, color="b", marker = 's', markerfacecolor = 'white', label="Translation Error")
#plt.yticks(np.arange(0, max(plot_y) + 0.2, 0.2))
plt.xticks(np.arange(min(length), max(length) + 50, 50))
plt.ylabel("Translation Error [%]")
plt.xlabel("Path Length [m]")
plt.title("Test_2")
plt.legend(loc="upper right")
plt.savefig('./tests/length_error.png')

fig3 = plt.figure()
plot_y = error_results
plot_x = speed_results

plt.plot(plot_x, plot_y, color="b", marker = 's', markerfacecolor = 'white', label="Speed Error")
#plt.yticks(np.arange(0, max(plot_y) + 0.2, 0.2))
plt.xticks(np.arange(min(plot_x), max(plot_x) + 5, 5))
plt.ylabel("Translation Error [%]")
plt.xlabel("Speed [km/h]")
plt.title("Test_2")
plt.legend(loc="upper right")
plt.savefig('./tests/speed_error.png')


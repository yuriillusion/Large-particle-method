import visualization
from math import *
import copy

N = 120
M = 1
r = 15e+4
dt = 0.0002
boundary = 300
initial_speed = (1000, 1000)


def calculate_force(X, s):
    F = [[0, 0] for i in xrange(N)]
    for i in xrange(N):
        F[i][1] += M*1000
        for j in xrange(N):
            distance = calculate_distance(X[i], X[j])
            friction_force = calculate_friction_force(distance, (4, 10))
            F[i][0] += (friction_force-r*(distance-s[i][j]))*(X[i][0]-X[j][0])/(distance+0.001)
            F[i][1] += (friction_force-r*(distance-s[i][j]))*(X[i][1]-X[j][1])/(distance+0.001)
            s[i][j] = distance
    return F, s


def calculate_friction_force(distance, thresholds):
    lower_threshold, upper_threshold = thresholds
    if distance < lower_threshold:
        return 10000
    elif distance < upper_threshold:
        return 1000*(8-distance)
    else:
        return 0


def calculate_coordinates(x, v, a):
    for i in xrange(N):
        for coord in xrange(2):
            x[i][coord] += v[i][coord]*dt
    return x


def calculate_speed(x, v, a):
    for i in xrange(N):
        if x[i][1] >= boundary:
            v[i] = [0, 0]
            x[i][1] = boundary-1
        else:
            for coord in xrange(2):
                v[i][coord] += a[i][coord]*dt
    return v


def calculate_acceleration(F):
    a = [[F[i][0]/M, F[i][1]/M] for i in xrange(N)]
    return a


def initialize_conditions():
    d = 6
    '''
    x = [[6*(i%12)+5, 6*(i/12)+5] for i in xrange(N)]
    '''
    x = [range(2) for i in xrange(N)]
    for j in xrange(20):
        for i in xrange(d):
            x[i+d*(j-1)][0] = 8*i if j%2==0 else 8*i+4
            x[i+d*(j-1)][1] = 7*j+140

    s = [[calculate_distance(x[i], x[j]) for j in xrange(N)] for i in xrange(N)]
    v = [[initial_speed[0], initial_speed[1]] for i in xrange(N)]
    a = [[0, 0] for i in xrange(N)]
    return x, v, a, s


def calculate_distance(point1, point2):
    return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def simulate_frame(x, v, a, s):
    x = calculate_coordinates(x, v, a)
    F, s = calculate_force(x, s)
    a = calculate_acceleration(F)
    v = calculate_speed(x, v, a)
    return x, v, a, s


def simulate(number_of_frames):
    x, v, a, s = initialize_conditions()
    X = [copy.deepcopy(x)]
    for i in xrange(number_of_frames):
        x, v, a, s = simulate_frame(x, v, a, s)
        X.append(copy.deepcopy(x))
        print 'Time frame number:', i
    return X


if __name__ == '__main__':
    time_frames = 500
    X = simulate(time_frames)
    visualization.make_animation(X, time_frames, (0, 500), (100, boundary*1.1), 1, boundary)

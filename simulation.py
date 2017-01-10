from math import *

N = 120
M = 1
r = 25e+4
dt = 0.001
b = 10


def calculate_force(X, s):
    F = [(0, 0) for i in xrange(N)]
    for i in xrange(N):
        for j in xrange(N):
            distance = calculate_distance(X[i], X[j])
            friction_force = calculate_friction_force(distance, (6, 10))
            F[i][0] += (friction_force-r*(distance-s[i, j]))*(X[i][0]-X[j][0])/(distance+0.001)
            F[i][1] += (friction_force-r*(distance-s[i, j]))*(X[i][1]-X[j][1])/(distance+0.001)+M*2
            s[i, j] = distance
    return F


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
            x[i][coord] += v[i][coord]+a[i][coord]*dt
    return x


def calculate_speed(v, a):
    for i in xrange(N):
        for coord in xrange(2):
            v[i][coord] += a[i][coord]*dt
    return v


def calculate_acceleration(F):
    a = [(F[i][0]/M, F[i][1]/M) for i in xrange(N)]
    return a


def initialize_conditions():
    d = 6
    X = [None]*N
    for i in xrange(20):
        for j in xrange(d):
            X[i+d*(j-1)][0] = 8*i if j%2==0 else 8*i+4
            X[i+d*(j-1)][1] = 7*j+140
    s = [[calculate_distance(X[i], X[j]) for j in xrange(N)] for i in xrange(N)]
    v = [(100, 60) for i in xrange(N)]
    return X, v, s


def simulate(x, v, a, F, s):
    F = calculate_force(X, s)
    a = calculate_acceleration(F)
    v = calculate_speed(v, a)
    x = calculate_coordinates(x, v, a)
    return x, v, a, F


def calculate_distance(point1, point2):
    return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


if __name__ == '__main__':
    X, v, s = initialize_conditions()


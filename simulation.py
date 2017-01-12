import visualization
import numpy as np
import scipy.spatial.distance as dist

N = 120
M = 1
r = 15e+4
dt = 0.0002
boundary = 300
initial_speed = np.array([1000, 1000])


def calculate_force(X, s):
    F = np.zeros((N, 2))
    actual_s = dist.squareform(dist.pdist(X))
    for i in xrange(N):
        F[i, 1] += M*1000
        for j in xrange(N):
            friction_force = calculate_friction_force(actual_s[i, j], (4, 10))
            distance = actual_s[i, j]
            distance_modification = actual_s[i, j] - s[i, j]
            shift = X[i]-X[j]
            F[i] += (friction_force-r*distance_modification)*shift/(distance+0.001)
    s = actual_s
    return F


def calculate_friction_force(distance, thresholds):
    lower_threshold, upper_threshold = thresholds
    if distance < lower_threshold:
        return 10000
    elif distance < upper_threshold:
        return 1000*(8-distance)
    else:
        return 0


def calculate_coordinates(x, v):
    x += v*dt


def calculate_speed(x, v, a):
    for i in xrange(N):
        if x[i, 1] >= boundary:
            v[i] = [0, 0]
            x[i, 1] = boundary-1
        else:
            v[i] += a[i]*dt


def calculate_acceleration(F):
    return F / M


def initialize_conditions():
    d = 6
    '''
    x = [[6*(i%12)+5, 6*(i/12)+5] for i in xrange(N)]
    '''
    x = np.zeros((N, 2))
    for j in xrange(20):
        for i in xrange(d):
            x[i+d*(j-1), 0] = 8*i if j%2==0 else 8*i+4
            x[i+d*(j-1), 1] = 7*j+140

    s = dist.squareform(dist.pdist(x))
    v = np.fromfunction(lambda i, j: initial_speed[j], (N, 2), dtype=int)
    a = np.zeros((N, 2))
    return x, v, a, s


def simulate_frame(x, v, a, s):
    calculate_coordinates(x, v)
    F = calculate_force(x, s)
    a = calculate_acceleration(F)
    calculate_speed(x, v, a)
    return x, v, a, s


def simulate(number_of_frames):
    x, v, a, s = initialize_conditions()
    X = [np.copy(x)]
    for i in xrange(number_of_frames):
        simulate_frame(x, v, a, s)
        X.append(np.copy(x))
        print 'Time frame number:', i
    return X


if __name__ == '__main__':
    time_frames = 3000
    X = simulate(time_frames)
    visualization.make_animation(X, time_frames, (0, 500), (100, boundary*1.1), 1, boundary)

from math import *
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N = 120
M = 1
r = 25e+4
dt = 0.001


def calculate_force(X, s):
    F = [[0, 0] for i in xrange(N)]
    for i in xrange(N):
        F[i][1] += M*2
        for j in xrange(N):
            distance = calculate_distance(X[i], X[j])
            friction_force = calculate_friction_force(distance, (6, 10))
            F[i][0] += (friction_force-r*(distance-s[i][j]))*(X[i][0]-X[j][0])/(distance+0.001)
            F[i][1] += (friction_force-r*(distance-s[i][j]))*(X[i][1]-X[j][1])/(distance+0.001)#+M*2
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
            x[i][coord] += v[i][coord]+a[i][coord]*dt
    return x


def calculate_speed(x, v, a):
    for i in xrange(N):
        if x[i][1] > 400:
            v[i] = [0, 0]
        else:
            for coord in xrange(2):
                v[i][coord] += a[i][coord]*dt
    return v


def calculate_acceleration(F):
    a = [[F[i][0]/M, F[i][1]/M] for i in xrange(N)]
    return a


def initialize_conditions():
    d = 6
    x = [range(2) for i in xrange(N)]
    for i in xrange(20):
        for j in xrange(d):
            x[i+d*(j-1)][0] = 8*i if j%2==0 else 8*i+4
            x[i+d*(j-1)][1] = 7*j+140
    s = [[calculate_distance(x[i], x[j]) for j in xrange(N)] for i in xrange(N)]
    v = [[100, 60] for i in xrange(N)]
    return x, v, s


def calculate_distance(point1, point2):
    return sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def simulate_frame(x, v, s):
    F, s = calculate_force(x, s)
    a = calculate_acceleration(F)
    v = calculate_speed(x, v, a)
    y = calculate_coordinates(x, v, a)
    return y, v, s


def simulate(number_of_frames):
    x, v, s = initialize_conditions()
    X = [copy.deepcopy(x)]
    for i in xrange(number_of_frames):
        x, v, s = simulate_frame(x, v, s)
        X.append(copy.deepcopy(x))
    print X[0]
    print X[1]
    return X


def make_animation(X):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(0, 1000), ylim=(0, 1000))
    particles, = ax.plot([], [], 'bo', ms=5)

    def init():
        particles.set_data([], [])
        return particles,

    def animate(i):
        ms = 5
        x = [X[i][j][0] for j in xrange(N)]
        y = [X[i][j][1] for j in xrange(N)]
        particles.set_data(x, y)
        particles.set_markersize(ms)
        return particles,

    ani = animation.FuncAnimation(fig, animate, frames=15,
                              interval=100, blit=True, init_func=init)
    plt.show()


if __name__ == '__main__':
    X = simulate(15)
    make_animation(X)
    print "done"

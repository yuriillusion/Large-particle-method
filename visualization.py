import matplotlib.pyplot as plt
import matplotlib.animation as animation


def make_animation(X, time_frames, xlim, ylim, interval, boundary):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=xlim, ylim=ylim)
    plt.plot(xlim, [boundary, boundary], 'k-')
    particles, = ax.plot([], [], 'bo', ms=5)

    def init():
        particles.set_data([], [])
        return particles,

    def animate(i):
        ms = 5
        x = [x_actual[0] for x_actual in X[i]]
        y = [y_actual[1] for y_actual in X[i]]
        particles.set_data(x, y)
        particles.set_markersize(ms)
        return particles,

    ani = animation.FuncAnimation(fig, animate, frames=time_frames,
                              interval=interval, blit=True, init_func=init)
    plt.show()

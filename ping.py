from pythonping import ping
import statistics
from matplotlib import pyplot
from queue import Queue, Full


def ping_wrapper():
    return [r for r in ping("google.com", count=1, interval=1)][0].time_elapsed_ms


def main():
    response_times = Queue(maxsize=120)
    # pyplot.plot(response_times)
    pyplot.gca().set(title="Ping")
    pyplot.ion()
    pyplot.show()

    while True:
        response_time = ping_wrapper()
        if response_times.full():
            response_times.get()
        response_times.put(response_time)

        # avg = statistics.mean(list(response_times.queue))
        # print(response_time, avg)

        pyplot.clf()
        pyplot.ylim(0, 300)
        pyplot.yticks([i for i in range(0, 301, 25)])
        pyplot.plot(list(response_times.queue))
        pyplot.gca().set(title="Ping", ylabel="ms")
        pyplot.draw()
        pyplot.pause(0.01)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as k:
        print("Exiting...")

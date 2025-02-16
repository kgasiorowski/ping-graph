from pythonping import ping
from pythonping.executor import Response
from matplotlib import pyplot
from queue import Queue


def ping_wrapper():
    response: Response = [r for r in ping("google.com", count=1, interval=1, timeout=1)][0]
    return response.time_elapsed_ms if response.success else 0


def main():
    maxsize = 120
    response_times = Queue(maxsize=maxsize)
    for _ in range(maxsize):
            response_times.put(0)
    pyplot.gca().set(title="Ping")
    pyplot.ion()
    pyplot.show()

    while True:
        try:
            response_time = ping_wrapper()
        except RuntimeError:
            print("There was a runtime error. Check your connection, it may have gone down for good.")
            exit(1)

        if response_times.full():
            response_times.get()
        response_times.put(response_time)

        max_y = int(max(response_times.queue) * 1.1)
        min_y = int(min(response_times.queue) / 1.1)

        pyplot.clf()
        pyplot.ylim(min_y, max_y)
        pyplot.yticks([i for i in range(min_y, max_y, int(((max_y-min_y)/10.0)))])
        pyplot.plot(list(response_times.queue))
        pyplot.gca().set(title="Ping", ylabel="ms")
        pyplot.draw()
        pyplot.pause(0.01)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as k:
        print("Exiting...")

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
        response_time = ping_wrapper()
        if response_times.full():
            response_times.get()
        response_times.put(response_time)


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

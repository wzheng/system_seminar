#!/usr/bin/env python

import argparse
import multiprocessing
import random
import time
import redis


def new_client():
    """
    Returns a new pubsub client instance - either the Redis or ZeroMQ
    client, based on command-line arg.
    """
    Client = redis.Redis
    return Client(host=args.host, port=7000)


def publisher():
    """
    Loops forever, publishing messages to random channels.
    """
    client = new_client()
    message = u"x" * args.message_size
    while True:
        client.publish(random.choice(channels), message)


def subscriber():
    """
    Subscribes to all channels, keeping a count of the number of
    messages received. Publishes and resets the total every second.
    """
    client = new_client()
    pubsub = client.pubsub()
    for channel in channels:
        pubsub.subscribe(channel)
    last = time.time()
    messages = 0
    for message in pubsub.listen():
        messages += 1
        now = time.time()
        if now - last > 1:
            client.publish("metrics", str(messages))
            last = now
            messages = 0


def run_workers(target):
    """
    Creates processes * --num-clients, running the given target
    function for each.
    """
    for _ in range(args.num_clients):
        proc = multiprocessing.Process(target=target)
        proc.daemon = True
        proc.start()


def get_metrics():
    """
    Subscribes to the metrics channel and returns messages from
    it until --num-seconds has passed.
    """
    client = new_client().pubsub()
    client.subscribe("metrics")
    start = time.time()
    while time.time() - start <= args.num_seconds:
        message = client.listen().next()
        if message["type"] == "message":
            yield int(message["data"])


def throughput_test():
    # Create publisher/subscriber workers, pausing to allow
    # publishers to hit full throttle
    run_workers(publisher)
    time.sleep(1)
    run_workers(subscriber)

    # Consume metrics until --num-seconds has passed, and display
    # the median value.
    metrics = sorted(get_metrics())
    print metrics[len(metrics) / 2], "median msg/sec"


def latency_test():
    client = new_client()
    pubsub = client.pubsub()
    for channel in channels:
        pubsub.subscribe(channel)

    message = u"x" * args.message_size


    start = time.time()
    for i in xrange(100):
        client.publish(channels[0], message)
        messages = pubsub.listen()

    end = time.time()
    latency = (end - start) / 100.0 * 1000.0
    print "start: ", start
    print "end: ", end
    print "Latency per message: ", latency, "ms"


if __name__ == "__main__":

    # Set up and parse command-line args.
    global args, channels
    default_num_clients = multiprocessing.cpu_count() / 2
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--num-clients", type=int, default=1)
    parser.add_argument("--num-seconds", type=int, default=10)
    parser.add_argument("--num-channels", type=int, default=1)
    parser.add_argument("--message-size", type=int, default=20)

    args = parser.parse_args()
    channels = [str(i) for i in range(args.num_channels)]

    throughput_test()
    latency_test()

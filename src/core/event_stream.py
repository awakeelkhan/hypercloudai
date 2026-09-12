from queue import Queue


class EventStream:
    def __init__(self):
        self.events = []
        self.queue = Queue()

    def emit(self, event):
        self.events.append(event)
        self.queue.put(event)

        print(
            f"[EVENT] {event.eventType}"
        )

    def getEvents(self):
        return self.events

    def getNext(self):
        return self.queue.get()

    def close(self):
        self.queue.put(None)

    def clear(self):
        self.events = []
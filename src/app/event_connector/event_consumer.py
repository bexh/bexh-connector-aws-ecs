from src.consumer import Consumer


class EventConsumer(Consumer):
    def __init__(self):
        super(EventConsumer, self).__init__()

    def process(self, message):
        print("GOT IT")

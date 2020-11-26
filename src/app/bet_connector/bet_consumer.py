from src.consumer import Consumer


class BetConsumer(Consumer):
    def __init__(self):
        super(BetConsumer, self).__init__()

    def process(self, message):
        pass

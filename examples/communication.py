import zmq
import numpy as np


class StatePublisher:
    def __init__(self, port=5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")

    def send(self, state):
        self.socket.send(state.astype(np.float64).tobytes())

    def close(self):
        self.socket.close()


class StateSubscriber:
    def __init__(self, port=5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def receive(self):
        data = self.socket.recv()
        return np.frombuffer(data, dtype=np.float64)

    def close(self):
        self.socket.close()


class ControlPublisher:
    def __init__(self, port=5556):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")

    def send(self, u):
        self.socket.send(u.astype(np.float64).tobytes())

    def close(self):
        self.socket.close()


class ControlSubscriber:
    def __init__(self, port=5556):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def receive(self):
        data = self.socket.recv()
        return np.frombuffer(data, dtype=np.float64)

    def close(self):
        self.socket.close()
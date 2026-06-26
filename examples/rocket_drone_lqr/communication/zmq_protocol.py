import json
from typing import Any

import zmq

DEFAULT_ENDPOINT = "tcp://127.0.0.1:5557"


class ZmqServer:
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT):
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(endpoint)

    def receive(self) -> dict[str, Any]:
        raw = self.socket.recv_string()
        return json.loads(raw)

    def send(self, message: dict[str, Any]) -> None:
        self.socket.send_string(json.dumps(message))


class ZmqClient:
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT):
        self.context = zmq.Context.instance()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(endpoint)

    def request(self, message: dict[str, Any]) -> dict[str, Any]:
        self.socket.send_string(json.dumps(message))
        raw = self.socket.recv_string()
        return json.loads(raw)
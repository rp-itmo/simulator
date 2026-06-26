import threading
import time

from examples.rocket_drone_lqr.communication.zmq_protocol import ZmqClient, ZmqServer


def test_zmq_request_response_roundtrip():
    endpoint = "tcp://127.0.0.1:5567"
    received = {}

    def server_task():
        server = ZmqServer(endpoint)
        message = server.receive()
        received.update(message)
        server.send({"ok": True, "value": message["value"]})

    thread = threading.Thread(target=server_task, daemon=True)
    thread.start()

    time.sleep(0.1)

    client = ZmqClient(endpoint)
    response = client.request({"value": 42})

    assert response == {"ok": True, "value": 42}
    assert received == {"value": 42}
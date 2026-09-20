import zmq

from laptimes import models
from .common import PassingSaver


class OpenStintPassingSaver(PassingSaver):
    def connect(self):
        address = f"tcp://{self.decoder.ip}:{str(self.decoder.port or 5556)}"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        print(f"Connected to {address}. Waiting for messages...")

    def read(self):
        msg = self.socket.recv_string().strip()
        print(msg)
        if not msg.startswith("P "):
            return  # ignore non-"P" messages
        parts = msg.split()
        if len(parts) < 6:
            return  # malformed message

        try:
            timecode = int(parts[1])
            transponder_type = parts[2]
            transponder_id = int(parts[3])
            rssi = float(parts[4])
            hit_count = int(parts[5])
            passing_obj = models.Passing(
                decoder=self.decoder,
                timestamp=timecode,
                signal=rssi,
                hit_count=hit_count,
                transponder=self.transponder(transponder_type, transponder_id)
            )
            passing_obj.save()

        except ValueError:
            return  # skip malformed data

    def close(self):
        self.socket.close()
        self.context.term()

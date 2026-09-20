import logging
import socket

from ambp3parser.record import AMBRecord, Passing

from laptimes import models
from .common import PassingSaver

logger = logging.getLogger(__name__)


class MyLapsPassingSaver(PassingSaver):
    socket: socket.socket
    buffer = b''

    def connect(self):
        logger.info('Connecting to %s:%d' % (self.decoder.ip, self.decoder.port or 5403))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.settimeout(0)
        self.socket.connect((self.decoder.ip, self.decoder.port or 5403))

    def close(self):
        logger.info('Closing socket to decoder %s' % self.decoder)
        self.socket.close()

    def _read(self):
        while True:
            response = self.socket.recv(1024)
            self.buffer += response
            if self.buffer.find(b'\x8e') is not None and self.buffer.find(b'\x8f') is not None:
                data = self.buffer  # Return when there is a valid record in the buffer
                self.buffer = b''
                return data

    def read(self):
        data = self._read()
        records = AMBRecord.parse_multiple_records(data)
        record: Passing
        for record in records:
            if record.TOR != 1:
                continue
            passing_obj = models.Passing(
                decoder=self.decoder,
                timestamp=record.RTC_TIME / 1000,
                signal=record.STRENGTH,
                hit_count=record.HITS,
                transponder=self.transponder('AMB', record.TRANSPONDER),
            )
            passing_obj.save()

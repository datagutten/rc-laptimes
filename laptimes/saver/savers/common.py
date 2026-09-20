from abc import ABC, abstractmethod

from laptimes import models


class PassingSaver(ABC):
    decoder: models.Decoder
    transponders = {}

    def __init__(self, decoder=models.Decoder):
        self.decoder = decoder

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def read(self):
        raise NotImplementedError()

    def run(self):
        self.connect()
        while True:
            try:
                self.read()
            except KeyboardInterrupt:
                print("\nInterrupted by user.")
                break

        self.close()

    def transponder(self, transponder_type: str, number: int) -> models.Transponder:
        assert transponder_type in ['OPN', 'AMB', 'VOS']
        key = f'{transponder_type}-{number}'
        if key in self.transponders:
            return self.transponders[key]

        transponder_obj, created = models.Transponder.objects.get_or_create(
            number=number,
            transponder_type=transponder_type,
        )
        self.transponders[key] = transponder_obj
        return transponder_obj

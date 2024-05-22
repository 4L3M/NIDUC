from Coding import Coding


class Decoder:
    """Klasa zawierająca metody dekodowania danych."""

    package = []

    def receive_package(self, package, choose_coding):
        """Otrzymuje pakiet i zwraca True jeśli kodowanie zgadza sie z wiadomością."""

        self.package = package
        if choose_coding == 0:
            if Coding.parity_bit(self.package[:-1]) == self.package[-1]:
                return True
            return False

        # kodowanie CRC8
        if choose_coding == 1:
            if package[-8:] == Coding.crc_8(package[0:-8]):
                return True
            return False
        # kodowanie CRC16
        if choose_coding == 2:
            if package[-16:] == Coding.crc_16(package[0:-16]):
                return True
            return False
        if choose_coding == 3:
            if package[-32:] == Coding.crc_32(package[0:-32]):
                return True
            return False

    def remove_coding_bits(self, packet, choose_coding):
        """Usuwa bity z pakietu, dodane w trakcie kodowania."""

        if choose_coding == 0:
            return packet[:-1]

        # kodowanie CRC8
        if choose_coding == 1:
            return packet[:-8]
        # kodowanie CRC16
        if choose_coding == 2:
            return packet[:-16]
        # kodowanie CRC32
        if choose_coding == 3:
            return packet[:-32]


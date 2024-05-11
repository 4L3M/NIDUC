from DetectionCoding import DetectionCoding
from CorrectionCoding import CorrectionCoding

class Decoder:
    package = []

    def receive_package(self, package, choose_coding):
        """ Odbiera pakiet i zwraca True jeśli pakiet jest poprawny
            package - pakiet do odbioru"""
        self.package = package
        detectionCoding = DetectionCoding()
        if choose_coding == 0:
            if detectionCoding.parity_bit(self.package[:-1]) == self.package[-1]:
                return True
            return False

        # CRC-8
        if choose_coding == 1:
            if package[-8:] == detectionCoding.crc_8(package[0:-8]):
                return True
            return False
        # CRC-16
        if choose_coding == 2:
            if package[-16:] == detectionCoding.crc_16(package[0:-16]):
                return True
            return False
        # CRC-32
        if choose_coding == 3:
            if package[-32:] == detectionCoding.crc_32(package[0:-32]):
                return True
            return False

    def remove_coding_bits(self, packet, choose_coding):
        """ Usuwa bity kodowania z pakietu
            package - pakiet do oczyszczenia
            choose_coding - wybór kodowania"""
        if choose_coding == 0:
            return packet[:-1]
        if choose_coding == 1:
            return packet[:-8]
        if choose_coding == 2:
            return packet[:-16]
        if choose_coding == 3:
            return packet[:-32]

    def hamming_decode(self, encode_data):
        """ Dekoduje dane zakodowane kodem Hamminga
            encode_data - zakodowane dane"""
        r = 0
        while 2 ** r < len(encode_data):
            r += 1

        decoded_data = []
        error_position = 0

        for i in range(r):
            parity_index = 2 ** i - 1
            parity_value = 0
            for j in range(parity_index, len(encode_data), 2 * (parity_index + 1)):
                parity_value ^= int(encode_data[j])
            if parity_value != 0:
                error_position += parity_index + 1

        if error_position > 0 and error_position < len(encode_data) + 1:
            encode_data[error_position - 1] ^= 1

        for i in range(1, len(encode_data) + 1):
            if i & (i - 1) != 0:
                decoded_data.append(encode_data[i - 1])

        return decoded_data
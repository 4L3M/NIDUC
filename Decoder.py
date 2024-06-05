from reedsolo import RSCodec

from DetectionCoding import DetectionCoding
from CorrectionCoding import CorrectionCoding

class Decoder:
    package = []

    def receive_package(self, package, choose_coding):
        """ Odbiera pakiet i zwraca True jeśli pakiet jest poprawny
            package - pakiet do odbioru"""
        self.package = package
        detectionCoding = DetectionCoding()

        # Ensure that package is not None
        if self.package is None:
            return False

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

    # def decode_tmr(self, encoded_data):
    #     """
    #     Dekodowanie danych zakodowanych potrójną redundancją modułową (TMR)
    #     Używa głosowania większościowego do określenia poprawnej wartości każdego bitu
    #
    #     :param encoded_data: String zakodowanych danych binarnych TMR (np. '111000111111')
    #     :return: Dane zdekodowane jako string
    #
    #     """
    #     if len(encoded_data) % 3 != 0:
    #         raise ValueError("Encoded data length must be a multiple of 3")
    #
    #     decoded_data = []
    #     for i in range(0, len(encoded_data), 3):
    #         triplet = encoded_data[i:i + 3]
    #         bit = '1' if triplet.count('1') > 1 else '0'
    #         decoded_data.append(bit)
    #
    #     return ''.join(decoded_data)

    def hamming_distance(self, seq1, seq2):
        return sum(el1 != el2 for el1, el2 in zip(seq1, seq2))

    def convolutional_decoder(self, encoded_data, g1, g2):
        data_bits = []
        register = [0] * max(len(g1), len(g2))
        correction = CorrectionCoding()


        for i in range(0, len(encoded_data), 2):
            received_bits = [int(encoded_data[i]), int(encoded_data[i + 1])]

            possible_outputs = [
                ([0], [0, 0]),
                ([0], [0, 1]),
                ([0], [1, 0]),
                ([0], [1, 1]),
                ([1], [0, 0]),
                ([1], [0, 1]),
                ([1], [1, 0]),
                ([1], [1, 1])
            ]

            min_distance = float('inf')
            best_match = None

            for input_bits, expected_output in possible_outputs:
              #  register = correction.convolutional_encoder().shift_register(register, input_bits[0])

                register = correction.shift_register(register, input_bits[0])
                output_bit1 = correction.xor_output(register, g1)
                output_bit2 = correction.xor_output(register, g2)
                distance = self.hamming_distance(received_bits, [output_bit1, output_bit2])

                if distance < min_distance:
                    min_distance = distance
                    best_match = input_bits[0]

            data_bits.append(best_match)

        return ''.join(map(str, data_bits))

    def bch_decode(self, encode_data):
        correctionCoding = CorrectionCoding()
        decoded_data = correctionCoding.bch_decode(encode_data)
        return decoded_data if decoded_data is not None else encode_data
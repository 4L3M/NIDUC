class Coding:
    """Klasa zawierająca metody kodowania danych."""

    @staticmethod
    def parity_bit(signal):
        """Zwraca bit parzystosci."""

        if signal.count(1) % 2 == 0:  # jezeli parzysta liczba '1', to parity = 0
            return 0
        else:
            return 1

    #
    @staticmethod
    def string_to_array(binary_string, coding):
        """Przekształca ciąg bitów na tablice bitów."""

        tab = []
        if (len(binary_string) - 2) % coding != 0:
            for i in range(coding - (len(binary_string) - 2) % coding):
                tab.append(0)
        for i in range(len(binary_string) - 2):
            bit = int(binary_string[i + 2])
            tab.append(bit)
        return tab

    @staticmethod
    def crc_8(data):
        """Generuje bity CRC8."""

        crc = 0
        polynomial = 0x8C  # polinom CRC-16
        for bit in data:
            crc ^= bit
            for i in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
        return Coding.string_to_array(bin(crc & 0XFF), 8)

    @staticmethod
    def crc_16(data):
        """Generuje bity CRC16."""

        crc = 0xFFFF
        polynomial = 0xA001  # polinom CRC-16
        for bit in data:
            crc ^= bit
            for i in range(16):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ polynomial
                else:
                    crc >>= 1
        return Coding.string_to_array(bin(crc & 0xFFFF), 16)

    @staticmethod
    def crc_32(data):
        """Generuje bity CRC32."""

        crc = 0xFFFFFFFF
        polynomial = 0xEDB88320  # polinom CRC-32
        for bit in data:
            crc ^= bit
            for i in range(32):
                if crc & 0x00000001:
                    crc = (crc >> 1) ^ polynomial
                else:
                    crc >>= 1
        return Coding.string_to_array(bin(crc & 0xFFFFFFFF), 32)

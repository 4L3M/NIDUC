class DetectionCoding:
    def __init__(self):
        pass
    def parity_bit(self, signal):
        """
        Kodowanie bitu parzystości
            signal - sygnał do zakodowania
            return - zakodowany sygnał
        """
        if signal.count(1) % 2 == 0:
            return 0
        else:
            return 1

    def string_to_array(self, binary_string, coding):
        """
        Zamienia ciąg bitów na tablicę bitów
            string - ciąg bitów
            coding - kodowanie
            return - tablica bitów
        """
        tab = []
        if(len(binary_string) - 2) % coding != 0:
            for i in range(coding - (len(binary_string) - 2) % coding):
                tab.append(0)
        for i in range(len(binary_string) - 2):
            bit = int(binary_string[i + 2])
            tab.append(bit)
        return tab

    def crc_8(self, data):
        """ Generuje bity CRC-8
            data - sygnał do zakodowania
            return - zakodowany sygnał"""
        crc = 0
        polynom = 0x8C # 0x07 = x^8 + x^2 + x + 1 wielomian dla crc-8
        for bit in data:
            crc ^= bit
            for i in range(8):
                if crc & 0x80:
                    crc = (crc >> 1) ^ polynom
                else:
                    crc >>= 1
        return self.string_to_array(bin(crc & 0xFF), 8)

    def crc_16(self, data):
        """ Generuje bity CRC-16
            data - sygnał do zakodowania
            return - zakodowany sygnał"""
        crc = 0xFFFF
        polynom = 0xA001  # 0x07 = x^8 + x^2 + x + 1 wielomian dla crc-8
        for bit in data:
            crc ^= bit
            for i in range(16):
                if crc & 0x001:
                    crc = (crc >> 1) ^ polynom
                else:
                    crc >>= 1
        return self.string_to_array(bin(crc & 0xFFFF), 16)

    def crc_32(self, data):
        """ Generuje bity CRC-32
            data - sygnał do zakodowania
            return - zakodowany sygnał"""
        crc = 0xFFFFFFFF
        polynom = 0xEDB88320  # 0x07 = x^8 + x^2 + x + 1 wielomian dla crc-8
        for bit in data:
            crc ^= bit
            for i in range(32):
                if crc & 0x00000001:
                    crc = (crc >> 1) ^ polynom
                else:
                    crc >>= 1
        return self.string_to_array(bin(crc & 0xFFFFFFFF), 32)
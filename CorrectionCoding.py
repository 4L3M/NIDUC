import bchlib


class CorrectionCoding:
    def hamming_encode(self, data):

        # Liczba bitów potrzebna do zakodwania danych
        r = 0
        while 2 ** r < len(data) + r + 1:
            r += 1
        # Lista bitów danych i bitów parzystości (początkowo None)
        encoded_data = [None] * (len(data) + r)

        # Wypełnianie listy bitami danych
        j = 0
        for i in range(1, len(encoded_data) + 1):
            if i & (i - 1) == 0:
                encoded_data[i - 1] = 0 #Bit parzystości na 0
            else:
                encoded_data[i - 1] = int(data[j])
                j += 1

        #Obliczanie wartości bitów parzystości
        for i in range(r):
            parity_index = 2**i - 1
            parity_value = 0
            for j in range(parity_index, len(encoded_data), 2 * parity_index + 2):
                parity_value ^= encoded_data[j]
            encoded_data[parity_index] = parity_value

        return encoded_data

    """----------------- BCH -----------------"""

    def bch_encode(self, data):
        t = 8  # Error correction capability
        poly = 8219  # Example polynomial, replace with a valid one if necessary
        m = 13  # Galois field size, replace with a valid one if necessary
        swap_bits = False
        try:
            bch = bchlib.BCH(t, poly, m, swap_bits)
        except RuntimeError as e:

            return None

        data_bytes = bytes(data)
        ecc = bch.encode(data_bytes)
        packet = data_bytes + ecc
        return list(packet)



    def repeat_encode(self, data, repeat_factor):
        """ Kodowanie danych poprzez powtarzanie """
        encoded_data = []
        for bit in data:
            encoded_data.extend([bit] * repeat_factor)
        return encoded_data

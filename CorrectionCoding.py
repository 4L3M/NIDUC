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

import bchlib
import numpy as np
from numpy.polynomial import polynomial as poly

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
            print(f"Error initializing BCH: {e}")
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




    #
    # @staticmethod
    # def gf2_add(x, y):
    #     return x ^ y
    #
    # @staticmethod
    # def gf2_multiply(x, y):
    #     result = 0
    #     while y > 0:
    #         if y & 1:
    #             result ^= x
    #         y >>= 1
    #         x <<= 1
    #     return result & 0xFF  # Ensure result is in GF(2^m)
    #
    # @staticmethod
    # def polynomial_multiply(a, b):
    #     result = [0] * (len(a) + len(b) - 1)
    #     for i in range(len(a)):
    #         for j in range(len(b)):
    #             result[i + j] ^= CorrectionCoding.gf2_multiply(a[i], b[j])
    #     return result
    #
    # @staticmethod
    # def polynomial_mod(dividend, divisor):
    #     result = list(dividend)
    #     for i in range(len(dividend) - len(divisor) + 1):
    #         if result[i] != 0:
    #             for j in range(len(divisor)):
    #                 result[i + j] ^= divisor[j]
    #     return result[-(len(divisor) - 1):]
    #
    # @staticmethod
    # def generate_gx(t, n):
    #     gx = [1]
    #     for i in range(t):
    #         gx = CorrectionCoding.polynomial_multiply(gx, [1, 2 ** i])
    #     return gx
    #
    # @staticmethod
    # def encode_bch(data, t, n):
    #     gx = CorrectionCoding.generate_gx(t, n)
    #     padded_data = data + [0] * (len(gx) - 1)
    #     remainder = CorrectionCoding.polynomial_mod(padded_data, gx)
    #     encoded_data = data + remainder
    #     return encoded_data
    #
    # @staticmethod
    # def calculate_syndromes(data, t, n):
    #     syndromes = []
    #     for i in range(1, 2 * t + 1):
    #         syndrome = 0
    #         for j in range(len(data)):
    #             syndrome ^= CorrectionCoding.gf2_multiply(data[j], 2 ** (i * j))
    #         syndromes.append(syndrome)
    #     return syndromes
    #
    # @staticmethod
    # def find_error_locator(syndromes, t):
    #     error_locator = [1]
    #     b = [1]
    #
    #     for i in range(t):
    #         delta = syndromes[i]
    #         for j in range(1, len(error_locator)):
    #             delta ^= CorrectionCoding.gf2_multiply(error_locator[-(j + 1)], syndromes[i - j])
    #
    #         b.append(0)
    #
    #         if delta != 0:
    #             new_error_locator = error_locator + [0] * (len(b) - len(error_locator))
    #             for j in range(len(b)):
    #                 new_error_locator[j] ^= CorrectionCoding.gf2_multiply(delta, b[j])
    #             if len(b) > len(error_locator):
    #                 b = [CorrectionCoding.gf2_multiply(x, delta) for x in error_locator]
    #             error_locator = new_error_locator
    #
    #     return error_locator
    #
    # @staticmethod
    # def find_error_positions(error_locator, n):
    #     error_positions = []
    #     for i in range(n):
    #         result = 0
    #         for j in range(len(error_locator)):
    #             result ^= CorrectionCoding.gf2_multiply(error_locator[j], 2 ** (j * i))
    #         if result == 0:
    #             error_positions.append(n - 1 - i)
    #     return error_positions
    #
    # @staticmethod
    # def correct_errors(data, error_positions):
    #     corrected_data = list(data)
    #     for pos in error_positions:
    #         corrected_data[pos] = CorrectionCoding.gf2_add(corrected_data[pos], 1)
    #     return corrected_data
    #
    # @staticmethod
    # def decode_bch(encoded_data, t, n):
    #     syndromes = CorrectionCoding.calculate_syndromes(encoded_data, t, n)
    #     if max(syndromes) == 0:
    #         return encoded_data[:n - 2 * t]
    #
    #     error_locator = CorrectionCoding.find_error_locator(syndromes, t)
    #     error_positions = CorrectionCoding.find_error_positions(error_locator, len(encoded_data))
    #     if not error_positions:
    #         return None  # Cannot correct errors
    #
    #     corrected_data = CorrectionCoding.correct_errors(encoded_data, error_positions)
    #
    #     if max(CorrectionCoding.calculate_syndromes(corrected_data, t, n)) == 0:
    #         return corrected_data[:n - 2 * t]
    #     else:
    #         return None

#
# # Parametry BCH
# n = 15  # Długość kodu
# t = 3  # Liczba błędów, które można skorygować
#
# # Dane do zakodowania
# data = [1, 0, 0, 0, 1, 1, 0, 1, 1]
#
# # Utworzenie instancji klasy CorrectionCoding
# correction_coding = CorrectionCoding()
#
# # Zakodowanie danych
# encoded_data = correction_coding.encode_bch(data, t, n)
# print("Encoded Data: ", encoded_data)
#
# # Uszkodzenie danych dla testów
# encoded_data_with_errors = list(encoded_data)
# encoded_data_with_errors[3] ^= 1  # Wprowadzenie błędu
# encoded_data_with_errors[7] ^= 1  # Wprowadzenie błędu
# print("Encoded Data with Errors: ", encoded_data_with_errors)
#
# # Dekodowanie danych
# decoded_data = correction_coding.decode_bch(encoded_data_with_errors, t, n)
# print("Decoded Data: ", decoded_data)


"""----------------- powtorzenia -----------------"""




# @staticmethod
# def encode_repeat(data, repetition_factor):
#     encoded_data_r = []
#     for bit in data:
#         encoded_data_r.extend([bit] * repetition_factor)
#     return encoded_data_r
#
#
# @staticmethod
# def decode_repeat(encoded_data, repetition_factor):
#     decoded_data = []
#     for i in range(0, len(encoded_data), repetition_factor):
#         chunk = encoded_data[i:i + repetition_factor]
#         if len(chunk) == repetition_factor:
#             majority_bit = 1 if sum(chunk) > (repetition_factor // 2) else 0
#             decoded_data.append(majority_bit)
#     return decoded_data


# Przykład użycia dla CorrectionCoding
# n = 15  # Długość kodu
# t = 3   # Liczba błędów, które można skorygować
#
# data = [1, 0, 0, 0, 1, 1, 0, 1, 1]
#
# correction_coding = CorrectionCoding()
#
# encoded_data = correction_coding.encode_repeat(data, t, n)
# print("Encoded Data (BCH): ", encoded_data)
#
# # Uszkodzenie danych dla testów (wprowadzenie błędów)
# encoded_data_with_errors = list(encoded_data)
# encoded_data_with_errors[3] = 0 if encoded_data_with_errors[3] == 1 else 1  # Wprowadzenie błędu
# encoded_data_with_errors[7] = 0 if encoded_data_with_errors[7] == 1 else 1  # Wprowadzenie błędu
# print("Encoded Data with Errors (BCH): ", encoded_data_with_errors)
#
# decoded_data = correction_coding.decode_repeat(encoded_data_with_errors, t, n)
# print("Decoded Data (BCH): ", decoded_data)
#
# # Przykład użycia dla RepetitionCoding
# data = [1, 0, 1, 1, 0, 0, 1]
# repetition_factor = 3
#
# cr = CorrectionCoding()
#
# encoded_data_repetition = cr.encode(data, repetition_factor)
# print("Encoded Data (Repetition): ", encoded_data_repetition)
#
# encoded_data_with_errors_repetition = list(encoded_data_repetition)
# encoded_data_with_errors_repetition[3] = 0 if encoded_data_with_errors_repetition[3] == 1 else 1  # Wprowadzenie błędu
# encoded_data_with_errors_repetition[7] = 0 if encoded_data_with_errors_repetition[7] == 1 else 1  # Wprowadzenie błędu
# encoded_data_with_errors_repetition[11] = 0 if encoded_data_with_errors_repetition[11] == 1 else 1  # Wprowadzenie błędu
# print("Encoded Data with Errors (Repetition): ", encoded_data_with_errors_repetition)
#
# decoded_data_repetition = cr.decode(encoded_data_with_errors_repetition, repetition_factor)
# print("Decoded Data (Repetition): ", decoded_data_repetition)
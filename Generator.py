import random
from Coding import Coding
from NumberGenerator import PseudoRandGenerator


class Generator:

    """
    Klasa zwierająca metody generowania danych.
    """
    def __init__(self, number_of_bits_for_a_package):
        self.num_to_signal = PseudoRandGenerator()
        self.number_of_bits = number_of_bits_for_a_package

    def __split_into_packages(self, signal):
        """
        Dzieli sygnał na pakiety
        zwraca listę z pakietami.
        """

        packages = []
        for i in range(0, len(signal), self.number_of_bits):
            package = signal[i: i + self.number_of_bits]
            packages.append(package)
        return packages


    def generate_signal(self, length):
        """Generuje randomowy sygnał."""

        tab = []
        tab = self.num_to_signal.binary_number(length)
        return tab

    def generate_package(self, signal, choose_coding):
        """Dzieli sygnał na pakiety i dodaje kodowanie. Zwraca ramkę z pakietami. Możliwe kodowania:\n
        '0' - bit parzystosci,\n
        '1' - CRC8,\n
        '2' - CRC16,\n
        '3' - CRC32."""

        # podziel na n-bitowe pakiety
        packages = self.__split_into_packages(signal)
        # dla każdego pakietu dodaj bit parzystości
        if choose_coding == 0:
            for packet in packages:
                packet.append(Coding.parity_bit(packet))
                # self.__add_parity_bit(packet)
        # kodowanie CRC8
        if choose_coding == 1:
            for packet in packages:
                packet += Coding.crc_8(packet)
        # kodowanie CRC16
        if choose_coding == 2:
            for packet in packages:
                packet += Coding.crc_16(packet)
        if choose_coding == 3:
            for packet in packages:
                packet += Coding.crc_32(packet)

        # zwroc paczkę z pakietami
        return packages

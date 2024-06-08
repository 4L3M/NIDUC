import random

from DetectionCoding import DetectionCoding
from CorrectionCoding import CorrectionCoding


class Generator:

    def __init__(self, bits_for_package):
        self.numb_of_bits = bits_for_package


    def generate_signal(self, length):
        """ Generuje sygnał o długości length
            length - długość sygnału
            return - sygnał (tablica)"""
        tab = []
        for i in range(length):
            tab.append(random.randint(0, 1))
        return tab

    def split_signal_into_packages(self, signal):
        """ Dzieli sygnał na paczki o długości self.numb_of_bits
            signal - sygnał do podzielenia
            return - lista paczek (tablica)"""
        packages = []
        for i in range(0, len(signal), self.numb_of_bits):
            package = signal[i: i + self.numb_of_bits]
            packages.append(package)
        return packages

    def generate_package(self, signal, choose_coding, type = 0):
        """ Generuje pakiety - dzieli sygnał na paczki i koduje je
            signal - sygnał do podzielenia i zakodowania
            choose_coding - wybór kodowania
            type - typ kodowania
            return - lista paczek (tablica)"""
        detectionCoding = DetectionCoding()
        correctionCoding = CorrectionCoding()
        packages = self.split_signal_into_packages(signal)
        """ Bit parzystości """
        # Kodowanie bitu parzystości
        if choose_coding == 0:
            for packet in packages:
                packet.append(detectionCoding.parity_bit(packet))
        # Kodowanie CRC-8
        if choose_coding == 1:
            for packet in packages:
                packet+=detectionCoding.crc_8(packet)
        # Kodowanie CRC-16
        if choose_coding == 2:
            for packet in packages:
                packet+=detectionCoding.crc_16(packet)
        # Kodowanie CRC-32
        if choose_coding == 3:
            for packet in packages:
                packet+=detectionCoding.crc_32(packet)


#---------Kody korekcyjne ----------------------

        # Kodowanie Hamminga
        if type == 0:
            for i, packet in enumerate(packages):
                packages[i] = correctionCoding.hamming_encode(packet)
        # Kodowanie BCH
        if type == 1:
            for i, packet in enumerate(packages):
                packages[i] = correctionCoding.bch_encode(packet)

        if type == 2:  # Kodowanie powtórzeń
            for i, packet in enumerate(packages):
                packages[i] = correctionCoding.repeat_encode(packet, 3)

        # Zwraca paczkę z pakietami
        return packages
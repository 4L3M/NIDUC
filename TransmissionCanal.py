import copy
import random


class TransmissionCanal:

    not_free_to = 0.0
    bandwidth = 0

    def __init__(self, bandwidth):
        self.bandwidth = bandwidth

    def transmission(self, packet, noise):
        """ Symuluje transmisję pakietu przez kanał
            packet - pakiet do przesłania
            noise - szum w kanale
            return -  zakłócony pakiet"""
        packet = copy.deepcopy(packet)

        for i in range(len(packet)):
            if 1 == random.randint(1,1 / noise): # zakłócenie pakietu z prawdopodobieństwem 1/noise
                packet[i] = random.randint(0, 1)
        return packet # zakłócony pakiet

    def is_free(self, time):
        """ Sprawdza czy kanał jest wolny
            time - czas
            return - True jeśli kanał jest wolny i może przesłać pakiet, False w przeciwnym wypadku"""
        if time > self.not_free_to:
            return True
        else:
            return False
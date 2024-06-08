import copy
import random

# BINARY SYMMETRIC CHANNEL
class TransmissionCanal:

    not_free_to = 0.0
    bandwidth = 0

    def __init__(self, bandwidth):
        self.bandwidth = bandwidth

    def transmission(self, packet, noise, error_type = 'BER'):
        """ Symuluje transmisję pakietu przez kanał
            packet - pakiet do przesłania
            noise - szum w kanale
            return -  zakłócony pakiet"""
        packet = copy.deepcopy(packet)

#Zaklocenie pakietu w zaleznosci od wybranego typu zaklocenia
        # BER - Bit Error Rate
        if error_type == 'BER':
            for i in range(len(packet)):
                if random.random() < noise:
                    packet[i] = 1 if packet[i] == 0 else 0
        # independent - niezależne zakłócenia
        elif error_type == 'independent':
            for i in range(len(packet)):
                if random.random() < noise:
                    packet[i] = 1 if packet[i] == 0 else 0
        # burst - zakłócenia grupowe
        elif error_type == 'burst':
            burst_length = int(len(packet) * noise)
            burst_start = random.randint(0, len(packet) - burst_length)
            for i in range(burst_start, burst_start + burst_length):
                packet[i] = 1 if packet[i] == 0 else 0


#Podstawowa forma zaklocenia pakietu
        # for i in range(len(packet)):
        #     if 1 == random.randint(1,int(1 / noise)): # zakłócenie pakietu z prawdopodobieństwem 1/noise
        #         packet[i] = random.randint(0, 1)
        return packet # zakłócony pakiet

    def is_free(self, time):
        """ Sprawdza czy kanał jest wolny
            time - czas
            return - True jeśli kanał jest wolny i może przesłać pakiet, False w przeciwnym wypadku"""
        if time > self.not_free_to:
            return True
        else:
            return False
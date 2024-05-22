import copy
import random


class TransmissionCanal:
    """Klasa zawierająca metody symulujące kanał transmisyjny."""

    not_free_to = 0.0
    bandwidth = 0

    def __init__(self, bandwidth):
        self.bandwidth = bandwidth

    def transmission(self, packet, noise):
        """Metoda symulująca przesył danych w kanale transmisyjnym o prawdopodobieństwie przekłamania bitu 'noise'.
        Zwraca zakłócony sygnał."""

        packet = copy.deepcopy(packet)

        for i in range(len(packet)):
            if 1 == random.randint(1, 1 / noise):
                packet[i] = random.randint(0, 1)
        return packet  # zwraca zaburzony lub niezaburzony sygnal

    def is_free(self, time):
        """Metoda zwraca True jeśli kanał jest wolny i może przesłać dane."""
        if time > self.not_free_to:
            return True
        else:
            return False

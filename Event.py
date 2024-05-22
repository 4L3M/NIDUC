class Event:
    """Klasa przechowująca zdarzenia."""

    start_time = 0
    packet = []
    duration = 0
    retransmission = 0 #licznik retransmiji
    check_sum_correct = 1  # 0 niepoprawny, 1 poprawny
    id = 0

    def __init__(self, packet, start_time, duration):
        self.start_time = start_time
        self.packet = packet
        self.duration = duration

    def __lt__(self, other): # funkcja wymagana przez kolejke priorytetowa
        return self.start_time < other.start_time

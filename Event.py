class Event:
    start_time = 0
    packet = []
    duration = 0
    retranmission = 0
    check_sum_if_correct = True # True - poprawny, False - niepoprawny
    id = 0

    def __init__(self, packet, start_time, duration):
        self.start_time = start_time
        self.packet = packet
        self.duration = duration

    # Dla kolejki priorytetowej
    def __lt__(self, other):
        return self.start_time < other.start_time


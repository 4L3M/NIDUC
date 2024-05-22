import random
from queue import PriorityQueue
from Event import Event
from Generator import Generator
from Decoder import Decoder
from TransmissionCanal import TransmissionCanal


def compare_signals(signal_in, signal_out):
    """Metoda porównująca dwa sygnały."""

    lost = 0
    for i in range(len(signal_in)):
        if signal_in[i] != signal_out[i]:
            lost += 1

    global stat
    stat = lost / len(signal_in)
    stat = round(stat * 100, 2)
    print("Sygnał wysłany:  ",signal_in)
    print("Sygnał odebrany: ",signal_out)
    print("Zakłamane bity: ", stat, "%")

def simulation(coding, packet_length, num_of_retransimssion2, signal_length, noise, bandwidth):
    """Symulacja transmisji w systemie ARQ."""

    result_queue = PriorityQueue()
    generator = Generator(packet_length)
    decoder = Decoder()
    times = []
    events_queue = PriorityQueue()
    current_time = 0.5
    delta_time = 0.5

    signal = generator.generate_signal(signal_length)
    received = []

    pakiety = generator.generate_package(signal, coding)

    transmission_canal = TransmissionCanal(bandwidth)
    iter = 0
    for packet in pakiety:
        r1 = (random.randint(1, 5) / 22)
        r2 = (random.randint(1, 3) / 333)
        duration = r1 * r2 * len(packet) / bandwidth
        event = Event(packet, current_time, duration)
        iter += 1

        event.id = iter
        events_queue.put(event)
        current_time += delta_time + (random.randint(1, 3) / 333) * (random.randint(1, 3) / 333)

    while not events_queue.empty():
        event = events_queue.get() # pobranie zdarzenie z kolejki
        # Sprawdzamy czy kanał jest wolny
        if transmission_canal.is_free(event.start_time):
            transmission_canal.not_free_to += event.duration
            # transmisja
            packet2 = transmission_canal.transmission(event.packet, noise) 

            if (event.retransmission <= num_of_retransimssion2) and (event.retransmission >= 0): # sprawdzenie czy pakiet osiagnal limi transmisji
                # Sprawdzamy sumę kontrolną
                times.append([packet2, transmission_canal.not_free_to])
                if decoder.receive_package(packet2, coding): # sprawdzenie sumy kontrolnej
                    packet_out = decoder.remove_coding_bits(packet2, coding) # usuwanie sumy kontrolnej
                    received += packet_out
                    event.check_sum_correct = 1
                    for i in range(len(packet_out)): # sprawdzenie czy suma kontrolna zadziałała poprawnie
                        if packet_out[i] != event.packet[i]:
                            event.check_sum_correct = 0
                    result_queue.put(event)
                    continue
                else:
                    event.retransmission += 1
            else:
                received += decoder.remove_coding_bits(packet2, coding)
                times.append([packet2, transmission_canal.not_free_to])
                continue
        event.start_time += delta_time
        events_queue.put(event)

    global end_time
    for i in range(len(times)):
        event.start_time = event.duration
        if i + 1 == len(times):
            end_time = round(times[i][1] * 1000, 4)

    compare_signals(signal, received)
    return result_queue


def tests():
    with open('test_results.txt', 'w') as file:
        line = "Coding; p_len; retransmisions; s_len; noise; bandwidth; lose [%]; variancja [%]; time [us]; nr; id; lretrans; correct \n"
        file.write(line)
        for kod in range(4):
            coding = kod
            for c in range(1):

                num_of_retransmission = 50
                for p in [0.05, 0.1, 0.25, 0.5]:
                    packet_length = int(signal_length * p)
                    for noise in [0.1, 0.05, 0.01]:
                        for bandwidth in [1, 10, 100, 1000]:
                            lose = 0
                            time = 0
                            loses = []
                            for i in range(100):
                                lista2 = simulation(coding, packet_length, num_of_retransmission, signal_length, noise,
                                                    bandwidth)
                                while not lista2.empty():
                                    event = lista2.get()
                                    line = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12}\n".format(
                                        str(coding),
                                        str(packet_length),
                                        str(num_of_retransmission),
                                        str(signal_length),
                                        str(noise), str(bandwidth),
                                        str(round(stat, 2)),
                                        0,
                                        str(round(end_time, 4)), i,
                                        str(event.id),
                                        str(event.retransmission),
                                        str(event.check_sum_correct))
                                    file.write(line)
                                loses.append(stat)
                                lose += stat
                                time += end_time

                            squared_diff = [(x - lose / 100) ** 2 for x in loses]
                            variance = sum(squared_diff) / len(loses)

                            line = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12}\n".format(str(coding),
                                                                                                     str(packet_length),
                                                                                                     str(num_of_retransmission),
                                                                                                     str(signal_length),
                                                                                                     str(noise),
                                                                                                     str(bandwidth),
                                                                                                     str(round(
                                                                                                         lose / 100,
                                                                                                         2)),
                                                                                                     str(round(variance,
                                                                                                               2)),
                                                                                                     str(round(
                                                                                                         time / 100,
                                                                                                         4)), 1000, 0,
                                                                                                     0, 0)
                            file.write(line)
        file.close()


def distribution_tests():
    with open('test_results.txt', 'w') as file:
        line = "Coding; straty[%]; czas[us];\n"
        file.write(line)
        for i in range(4):
            for j in range(100):
                simulation(i, packet_length, num_of_retransmission, signal_length, noise, bandwidth)
                line = "{0}; {1}; {2};\n".format(str(i), str(stat), str(end_time))
                file.write(line)
        file.close()


if __name__ == '__main__':
    # Typy kodowania: 0 - bit parzystości, 1 - crc_8, 2 - crc_16, 3 - crc_32
    coding = 3
    # Długość  pakietu
    packet_length = 1
    # Ilość możliwych retransmisji
    num_of_retransmission = 1
    # Długość sygnału
    signal_length = 10
    # % na zaklocnenie pojedynczej paczki np 0.2 = 20 %
    noise = 0.5
    # Przepustowość medium w Mb
    bandwidth = 100

    simulation(coding, packet_length, num_of_retransmission, signal_length, noise, bandwidth)
    # distribution_tests()
    # tests()

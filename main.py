from queue import PriorityQueue
import random
import tkinter as tk

from Decoder import Decoder
from Event import Event
from Generator import Generator
from TransmissionCanal import TransmissionCanal


def compare_signals(signal_in, signal_out):
    """ Porównuje sygnały
        signal_in - sygnał wejściowy
        signal_out - sygnał wyjściowy """
    lost = 0
    for i in range(len(signal_in)):
        if signal_in[i] != signal_out[i]:
            lost += 1
    global stat
    # print("Sygnał wejściowy: ", signal_in)
    # print("Sygnał wyjściowy: ", signal_out)
    stat = lost / len(signal_in)
    stat = round(stat * 100, 2)
    return stat             # zwraca procent błędów BER


def simulation(coding, packet_length, num_of_retransmission, signal_length, noise, bandwith, type=0,
               bits_repetition_numb=0):

    ####
    # root = tk.Tk()
    # root.title("Packet Transmission Simulation")
    # canvas = tk.Canvas(root, width=1400, height=600)
    # canvas.pack()
    ####
    result_queue = PriorityQueue()
    generator = Generator(packet_length)
    decoder = Decoder()
    # encoder = CorrectionCoding()
    time = []
    events_queue = PriorityQueue()
    current_time = 0.5
    delta_time = 0.5
    liczba_retransmisji = 0
    numb_of_packages = signal_length / packet_length

    signal = generator.generate_signal(signal_length)
    received_signal = []

    packets, redundant_bits = generator.generate_package(signal, coding, type)


    transmission_canal = TransmissionCanal(bandwith)
    iter = 0

    for packet in packets:
        r1 = (random.randint(1, 5) / 34)
        r2 = (random.randint(1, 3) / 345)
        duration = r1 * r2 * len(packet) / bandwith
        event = Event(packet, current_time, duration)
        iter += 1

        event_id = iter
        events_queue.put(event)
        current_time += delta_time + (random.randint(1, 3) / 345) * (random.randint(1, 3) / 345)

    while not events_queue.empty():
        event = events_queue.get()
        if transmission_canal.is_free(event.start_time):
            transmission_canal.not_free_to += event.duration
            packet2 = transmission_canal.transmission(event.packet, noise, 'BER')
            time.append([packet2, transmission_canal.not_free_to])
            # Zdekodowanie kodów korekcyjnych - proba naprawy błedów
            if type == 0:
                packet2 = decoder.hamming_decode(packet2)
            elif type == 2:
                packet2 = decoder.bch_decode(packet2)
            elif type == 1:
                packet2 = decoder.repeat_decode(packet2, bits_repetition_numb)


            # Dekodowanie kodów detekcyjnych
            if decoder.receive_package(packet2, coding):
                packet_out = decoder.remove_coding_bits(packet2, coding)
                received_signal += packet_out
                result_queue.put(event)
                continue
            else:
                if event.retransmission <= num_of_retransmission:
                    event.retransmission += 1
                    liczba_retransmisji+= 1

                else:
                    result_queue.put(event)
                    received_signal += decoder.remove_coding_bits(packet2, coding)
                    time.append([packet2, transmission_canal.not_free_to])
                    continue
        event.start_time += delta_time
        events_queue.put(event)


    global end_time
    for i in range(len(time)):
        event.start_time = event.duration
        if i + 1 == len(time):
            end_time = round(time[i][1] * 1000, 4)

    compare_signals(signal, received_signal)
    return result_queue, redundant_bits, liczba_retransmisji


def tests():
    with open('test_results.txt', 'w') as file:
        line = "Coding; CodingFEC; p_len; retransmisions; s_len; extra bits; noise; bandwidth; lose [%]; variancja [%]; time [us] \n"
        file.write(line)
        for coding_fec in range(3):
            type = coding_fec
            for kod in range(4):
                coding = kod
                num_of_retransmission = 5
                for p in [0.05, 0.1, 0.25, 0.5]:
                    packet_length1 = int(signal_length * p)
                    for noise in [0.1, 0.05, 0.01]:
                        for bandwidth in [1, 10, 100, 1000]:
                            lose = 0
                            time = 0
                            loses = []
                            liczba_retransmisji = 0
                            for i in range(20):
                                lista2, extra_bits, liczba_retransmisji = simulation(coding, packet_length1, num_of_retransmission,
                                                                signal_length, noise,
                                                                bandwidth, type, bits_repetition_numb)

                                id = 0
                                while not lista2.empty():
                                    event = lista2.get()
                                    line = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(
                                        str(coding),
                                        str(type),
                                        str(packet_length1),
                                        str(liczba_retransmisji),
                                        str(signal_length),
                                        str(extra_bits),
                                        str(noise), str(bandwidth),
                                        str(round(stat, 2)),
                                        0,
                                        str(round(end_time, 4)), i,
                                        str(event.id),
                                        str(event.retransmission),
                                        str(event.check_sum_correct))
                                    #file.write(line)
                                loses.append(stat)
                                lose += stat
                                time += end_time

                            squared_diff = [(x - lose / 100) ** 2 for x in loses]
                            variance = sum(squared_diff) / len(loses)
                            var = liczba_retransmisji / 20  #srednia liczba retransmisji


                            line = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}\n".format(
                                str(coding),
                                str(type),
                                str(packet_length1),
                                str(var),
                                str(signal_length),
                                str(extra_bits),
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
    # Typ kodowania 0 - bit parzystości, 1 - CRC-8, 2 - CRC-16, 3 - CRC-32
    coding = 1
    # Typ kodowania korekcyjnego 0 - Hamming, 1 - BCH, 2 - repeat
    type = 0
    # Powtorzenia bitów
    bits_repetition_numb = 3
    # Długość pakietu
    packet_length = 10
    # Liczba możliwych retransmisji
    num_of_retransmission = 10
    # Długość sygnału
    signal_length = 1000
    # Szum w kanale - % na zakłócenie pojedynczej paczki np 0.2 = 20%
    noise = 0.01
    # Szerokość pasma w Mb
    bandwidth = 1000
    # Liczba powtórzeń symulacji
    num_of_repetition = 10

    # Symulacja
    wynik = 0

    # Srednia z wynikow
    # for i in range(num_of_repetition):
    #     wynik += simulation(coding, packet_length, num_of_retransmission, signal_length, noise, bandwidth, type, bits_repetition_numb)
    # print("Wynik: ", wynik / num_of_repetition, "%")

    tests()

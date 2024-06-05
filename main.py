from queue import PriorityQueue
import random

from Decoder import Decoder
from Event import Event
from Generator import Generator
from TransmissionCanal import TransmissionCanal
from CorrectionCoding import CorrectionCoding
from TransmissionGUI import TransmissionGUI


def compare_signals(signal_in, signal_out):
    """ Porównuje sygnały
        signal_in - sygnał wejściowy
        signal_out - sygnał wyjściowy
        zwraca - procent utraconych bitów"""

    min_length = min(len(signal_in), len(signal_out))
    lost = 0
    for i in range(min_length):
        if signal_in[i] != signal_out[i]:
            lost += 1

    # Uwzględnij brakujące bity w received_signal jako utracone bity
    lost += abs(len(signal_in) - len(signal_out))
    global stat
    # print("Sygnał wejściowy: ", signal_in)
    # print("Sygnał wyjściowy: ", signal_out)
    stat = lost / len(signal_in)
    stat = round(stat * 100, 2)
    return stat

# def simulation (coding, packet_length, num_of_retransmission, signal_length, noise, bandwidth, type = 0):
#     # Wynik symulacji
#     #[0] - liczba poprawnie odebranych pakietów
#     #[1] - liczba niepoprawnie odebranych pakietów
#     #[2] - liczba retransmisji
#     #[3] - procent poprawnie odebranych pakietów
#     #[4] - procent niepoprawnie odebranych pakietów
#     #[5] - procent retransmisji
#     #[6] - liczba nadmiarowych bitów
#     #[7] - liczba skorygowanych błędów
#     #[8] - liczba nieskorygowanych błędów
#     #[9] - czas symulacji
#     simulation_result = []
#
#
#     result_queue = PriorityQueue()
#     generator = Generator(packet_length)
#     decoder = Decoder()
#     time = []
#     events_queue = PriorityQueue()
#     current_time = 0.5
#     delta_time = 0.5
#     g1 = [1, 0, 1]
#     g2 = [1, 1, 1]
#
#     signal = generator.generate_signal(signal_length)
#     received_signal = []
#
#     packets = generator.generate_package(signal, coding, type)
#     transmission_canal = TransmissionCanal(bandwidth)
#
#    # gui = TransmissionGUI(bandwidth, packet_length, num_of_retransmission, noise)
#    # gui.start_simulation(packets)
#
#     iter = 0
#
#     redundant_bits = 0
#     corrected_errors = 0
#     uncorrected_errors = 0
#
#     for packet in packets:
#         r1 = (random.randint(1, 5) / 34)
#         r2 = (random.randint(1, 3) / 345)
#         duration = r1 * r2 * len(packet) / bandwidth
#         event = Event(packet, current_time, duration)
#         iter += 1
#
#         event_id = iter
#         events_queue.put(event)
#         current_time += delta_time + (random.randint(1, 3) / 345) * (random.randint(1, 3) / 345)
#
#     while not events_queue.empty():
#         event = events_queue.get()
#         if transmission_canal.is_free(event.start_time):
#             transmission_canal.not_free_to += event.duration
#             packet2 = transmission_canal.transmission(event.packet, noise)
#
#             time.append([packet2, transmission_canal.not_free_to])
#             corrected = 0
#             uncorrected = 0
#
#             if(type == 0):
#                 #packet2, corrected, uncorrected = decoder.hamming_decode(packet2)
#                 packet2 = decoder.hamming_decode(packet2)
#             if(type == 1):
#                 #packet2, corrected, uncorrected = decoder.repeating_decode(packet2)
#                 packet2 = decoder.repeating_decode(packet2)
#             if(type == 2):
#                 #packet2, corrected, uncorrected = decoder.bch_decode(packet2, 7, 3)
#                 packet2 = decoder.bch_decode(packet2, 7, 3)
#             if(type == 3):
#                 #packet2, corrected, uncorrected = decoder.convolutional_decoder(packet2, g1, g2)
#                 packet2 = decoder.convolutional_decoder(packet2, g1, g2)
#
#             corrected_errors += corrected
#             uncorrected_errors += uncorrected
#             redundant_bits += len(packet2) - len(event.packet)
#
#             if decoder.receive_package(packet2, coding):       #ZMIANA: DODAWNIE TYPE
#                 packet_out = decoder.remove_coding_bits(packet2, coding)        #ZMIANA: DODAWNIE TYPE
#                 received_signal += packet_out
#                 event.check_sum_if_correct = True
#                 for i in range (len(packet_out)):
#                     if packet_out[i] != event.packet[i]:
#                         event.check_sum_if_correct = False
#                 result_queue.put(event)
#                 continue
#             else:
#                 if event.retranmission <= num_of_retransmission:
#                     event.retranmission += 1
#                 else:
#                     result_queue.put(event)
#                     received_signal += decoder.remove_coding_bits(packet2, coding)        #ZMIANA: DODAWNIE TYPE
#                     time.append([packet2, transmission_canal.not_free_to])
#                     continue
#         event.start_time += delta_time
#         events_queue.put(event)
#
#     for i in range(len(time)):
#         event.start_time = event.duration
#         if i + 1 == len(time):
#             end_time = round(time[i][1] * 1000, 4)
#
#     stat = compare_signals(signal, received_signal)
#     return result_queue, stat, end_time, redundant_bits, corrected_errors, uncorrected_errors

def simulation (coding, packet_length, num_of_retransmission, signal_length, noise, bandwith, type = 0):
    result_queue = PriorityQueue()
    generator = Generator(packet_length)
    decoder = Decoder()
    correction_coding = CorrectionCoding()
    time = []
    events_queue = PriorityQueue()
    current_time = 0.5
    delta_time = 0.5

    signal = generator.generate_signal(signal_length)
    received_signal = []

    packets = generator.generate_package(signal, coding, type)
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
            packet2 = transmission_canal.transmission(event.packet, noise)

            time.append([packet2, transmission_canal.not_free_to])
            if type == 0:
                packet2 = decoder.hamming_decode(packet2)
            if type == 1:
                packet2 = correction_coding.repeat_decode(packet2, 3)
            #if type == 2:
                #packet2 = correction_coding.bch_decode(packet2)
            if type == 2:
                packet2 = correction_coding.convolutional_decoder(packet2, [1, 0, 1], [1, 1, 1])
            redundant_bits = 0
            redundant_bits += len(packet2) - len(event.packet)
            if decoder.receive_package(packet2, coding):
                packet_out = decoder.remove_coding_bits(packet2, coding)
                received_signal += packet_out
                event.check_sum_if_correct = True
                for i in range (len(packet_out)):
                    if packet_out[i] != event.packet[i]:
                        event.check_sum_if_correct = False
                result_queue.put(event)
                continue
            else:
                if event.retranmission <= num_of_retransmission:
                    event.retranmission += 1
                else:
                    result_queue.put(event)
                    received_signal += decoder.remove_coding_bits(packet2, coding)
                    time.append([packet2, transmission_canal.not_free_to])
                    continue
        event.start_time += delta_time
        events_queue.put(event)

    global end_time

    #return compare_signals(signal, received_signal)
    return redundant_bits


def tests():
    with open('test_results.txt', 'w') as file:
        line = "Coding; p_len; retransmisions; s_len; noise; bandwidth; lose [%]; variancja [%]; time [us]; redundant_bits; corrected_errors; uncorrected_errors; nr; id; lretrans; correct \n"
        file.write(line)
        for kod in range(4):
            coding = kod
            for typ in range(4):
                type = typ
                for c in range(1):
                    num_of_retransmission = 50
                    for p in [0.05, 0.1, 0.25, 0.5]:
                        packet_length = int(signal_length * p)
                        for noise in [0.1, 0.05, 0.01]:
                            for bandwidth in [1, 10, 100, 1000]:
                                lose = 0
                                time = 0
                                loses = []
                                # total_redundant_bits = 0
                                # total_corrected_errors = 0
                                # total_uncorrected_errors = 0

                                for i in range(100):
                                    lista2 = simulation(coding, packet_length, num_of_retransmission, signal_length,
                                                        noise,
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
                                                                                                         str(round(
                                                                                                             variance,
                                                                                                             2)),
                                                                                                         str(round(
                                                                                                             time / 100,
                                                                                                             4)), 1000,
                                                                                                         0,
                                                                                                         0, 0)

                                file.write(line)
        file.close()

def distribution_tests():
    with open('test_results.txt', 'w') as file:
        line = "Coding; straty[%]; czas[us];\n"
        file.write(line)
        for i in range(4):
            for j in range(100):
                _, stat, end_time, _, _, _ = simulation(i, packet_length, num_of_retransmission, signal_length, noise, bandwidth)
                line = "{0}; {1}; {2};\n".format(str(i), str(stat), str(end_time))
                file.write(line)
        file.close()




if __name__ == '__main__':
    # Typ kodowania 0 - bit parzystości, 1 - CRC-8, 2 - CRC-16, 3 - CRC-32
    coding = 2
    # Typ kodowania korekcyjnego 0 - Hamming, 1 - Powtarzające, 2 - BCH, 3 - Splotowe
    type = 0
    # Długość pakietu
    packet_length = 50
    # Liczba możliwych retransmisji
    num_of_retransmission = 5
    # Długość sygnału
    signal_length = 100
    # Szum w kanale - % na zakłócenie pojedynczej paczki np 0.2 = 20%
    noise = 0.2
    # Szerokość pasma w Mb
    bandwidth = 1000
    # Liczba powtórzeń symulacji
    num_of_repetition = 100


    # Symulacja
    wynik = 0 # Czy sygnał został poprawnie odebrany
    stat = 0
    redundant_bits_result = 0
    # Srednia z wynikow
    for packet in [50, 100, 200, 500, 1000]:
        for coding in range(4):
            for typ in range(2):
                wynik = 0  # Resetowanie wyniku dla każdej kombinacji
                for i in range(num_of_repetition):
                #     _, stat, _, _, _, _ = simulation(coding, packet, num_of_retransmission, signal_length, noise,
                #                                      bandwidth, typ)
                #     wynik += simulation(coding, packet, num_of_retransmission, signal_length, noise, bandwidth, typ)
                # print(packet, ":", coding, ":", typ,":", wynik / num_of_repetition, "%")
                    redundant_bits_result += simulation(coding, packet, num_of_retransmission, signal_length, noise, bandwidth, typ)
                print(packet, ":", coding, ":", typ, ":", redundant_bits_result / num_of_repetition)

    # simulation(coding, packet_length, num_of_retransmission, signal_length, noise, bandwidth, type)
    # distribution_tests()
    # tests()


    print("--------------------------------------------------------")
# Przykład użycia kodu korekcyjnego splotowego
    # Przykład użycia dekodera
    # Przykład użycia
    # data = '1011'
    # g1 = [1, 0, 1]
    # g2 = [1, 1, 1]
    #
    # correction = CorrectionCoding()
    # decoding = Decoder()
    # encoded_data = correction.convolutional_encoder(data, g1, g2)
    # decoded_data = decoding.convolutional_decoder(encoded_data, g1, g2)
    # print("Data:", data)
    # print("Encoded data:", encoded_data)
    # print("Decoded data:", decoded_data)


    # def correction_decode(self, encoded_data, type):
    #     if type == 0:
    #         self.hamming_decode(encoded_data)
    #     if type == 1:
    #         self.convolutional_decoder(encoded_data, g1, g2)
    #     if type == 2:
    #         self.bch_decode(encoded_data, n, t)


from queue import PriorityQueue
import random
from Decoder import Decoder
from Event import Event
from Generator import Generator
from TransmissionCanal import TransmissionCanal
from EventExtended import EventExtended


def compare_signals(signal_in, signal_out):
    """ Porównuje sygnały
        signal_in - sygnał wejściowy
        signal_out - sygnał wyjściowy """
    lost = 0
    for i in range(len(signal_in)):
        if signal_in[i] != signal_out[i]:
            lost += 1
    global stat, temp
    print("Sygnał wejściowy: ", signal_in)
    print("Sygnał wyjściowy: ", signal_out)

    stat = lost / len(signal_in)
    stat = round(stat * 100, 2)
    print("Procent błędów: ", stat, "%")

    return stat


def simulation(coding, packet_length, num_of_retransmission, signal_length, noise, bandwith, type=0,
               bits_repetition_numb=0):
    result_queue = PriorityQueue()
    generator = Generator(packet_length)
    decoder = Decoder()
    time = []
    events_queue = PriorityQueue()
    current_time = 0.5
    delta_time = 0.5
    liczba_retransmisji = 0
    signal = generator.generate_signal(signal_length)
    received_signal = []

    packets, redundant_bits = generator.generate_package(signal, coding, type)


    transmission_canal = TransmissionCanal(bandwith)
    iter = 0
    for packet in packets:
        r1 = (random.randint(1, 5) / 34)
        r2 = (random.randint(1, 3) / 345)
        duration = r1 * r2 * len(packet) / bandwith
        event_id = iter
        event = Event(packet, current_time, duration, event_id)
        iter += 1


        events_queue.put(event)
        current_time += delta_time + (random.randint(1, 3) / 345) * (random.randint(1, 3) / 345)

    while not events_queue.empty():
        event = events_queue.get()
        copy_of_packet = event.packet.copy()
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
                event.packet = packet_out
                result_queue.put(event)
                continue
            else:
                if event.retransmission <= num_of_retransmission:
                    event.retransmission += 1
                    liczba_retransmisji+= 1
                else:

                    received_signal += decoder.remove_coding_bits(packet2, coding)
                    event.packet = decoder.remove_coding_bits(packet2, coding)
                    result_queue.put(event)
                    time.append([packet2, transmission_canal.not_free_to])
                    continue
        event.start_time += delta_time
        events_queue.put(event)


    global end_time
    for i in range(len(time)):
        event.start_time = event.duration
        if i + 1 == len(time):
            end_time = round(time[i][1] * 1000, 4)

    received_signal2 = []
    retrunQueue = PriorityQueue()


    while result_queue.empty() == False:
        element = result_queue.get()
        returnElement = EventExtended(element.packet, element.start_time, element.duration, element.id)
        retrunQueue.put(returnElement)

    while not retrunQueue.empty():
        element = retrunQueue.get()
        received_signal2 +=element.packet

    compare_signals(signal, received_signal2)
    return retrunQueue, redundant_bits, liczba_retransmisji


def tests():
    signal_length = 1000
    with open('test_results.txt', 'w') as file:
        line = "Coding; CodingFEC; p_len; retransmisions; s_len; extra bits; noise; bandwidth; lose [%]; variancja [%]; time [us];retransmission \n"
        file.write(line)
        for num_of_retransmission in [5, 25, 125]:
            for coding_fec in range(3):
                type = coding_fec
                for kod in range(4):
                    coding = kod

                    for p in [0.05, 0.1, 0.25, 0.5]:
                        packet_length1 = int(signal_length * p)
                        for noise in [0.3, 0.2, 0.1]:
                            for bandwidth in [1, 10, 100, 1000]:
                                lose = 0
                                time = 0
                                loses = []
                                liczba_retransmisji = 0
                                for i in range(20):
                                    lista2, extra_bits, liczba_retransmisji = simulation(coding, packet_length1, num_of_retransmission, signal_length, noise, bandwidth, type, 3)


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


                                line = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11}\n".format(
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
                                        4)), num_of_retransmission, 1000, 0,
                                    0, 0)
                                file.write(line)
        file.close()


def menu():
    coding = input("Wybierz kodowanie: 0 - bit parzystości, 1 - CRC-8, 2 - CRC-16, 3 - CRC-32: ")
    type = input("Wybierz kodowanie korekcyjne: 0 - Hamming, 1 - repeat, 2 - BCH: ")
    if type == 1:
        bits_repetition_numb = input("Podaj liczbę powtórzeń bitów: ")
    else:
        bits_repetition_numb = 0
    packet_length = input("Podaj długość pakietu: ")
    num_of_retransmission = input("Podaj liczbę możliwych retransmisji: ")
    signal_length = input("Podaj długość sygnału: ")
    noise = 0.2
    bandwidth = input("Podaj szerokość pasma: ")

    simulation(int(coding), int(packet_length), int(num_of_retransmission), int(signal_length), noise,
               int(bandwidth), int(type), int(bits_repetition_numb))
if __name__ == '__main__':
    menu()
    #tests()

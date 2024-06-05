import tkinter as tk
from queue import PriorityQueue
import random
import copy

from TransmissionCanal import TransmissionCanal
from Event import Event  # Ensure Event is imported

class TransmissionGUI:
    def __init__(self, bandwidth, packet_length, num_of_retransmissions, noise):
        self.root = tk.Tk()
        self.root.title("Packet Transmission Simulation")
        self.canvas = tk.Canvas(self.root, width=1400, height=600)
        self.canvas.pack()
        self.bandwidth = bandwidth
        self.packet_length = packet_length
        self.num_of_retransmissions = num_of_retransmissions
        self.noise = noise
        self.current_time = 0.5
        self.delta_time = 0.5
        self.events_queue = PriorityQueue()
        self.transmission_canal = TransmissionCanal(bandwidth)

    def draw_packet(self, x, y, status):
        color = "green" if status == "accepted" else "red" if status == "corrupted" else "blue"
        self.canvas.create_rectangle(x, y, x + 20, y + 10, fill=color)

    def simulate_step(self):
        if not self.events_queue.empty():
            event = self.events_queue.get()
            self.current_time = event.start_time
            packet = event.packet
            duration = event.duration
            retransmission_count = event.retranmission

            if self.transmission_canal.is_free(self.current_time):
                self.transmission_canal.not_free_to += duration
                corrupted_packet = self.transmission_canal.transmission(packet, self.noise)

                x = int(self.current_time * 100)
                y = retransmission_count * 20 + 50
                status = "accepted" if corrupted_packet == packet else "corrupted"
                self.draw_packet(x, y, status)

                if corrupted_packet != packet and retransmission_count < self.num_of_retransmissions:
                    retransmission_count += 1
                    new_event = Event(packet, self.current_time + self.delta_time, duration)
                    new_event.retranmission = retransmission_count
                    self.events_queue.put(new_event)

            self.current_time += self.delta_time
            self.root.after(100, self.simulate_step)  # Continue simulation after 100 ms

    def start_simulation(self, packets):
        current_time = 0.5
        delta_time = 0.5

        for packet in packets:
            duration = (random.randint(1, 5) / 34) * (random.randint(1, 3) / 345) * len(packet) / self.bandwidth
            event = Event(packet, current_time, duration)  # Correct instantiation of Event
            self.events_queue.put(event)
            current_time += delta_time + (random.randint(1, 3) / 345) * (random.randint(1, 3) / 345)

        self.simulate_step()
        self.root.mainloop()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Inicjalizacja danych
packet_sequence = [(1, 'Sent'), (1, 'Lost'), (1, 'Retransmitted'), (1, 'Received')]
packet_colors = {'Sent': 'blue', 'Lost': 'red', 'Retransmitted': 'orange', 'Received': 'green'}

# Inicjalizacja animacji
fig, ax = plt.subplots()
ax.set_xlim(0, 4)
ax.set_ylim(0, 2)
ax.set_xlabel('Czas')
ax.set_ylabel('Numer paczki')
ax.set_title('Symulacja transmisji pojedynczego pakietu')

# Funkcja inicjalizująca animację
def init():
    return []

# Funkcja animacji
def animate(i):
    ax.clear()
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2)
    ax.set_xlabel('Czas')
    ax.set_ylabel('Numer paczki')
    ax.set_title('Symulacja transmisji pojedynczego pakietu')

    for packet, status in packet_sequence[:i]:
        color = packet_colors.get(status, 'black')
        # Obliczanie położenia paczki w czasie
        y_pos = 1 if status == 'Received' else 0
        ax.plot([i-0.5, i+0.5], [y_pos, y_pos], color=color, lw=2, label=status)
        ax.text(i+0.5, y_pos, f'Paczka {packet}\n({status})', verticalalignment='center')

    ax.legend(loc='upper left')

# Tworzenie animacji
ani = FuncAnimation(fig, animate, frames=len(packet_sequence)+1, init_func=init, blit=True)

plt.show()

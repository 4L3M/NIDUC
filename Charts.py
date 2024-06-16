import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from docutils.languages.af import labels

# Read data from a CSV file
file_path = 'wyniki_niduc_BER_1.csv'  # Change this to the path of your file
df = pd.read_csv(file_path, sep=';')

# Wyswietlenie do sprawdzenia
print(df)

# Usuń zbędne spacje i zamień nazwy kolumn na małe litery
df.columns = df.columns.str.strip().str.lower()

# Funkcja do obliczania procentu poprawnie przesłanych pakietów
def correctly_transmitted_percentage(data):
    return 100 - data['lose [%]']

# Pobierz unikalne kody FEC
fec_codes = df['codingfec'].unique()

# Tworzenie wykresów dla każdego kodu FEC
for fec_code in fec_codes:
    fec_data = df[df['codingfec'] == fec_code]
    packet_sizes = sorted(fec_data['p_len'].unique())



    # Przygotuj dane do wykresu
    detection_methods = fec_data['coding'].unique()
    correctly_transmitted = {method: [] for method in detection_methods}

    for p_len in packet_sizes:
        for method in detection_methods:
            data = fec_data[(fec_data['p_len'] == p_len) & (fec_data['coding'] == method)]
            if not data.empty:
                correctly_transmitted[method].append(correctly_transmitted_percentage(data).values[0])
            else:
                correctly_transmitted[method].append(0)

    # Rysowanie wykresów
    fig, ax = plt.subplots(figsize=(12, 8))

    bar_width = 0.15
    index = range(len(packet_sizes))

    label = []
    label = ['Bit parzystosci', 'CRC-8', 'CRC-16', 'CRC-32']


    for i, method in enumerate(detection_methods):
        ax.bar([x + i * bar_width for x in index], correctly_transmitted[method], bar_width,
               label=label[i])

    # Ustawienia tytułu i etykiet

    if fec_code == 0:
        ax.set_title(f'Procent poprawnie przesłanych pakietów z zastosowaniem kodu Hamminga')
    elif fec_code == 1:
        ax.set_title(f'Procent poprawnie przesłanych pakietów z zastosowaniem kodu BCH')
    elif fec_code == 2:
        ax.set_title(f'Procent poprawnie przesłanych pakietów z zastosowaniem kodu powtórzeń (3 krotne)')

#    ax.set_title(f'Procent poprawnie przesłanych pakietów dla kodu FEC {fec_code}')
    ax.set_xlabel('Długość pakietu')
    ax.set_ylabel('Procent poprawnie przesłanych pakietów')
    ax.set_xticks([x + bar_width * (len(detection_methods) / 2) for x in index])
    ax.set_xticklabels(packet_sizes)
    # Przesunięcie legendy na bok
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Wyświetlanie wykresu
    plt.tight_layout()
    plt.show()

#1. BER
# Hamming - porownanie blednych transmisji dla roznych kodow detekcyjnych

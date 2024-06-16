import pandas as pd
import re

# Wczytaj dane z pliku tekstowego
with open('C:\\Users\\Amelia\\Desktop\\NIDUC WYNIKI\\grupowe_5.txt', 'r') as file:
    data = file.read()

# Podziel dane na linie
lines = data.strip().split('\n')
# Podziel pierwszą linię na nagłówki
headers = lines[0].split('; ')

# Przetwórz każdą linię danych
rows = []
for line in lines[1:]:
    row = line.split(';')
    row = [re.sub(r'\s+', '', item) for item in row]  # Usuń nadmiarowe spacje
    rows.append(row)

# Stwórz DataFrame z danych
df = pd.DataFrame(rows, columns=headers)

# Zapisz dane do pliku Excel
df.to_excel('C:\\Users\\Amelia\\Desktop\\NIDUC WYNIKI\\grupowe_5.xlsx', index=False)

print("Dane zostały zapisane do 'C:\\Users\\Amelia\\Desktop\\NIDUC WYNIKI\\grupowe_5.xlsx'")

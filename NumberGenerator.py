import time


class PseudoRandGenerator:
    def __init__(self, a=1103515245, c=12345, m=2**32, seed=None, bit_len=2):
        self.a = a
        self.c = c
        self.m = m
        self.x0 = seed
        self.bit_len = bit_len
        self.x_prev = self.x0

    def gen_number(self, range_start, range_end):
        self.x_prev = (self.a * self.x_prev + self.c) % self.m

        if range_start is None or range_end is None:
            return self.x_prev
        else:
            return int((self.x_prev / (self.m - 1)) * (range_end - range_start) + range_start)


    def binary_number(self, length):
        signal = []
        for _ in range(length):
            rand_num = self.gen_number(0, 2**self.bit_len)
            bin_num = bin(rand_num)[2:].zfill(self.bit_len)
            signal.append(bin_num)
        return signal

# Przykład użycia:
rand = PseudoRandGenerator(seed = time.time())
signal = rand.binary_number(4)
for binary in signal:
    print(binary)

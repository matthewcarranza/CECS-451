import random
import time
from board import Board


def genetic():
    h_vals = []
    codes = []

    for i in range(8):
        board = Board(5)
        codes.append(board.encode())
        h = 10 - board.get_fitness()
        if h == 10:
            return codes[i].decode()
        h_vals.append(h)

    while True:
        s = sum(h_vals)
        checkpoints = []
        check = 0

        for i in range(7):
            h_vals[i] = round((h_vals[i] / s), 2)
            check += h_vals[i]
            checkpoints.append(round(check, 2))
        checkpoints.append(1.00)

        pairs = []
        for _ in range(8):
            r = random.random()
            for i in range(8):
                if r < checkpoints[i]:
                    pairs.append(codes[i])
                    break

        crossover = []
        for i in range(4):
            split = random.randint(0, 4)

            crossover.append(pairs[i * 2][:split] + pairs[(i * 2) + 1][split:])
            crossover.append(pairs[(i * 2) + 1][:split] + pairs[i * 2][split:])

        mutated = []
        for i in range(8):
            m = random.randint(0, 4)
            new = crossover[i][0:m] + str(random.randint(0, 4)) + crossover[i][m + 1:]
            mutated.append(new)
        h_vals = []
        codes = []
        for code in mutated:
            new_board = Board(5)
            new_board.decode(code)
            codes.append(code)
            h = 10 - new_board.get_fitness()
            if h == 10:
                return new_board
            h_vals.append(h)


if __name__ == "__main__":
    start_time = time.time()
    b = genetic()
    print(f"Running time: {((time.time() - start_time)*1000):.2f}ms")
    b.print_map()

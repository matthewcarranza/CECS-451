from board import Board
import time


def get_neighbors(board):
    neighbors = []
    for col in range(board.n_queen):
        current_row = board.map[col].index(1)
        for new_row in range(board.n_queen):
            if new_row != current_row:
                neighbor = Board(board.n_queen)
                neighbor.decode(board.encode())
                neighbor.flip(col, current_row)
                neighbor.flip(col, new_row)
                neighbors.append(neighbor)
    return neighbors


def _hill_climbing(board):
    current_board = board
    current_fitness = current_board.get_fitness()
    while True:
        neighbors = get_neighbors(current_board)
        best_neighbor = neighbors[0]
        for neighbor in neighbors[1:]:
            if neighbor.get_fitness() < best_neighbor.get_fitness():
                best_neighbor = neighbor
        best_neighbor_fitness = best_neighbor.get_fitness()

        if best_neighbor_fitness >= current_fitness:
            return current_board

        current_board = best_neighbor
        current_fitness = best_neighbor_fitness


def hill_climbing(max_restarts):
    for restart in range(max_restarts):
        initial_board = Board(5)
        result_board = _hill_climbing(initial_board)
        if result_board.get_fitness() == 0:
            return result_board
    return None


if __name__ == "__main__":
    start_time = time.time()
    solution = hill_climbing(100)
    print(f"Running time: {((time.time() - start_time)*1000):.2f}ms")
    solution.print_map()

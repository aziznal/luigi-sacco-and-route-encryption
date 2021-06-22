
from typing import List, Tuple


def get_divisors(number: int) -> List[int]:
    """
    Returns all positive integers that divide given number without remainder
    (including the number itself)
    """
    return [divisor for divisor in range(1, number+1) if number % divisor == 0]


def get_potential_table_sizes(message_length: int, verbose: bool = False) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
    """
    Returns a Tuple where the first element is a list of all potential sizes for
    the given message length and the second element is the optimal size
    """

    if verbose:
        print(f"Got message with size = {message_length}")

    # Need to get all divisors of the given message length
    divisors = get_divisors(message_length)
    reverse_divisors = divisors[::-1]

    potential_table_sizes = [(i, j)
                             for i, j in zip(divisors, reverse_divisors)]

    if verbose:
        print("\nPotential Sizes for Table:")
        for i, j in potential_table_sizes:
            print(f"{i} x {j}")

    # Optimal size is when the difference between row counts and column counts is minimized
    optimal_size = min(potential_table_sizes, key=lambda x: abs(x[0]-x[1]))

    if verbose:
        print(f"\nOptimal Size = {optimal_size}")

    return potential_table_sizes, optimal_size


def create_empty_matrix(table_size: Tuple[int, int], verbose: bool = False) -> List[List[str]]:
    """
    Create matrix with the given size, filled with placeholder values
    """
    if verbose:
        print(f"\nCreating empty matrix with size {table_size[0]} x {table_size[1]}")

    return [['_' for col in range(table_size[1])] for row in range(table_size[0])]


def get_matrix_diags(matrix: List[List[str]]) -> List[Tuple[int, int]]:
    """
    Returns a list of all the diagonals for the given matrix appropriate to the
    e4 route. The diagonals are returned in order and can be traversed to form
    the message or decrypt an e4 matrix.
    """
    row_count, col_count = len(matrix), len(matrix[0])

    diags = []
    # Every element in the last column is the start of a diagonal
    # List is reversed to keep order of diagonals
    for i in list(range(row_count))[::-1]:
        diags.append((i, col_count-1))

    # Every element in the first row is also the start of a diagonal
    for j in list(range(col_count))[::-1]:
        if (0, j) not in diags:
            diags.append((0, j))

    return diags


def apply_e4(message: str, empty_matrix: List[List[str]]) -> List[List[str]]:
    """
    Distributes letters of given message across empty matrix according to E4
    route
    """
    row_count, col_count = len(empty_matrix), len(empty_matrix[0])

    # Copying given matrix
    matrix = [[element for element in row] for row in empty_matrix]

    # Iterator is used to easily distribute chars of message across matrix
    message_iterator = iter(message)

    diags = get_matrix_diags(matrix)

    for diag_head in diags:

        i, j = diag_head

        while i <= row_count-1 and j >= 0:
            matrix[i][j] = next(message_iterator)
            i += 1
            j -= 1

    return matrix


def apply_b3(matrix: List[List[str]]) -> str:
    """
    Creates encrypted message by following route in given matrix. Implemented
    according to B3 route
    """
    row_count, col_count = len(matrix), len(matrix[0])

    message = []

    # Iterate over all columns. The message starts from the end of the column to its top
    for col in range(col_count):
        # Iterate rows starting from bottom
        for row in list(range(row_count))[::-1]:
            message.append(matrix[row][col])

    return ''.join(message)


def apply_reverse_b3(message: str, table_size: Tuple[int, int]) -> List[List[str]]:
    """
    Applies a reverse version of B3 to distribute letters of given message
    across a matrix with the given table size
    """
    row_count, col_count = table_size

    # Create matrix with correct number of columns and rows
    matrix = create_empty_matrix(table_size)

    # Iterator is used to easily distribute message letters across matrix
    message_iterator = iter(message)

    for col in range(col_count):
        for row in list(range(row_count))[::-1]:
            matrix[row][col] = next(message_iterator)

    return matrix


def apply_reverse_e4(matrix: List[List[str]]) -> str:
    """
    Applies reverse E4 route algorithm to extract message from given matrix
    """
    row_count, col_count = len(matrix), len(matrix[0])

    message = ""

    diags = get_matrix_diags(matrix)

    for diag_head in diags:

        i, j = diag_head

        while i <= row_count-1 and j >= 0:
            message += matrix[i][j]
            i += 1
            j -= 1

    return message


def route_encrypt(message: str, table_size: Tuple[int, int], verbose: bool = False) -> str:
    """
    Encrypts given message across a matrix with given table size according to E4 & B3 methods.
    """
    if verbose:
        print(f"Creating empty matrix")

    empty_e4_matrix = create_empty_matrix(table_size, verbose=verbose)

    if verbose:
        print("\n\nEmpty Matrix\n")
        [print(f"{row}") for row in empty_e4_matrix]

    populated_e4_matrix = apply_e4(message, empty_e4_matrix)

    if verbose:
        print("\n\nE4 Matrix\n")
        [print(row) for row in populated_e4_matrix]

    b3_message = apply_b3(populated_e4_matrix)

    return b3_message


def route_decrypt(input_text: str, table_size: Tuple[int, int], verbose: bool = False) -> str:
    """
    Decrypts given message according to given table size. Follows reverse E4 & B3 routes.
    """

    e4_matrix = apply_reverse_b3(input_text, table_size)

    if verbose:
        print("\n\nInferred E4 Matrix:")
        [print(row) for row in e4_matrix]

    message = apply_reverse_e4(e4_matrix)

    return message


def execute_tests() -> None:
    """
    Simple Test Suite to test multiple messages across multiple different table sizes.
    """

    messages = [
        "Here is a normal message",
        "Now here is a very long message that is quite cumbersome to write and may in fact cause the program the crash if it hadn't been written with this kind of message in mind",
        "short",
        "how's about we uses a few numbers and symbols?"
    ]

    total = 0
    total_correct = 0

    faulty_tests = []

    for message in messages:

        sizes, _ = get_potential_table_sizes(len(message))

        for size in sizes:

            encrypted_message = route_encrypt(message, size, verbose=False)
            decrypted_message = route_decrypt(
                encrypted_message, size, verbose=False)

            total += 1

            if message.replace(' ', '') == decrypted_message.replace(' ', ''):
                total_correct += 1

            else:
                faulty_tests.append((message, size))

    print(f"\nGot {total_correct} correct out of {total}")

    if faulty_tests:
        print("\n")
        [print(row) for row in faulty_tests]


if __name__ == '__main__':

    execute_tests()

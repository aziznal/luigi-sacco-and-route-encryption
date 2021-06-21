
from common import ENGLISH_ALPHABET, TURKISH_ALPHABET


def get_divisors(number):
    return [divisor for divisor in range(1, number+1) if number % divisor == 0]


def get_potential_table_sizes(message_length, verbose=False):

    print(f"Got message with size = {message_length}")

    # Need to get all divisors of the given message length
    divisors = get_divisors(message_length)
    reverse_divisors = divisors[::-1]

    potential_table_sizes = [(i, j) for i, j in zip(divisors, reverse_divisors)]

    if verbose:
        print("\nPotential Sizes for Table:")
        for i, j in potential_table_sizes:
            print(f"{i} x {j}")

    # Optimal size is when the difference between row counts and column counts is minimized
    optimal_size = min(potential_table_sizes, key= lambda x: abs(x[0]-x[1]))

    if verbose:
        print(f"\nOptimal Size = {optimal_size}")

    return potential_table_sizes, optimal_size



def create_empty_matrix(table_size, verbose=False):
    if verbose:
        print(f"\nCreating empty matrix with size {table_size[0]} x {table_size[1]}")

    return [ [ '_' for column in range(table_size[1]) ] for row in range(table_size[0]) ]



def populate_e4(message, empty_matrix):
    row_count, col_count = len(empty_matrix), len(empty_matrix[0])

    return empty_matrix



def populate_b3(message, matrix):
    row_count, col_count = len(matrix), len(matrix[0])
    return matrix



def create_matrix(message, table_size, verbose=True):
    """
    Create matrix with the given size, filled with placeholder values
    """

    if verbose:
        print(f"Creating empty matrix")
        
    empty_matrix = create_empty_matrix(table_size, verbose=verbose)

    if verbose:
        print("\n")
        [print(f"{row}") for row in empty_matrix]


    # Now the matrix must be populated with the letters of the message

    e4_matrix = populate_e4(message, empty_matrix)

    print("\n\nE4 Matrix\n")
    [print(row) for row in e4_matrix]


    e4_message = ''.join( ''.join(row) for row in e4_matrix)

    print("\n\nE4 Message\n")
    print(e4_message)


    b3_matrix = populate_b3(e4_message, empty_matrix)

    print("\n\nB3 Matrix\n")
    [print(row) for row in b3_matrix]

    b3_message = ' '.join( ''.join(row) for row in e4_matrix)

    print("\n\nB3 Message\n")
    print(b3_message)

    return b3_message


def route_encrypt(input_text, table_size, verbose=True):
    pass


def route_decrypt(input_text, table_size, verbose=True):
    pass


if __name__ == '__main__':

    # TODO: If message length is prime, either inform user or automatically add extra letter to make its length non-prime

    msg = "KALEMKILIÇTANÜSTÜNDÜR"

    sizes, optimal_size = get_potential_table_sizes(len(msg))

    matrix = create_matrix(msg, optimal_size)

    # route_encrypt()

    # route_decrypt()

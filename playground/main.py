import string

TURKISH_ALPHABET = {letter: letter_index for letter_index,
                    letter in enumerate("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ")}

ENGLISH_ALPHABET = {letter: letter_index for letter_index,
                    letter in enumerate(string.ascii_uppercase)}

def custom_sort(iterable, lang):
    if lang == "TR":
        return sorted(
            iterable,
            key=lambda i: TURKISH_ALPHABET.get(i[0])
        )

    elif lang == "EN":
        return sorted(
            iterable,
            key=lambda i: ENGLISH_ALPHABET.get(i[0])
        )

    else:
        raise ValueError(f"Unsupported Language ({lang})")


def get_letter_index_pairs(key, lang):

    # Used a list here instead of a dict to account for repeating letters in given Key
    if lang == "TR":
        return [ [letter, TURKISH_ALPHABET[letter]] for letter in key]

    elif lang == "EN":
        return [ [letter, ENGLISH_ALPHABET[letter]] for letter in key]

    else:
        raise ValueError(f"Unsupported Language ({lang})")


def order_key(key, lang):

    letter_index_pairs = get_letter_index_pairs(key, lang)

    # Get column numbers based on alphabetical order of key

    # NOTE
    #   if key has repeating letters, then recurring letters are numbered
    #   sequentially in order of appearance in key

    for letter_index, pair in enumerate(custom_sort(letter_index_pairs, lang)):
        pair[1] = letter_index + 1

    return [letter_index_pairs.index(pair) + 1 for pair in custom_sort(letter_index_pairs, lang)]


def get_transposed(matrix):
    return list(map(list, zip(*matrix)))


def luigi_sacco_encrypt(key, plain_text, lang="TR", verbose=False):

    # Remove all spaces and symbols and capitalize text
    plain_text = plain_text.replace(' ', '')
    plain_text = plain_text.upper()
    for symbol in string.punctuation:
        plain_text = plain_text.replace(symbol, '')

    # Get column splits from key
    splits = order_key(key, lang)
    key_length = len(splits)

    if verbose:
        print("\nKey Length: ")
        print(key_length)

    # NOTES
    #   I could probably get away with not splitting a very message into multiple
    #   bits if I can get gud with matrix operations
    #
    #   A Row will NEVER be longer than the length of the key by definition of this encryption method
    #
    #   Columns may be longer than the key length depending on length of plain text 

    initial_matrix = []

    while len(plain_text) > 0:

        for split in splits:
            message_row = []
            while split != 0:
                try:
                    message_row.append(plain_text[0])
                    plain_text = plain_text[1:]
                    split -= 1

                # TODO: check how sturdy this actually is
                except IndexError:
                    break
                
            filler = ['_' for i in range(key_length - len(message_row))]
            initial_matrix.append(message_row + filler)

    # Must fill up 'empty spaces' in message matrix to be able to get the final form
    max_row_length = len(max(initial_matrix, key=len))
    
    for row in initial_matrix:
        while len(row) < max_row_length:
            row.append('_')

    if verbose:
        print("\nInitial Matrix")
        [print(row) for row in initial_matrix]

    # Transposing to make extracting final message easier
    transposed_matrix = get_transposed(initial_matrix)

    if verbose:
        print("\nTransposed Matrix")
        [print(row) for row in transposed_matrix]

    # Pick the words of the message in the order provided by the splits.
    
    final_message_matrix = []

    for row_index in splits:
        if row_index <= len(transposed_matrix):
            final_message_matrix.append(transposed_matrix[row_index - 1])

    # final_message_matrix = [transposed_matrix[row-1] for row in splits if row <= len(transposed_matrix)]

    if verbose:
        print(splits)
        print("\nFinal Message Matrix")
        [print(row) for row in final_message_matrix]
    
    # Removing underscores and joining message together
    final_message = ' '.join([''.join(row).replace('_', '') for row in final_message_matrix])

    return final_message



def get_indices_of_extra_letters(row, split):

    row_without_placeholder = ''.join(char for char in row if char != '_')
    difference = len(row_without_placeholder) - split
    
    if difference <= 0:
        return []

    # indices_of_extra_letters = [i for i in range(split, split + difference)]
    indices_of_extra_letters = [ row.index(letter) for letter in row[split:] if letter!='_' ]

    # print(f"\nExtra indices in {row} are {indices_of_extra_letters}")

    return indices_of_extra_letters


def recursive_push_down(matrix, row, index_of_letter_to_be_pushed_down):

    # If space is empty, then just set character where it needs to go:
    if matrix[row + 1][index_of_letter_to_be_pushed_down] == '_':
        matrix[row + 1][index_of_letter_to_be_pushed_down] = matrix[row][index_of_letter_to_be_pushed_down]
        matrix[row][index_of_letter_to_be_pushed_down] = '_'

    # Else, push the below character to the row below itself
    else:
        recursive_push_down(matrix, row + 1, index_of_letter_to_be_pushed_down)


def push_down(matrix, row, split):
    # indices_of_extra_letters = [i for i in range(split, len(matrix[row]))]
    indices_of_extra_letters = get_indices_of_extra_letters(matrix[row], split)
    
    for i in indices_of_extra_letters:

        try:
            recursive_push_down(matrix, row, i)

        except:
            pass
        

def super_sophisticated_matrix_transformation_algorithm(matrix, splits, verbose):

    # Starting from first row, make sure there are only as many chars in it as the split

    # 'PUSH' down any extra characters in the row to the row below it

    # If the row below it has characters filling up the space where we want to push
    # the extra characters from below, then push them down as well.

    # Copying matrix to avoid changing the passed in matrix
    matrix = [ [element for element in row] for row in matrix ]

    # NOTE: if we had a long message, we'd have more rows than there are splits.
    # and this code would fail. Solution is to divide message into 6 row matrices whenever
    # is longer than 6 rows, and apply this algorithm on each of those matrices.

    # while len([char for char in matrix[-1] if char != '_']) != splits[-1]:

    for _ in range(10):
        for (i, row), split in zip(enumerate(matrix), splits):
            if len(row) != split:
                push_down(matrix, i, split)

    if verbose:
        print("\n\n")
        [print(row) for row in matrix]

    return matrix


def luigi_sacco_decrypt(key, encrypted_text, lang="TR", verbose=False):
    
    splits = order_key(key, lang)
    
    if verbose:
        print(splits)

    encrypted_text = encrypted_text.split(' ')

    transposed_matrix = [ [] for _ in range(len(splits)) ]

    for word, split in zip(encrypted_text, splits):
        # Split word in character list and assign to relevant column
        transposed_matrix[split - 1] = [char for char in word]


    # Filling in empty spaces with '_' to transpose matrix (because function has
    # trouble with 'jagged' matrices)
    max_row_length = len(max(transposed_matrix, key=len))

    for row in transposed_matrix:
        while len(row) < max_row_length:
            row.append('_')

    if verbose:
        print("\nTransposed Matrix")
        [print(row) for row in transposed_matrix]

    initial_matrix = get_transposed(transposed_matrix)

    if verbose:
        print("\n")
        [print(row) for row in initial_matrix]

    # Clearing the '_' to make next step easier
    # initial_matrix = [ [element for element in row if element != '_'] for row in initial_matrix]

    final_matrix = super_sophisticated_matrix_transformation_algorithm(initial_matrix, splits, verbose)

    return ''.join([''.join(row).replace('_', '') for row in final_matrix])



def test_program(key, plain_text, lang="TR"):

    encrypted_message = luigi_sacco_encrypt(key, plain_text, lang=lang, verbose=True)
    decrypted_message = luigi_sacco_decrypt(key, encrypted_message, lang=lang, verbose=False)


    print(f"\n\n\nOriginal Message:")
    print("\n\t" + plain_text)
    
    print("\n\nEncrypted Message: ")
    print("\n\t" + encrypted_message, end='')
    if len(encrypted_message.replace(' ' ,'')) == len(plain_text.replace(' ', '')):
        print(" (Lengths match)")
    else:
        print(" (Lengths DON'T match)")

    print("\n\nDecrypted Message: ")
    print("\n\t" + decrypted_message)

    print("\nHas been decoded correctly?")
    if decrypted_message.replace(' ', '') == plain_text.replace(' ', ''):
        print("\n\tYes!")

    else:
        print("\n\tNope :'(")



if __name__ == '__main__':

    
    # FIXED: if given text is too long, then not all of it is getting encrypted.
    # FIXME: if key is too long, some weird stuff is happening
    # FIXME: having repeated letters in a key ruins the decryption process
    # TODO: create a big test for encryption and decryption

    # key = "TERAZİ"
    # plain_text = "ADALET MÜLKÜN TEMELİDİR"


    # key = "CONVENIENCE"
    # plain_text = "HERE IS A SECRET MESSAGE ENCIPHERED BY TRANSPOSITION"

    key = "SPANISHINQUISITION"
    plain_text = "NO ONE EXPECTS THE SPANISH INQUISITION"


    # key = "AZİZNALISMYNAME"
    # key = "AZİZNAL"
    # plain_text = "BUGÜN ÇOK İYİ BİR GÜN OLACAK"


    # test_program(key, plain_text, lang="EN")
    test_program(key, plain_text, lang="TR")

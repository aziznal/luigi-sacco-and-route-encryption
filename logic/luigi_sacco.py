import string
import traceback


from typing import Iterable, Literal, Union, List, Tuple

from .common import TURKISH_ALPHABET, ENGLISH_ALPHABET


def custom_sort(iterable: Iterable, lang: Literal["EN", "TR"]) -> Iterable:
    """
    Alphabetically sorts given iterable according to given lang parameter
    """
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


def get_letter_index_pairs(key: str, lang: Literal["EN", "TR"]) -> List[ Tuple[str, str] ]:
    """
    Returns a list of tuples where the first element in each tuple is a letter from the given key
    and the second element is the position of that letter in the alphabet of the given langauge
    """

    if lang not in ["TR", "EN"]:
        raise ValueError(f"Unsupported Language ({lang})")

    # Used a list here instead of a dict to account for repeating letters in given Key
    if lang == "TR":
        return [[letter, TURKISH_ALPHABET[letter]] for letter in key]

    elif lang == "EN":
        return [[letter, ENGLISH_ALPHABET[letter]] for letter in key]


def order_key(key: str, lang: Literal["EN", "TR"]) -> List[int]:

    letter_index_pairs = get_letter_index_pairs(key, lang)

    # NOTE
    #   if key has repeating letters, then recurring letters are numbered
    #   sequentially in order of appearance in key

    # Get column numbers based on alphabetical order of key
    for letter_index, pair in enumerate(custom_sort(letter_index_pairs, lang)):
        pair[1] = letter_index + 1

    return [letter_index_pairs.index(pair) + 1 for pair in custom_sort(letter_index_pairs, lang)]


def get_transposed(matrix: List[List['str']]) -> List[List['str']]:
    """
    Returns transpose of given matrix
    """
    return list(map(list, zip(*matrix)))


def get_indices_of_extra_letters(row: List[str], split: int, key_length: int) -> List[int]:
    """
    Returns indices of all letters which don't belong in a row because they make its length bigger
    than the given split.
    """

    row_without_placeholder = ''.join(char for char in row if char != '_')
    difference = len(row_without_placeholder) - split

    difference = key_length - split

    if difference == 0:
        return []

    # Extra letter indices start from the split's index and go till the end of that row
    indices_of_extra_letters = [i for i in range(split, key_length)]

    # Remove indices of '_' placeholders, and make sure the indices list is only
    # as long as the original key
    indices_of_extra_letters = [e for e in indices_of_extra_letters[:key_length] if row[e] != '_']

    return indices_of_extra_letters


def recursive_push_down(matrix: List[List['str']], row: int, index_of_letter_to_be_pushed_down: int) -> None:
    """
    Recursive function to push down a given element in a matrix one row down.

    If there is another element below the given element, then it is recursively
    pushed down first.

    WARNING: This has not been tested if the entire column below the given element is full.
    """

    # Check if below space is empty or not (empty means '_')
    if matrix[row + 1][index_of_letter_to_be_pushed_down] != '_':
        recursive_push_down(matrix, row + 1, index_of_letter_to_be_pushed_down)

    # Place given element to at the row below its current row, and replace its
    # original position with the placehoder '_'
    matrix[row + 1][index_of_letter_to_be_pushed_down] = matrix[row][index_of_letter_to_be_pushed_down]
    matrix[row][index_of_letter_to_be_pushed_down] = '_'


def push_down(matrix: List[List['str']], row: int, split: int, verbose: bool, key_length: int):
    """
    Pushes all extra letters in given row of given matrix down one row.
    """

    # Get extra letter indices for this current row
    indices_of_extra_letters = get_indices_of_extra_letters(matrix[row], split, key_length)

    # Push each of these extra letters down one row
    for i in indices_of_extra_letters:

        recursive_push_down(matrix, row, i)

        if verbose:
            print(f"\t\t\n\n\nIteration {i}")
            [print(row) for row in matrix]


def distribute_letters_across_matrix(matrix: List[List['str']], splits: List[int], verbose: bool) -> List[List['str']]:
    """
    Algorithm works as follows:
        Starting from first row, make sure there are only as many chars in it as the split

        'PUSH' down any extra characters in the row to the row below it

        If the row below has characters filling up the space where we want to push
        the extra characters, then push them down as well.

    """

    # Copying matrix to avoid changing the passed in matrix
    matrix = [[element for element in row] for row in matrix]

    # NOTE
    #   if we had a long message, we'd have more rows than there are splits.
    #   I fix this by repeating the key as many times as needed
    #
    #   This is assuming that the luigi sacco transposition algorithm would
    #   function like this in the first place, but who's checking?
    #

    extended_splits = [element for element in splits]

    while len(extended_splits) < len(matrix):
        extended_splits += splits

    # The key is cut at the amount of rows the matrix has to avoid IndexError exceptions
    extended_splits = extended_splits[:len(matrix)]

    # push down extra letters in each row so elements in matrix take correct positions
    for (row_index, row), split in zip(enumerate(matrix), extended_splits):
        if len(row) != split:
            # Note: passing in original key length here because it's used to
            # infer necessary number of columns in matrix
            push_down(matrix, row_index, split, verbose, key_length=len(splits))

    if verbose:
        print("\n\n\n\t\t*** SHAPE OF MATRIX AT THE END ***\n")
        [print(row) for row in matrix]
        print("\n\n")

    return matrix


def get_split_encrypted_text(key: str, encrypted_text: str, lang: str) -> List[str]:
    """
    Returns the given encrypted text (given without white spaces) split up into
    correctly size chunks (words). This is done by encrypting a message of the
    same size but setting the output to include white space, and inferring the
    word sizes from it.
    """
    mock_msg = "A"*len(encrypted_text)

    # This gives me the message in the shape that I need
    mock_enc = luigi_sacco_encrypt(key, mock_msg, lang, with_spaces=True)

    word_lengths = [len(word) for word in mock_enc.split(' ')]

    modded_encrypted_text = []

    current_index = 0

    for i in word_lengths:
        modded_encrypted_text.append(encrypted_text[current_index:current_index+i])
        current_index += i

    return modded_encrypted_text


def confirm_text_in_correct_lang(text: str, lang: Literal["EN", "TR"]) -> None:
    """
    Checks whether given text has any characters that don't belong in the given
    language (such as Q or W in turkish)
    """

    if lang not in ["EN", "TR"]:
        raise ValueError(f"Given language is not supported ({lang})")

    try:
        if lang == "TR":
            for char in text:
                if char not in TURKISH_ALPHABET:
                    raise ValueError()

        elif lang == "EN":
            for char in text:
                if char not in ENGLISH_ALPHABET:
                    raise ValueError()

    except ValueError as e:
        raise ValueError(
            f"Given text does not seem to belong to the group '{lang}'")


def format_key_and_input_text(key: str, input_text: str) -> Tuple[str, str]:
    """
    Returns a tuple of given key and input text stripped of all double spaces,
    and converted into upper case letters.
    """

    def format(x): return x.upper().replace(' ', '')

    formatted_key = format(key)
    formatted_input_text = format(input_text)

    return formatted_key, formatted_input_text


### ENCRYPT
def luigi_sacco_encrypt(key: str, plain_text: str, lang: Literal["EN", "TR"] = "TR", verbose: bool=False, with_spaces: bool = False) -> str:
    """
    Encrypts given plain text message using given key.
    """

    key, plain_text = format_key_and_input_text(key, plain_text)

    confirm_text_in_correct_lang(key, lang)
    confirm_text_in_correct_lang(plain_text, lang)

    # Get column splits from key
    splits = order_key(key, lang)
    key_length = len(splits)

    if verbose:
        print("\nKey Length: ")
        print(key_length)

    # NOTES
    #   A Row will NEVER be longer than the length of the key by definition of this encryption method
    #
    #   Columns may be longer than the key length depending on length of plain text

    # This is the matrix that you will see under the 'luigi sacco' section in the teacher's notes
    initial_matrix = []

    while len(plain_text) > 0:

        for split in splits:

            new_row = []

            while split != 0 and len(plain_text) > 0:
                new_row.append(plain_text[0])
                plain_text = plain_text[1:]
                split -= 1


            filler = ['_' for i in range(key_length - len(new_row))]
            initial_matrix.append(new_row + filler)

    # fill up 'empty spaces' in message matrix to be able to get the final form
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


    final_message_matrix = []

    # Pick the words of the message in the order provided by the splits.
    for row_index in splits:
        if row_index <= len(transposed_matrix):
            final_message_matrix.append(transposed_matrix[row_index - 1])

    if verbose:
        print(splits)
        print("\nFinal Message Matrix")
        [print(row) for row in final_message_matrix]

    # Removing underscores and joining message together
    final_message = ' '.join([''.join(row).replace('_', '') for row in final_message_matrix])

    if not with_spaces:
        final_message = final_message.replace(' ', '')

    return final_message


### DECRYPT
def luigi_sacco_decrypt(key: str, encrypted_text: str, lang: Literal["EN", "TR"] = "TR", verbose: bool = False) -> str:
    """
    Decrypts given encrypted message using given key.
    """
    key, encrypted_text = format_key_and_input_text(key, encrypted_text)
    
    confirm_text_in_correct_lang(key, lang)
    confirm_text_in_correct_lang(encrypted_text, lang)

    # Start of decryption #

    splits = order_key(key, lang)

    if verbose:
        print(splits)

    encrypted_text = get_split_encrypted_text(key, encrypted_text, lang)

    # Create empty matrix
    transposed_matrix = [[] for _ in range(len(splits))]

    # Fill 'er up
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

    # This has the same shape as the initial matrix in the encrypting function
    # but the positions of the letters are not correct yet
    initial_matrix = get_transposed(transposed_matrix)

    if verbose:
        print("\n")
        [print(row) for row in initial_matrix]

    # This final step places the letters in their correct positions
    final_matrix = distribute_letters_across_matrix(initial_matrix, splits, verbose)

    decrypted_message = ''.join([''.join(row).replace('_', '') for row in final_matrix])

    return decrypted_message


def test_program(key: str, plain_text: str, lang: Literal["EN", "TR"] = "TR", verbose=False) -> bool:
    """

    """

    encrypted_message = luigi_sacco_encrypt(key, plain_text, lang=lang, verbose=False)

    # Feeding the encryption function's output to this function to ensure they
    # both work correctly
    decrypted_message = luigi_sacco_decrypt(key, encrypted_message, lang=lang, verbose=False)

    correctly_encrypted_and_decrypted = \
        decrypted_message.replace(' ', '').upper() == plain_text.replace(' ', '').upper()

    if verbose:
        print(f"\n\n\nOriginal Message:")
        print("\n\t" + plain_text)

        print("\n\nEncrypted Message: ")
        print("\n\t" + encrypted_message, end='')
        if len(encrypted_message.replace(' ', '')) == len(plain_text.replace(' ', '')):
            print(" (Lengths match)")
        else:
            print(" (Lengths DON'T match)")

        print("\n\nDecrypted Message: ")
        print("\n\t" + decrypted_message)

        print("\n\nHas been decoded correctly?")
        if correctly_encrypted_and_decrypted:
            print("\n\tYes!")

        else:
            print("\n\tNope :'(")
            print(key)

    return correctly_encrypted_and_decrypted


def execute_english_tests():

    keys = [
        "helloworld",
        "thisisaverylongkeyindeed",
        "short",
        "MuLtiPlEcASe",
        "how about a key which is COMPLETELY WAY TOO LONG PLEASE MAKE IT STOP AHHHHHH"
    ]

    messages = [
        "Whatawonderfulworldwelivein",
        "Armiesareready",
        "Telleveryonethattheirmessageshouldnotbe too long otherwise the encryption algorithm has trouble with it",
        "short"
    ]

    total = 0
    total_correct = 0

    incorrect_combos = []

    for key in keys:
        for message in messages:
            total += 1
            is_correct = test_program(key, message, lang="EN", verbose=False)

            if is_correct:
                total_correct += 1

            else:
                incorrect_combos.append([key, message])

    print(f"Got {total_correct} correct out of {total}")

    if incorrect_combos:
        print("\nFaulty Combinations:")
        [print(row) for row in incorrect_combos]

    else:
        print("""

            * * * * * * * * * * * * * * * * *  
            *                               *
            *   ALL ENGLISH TESTS PASSED!   *
            *                               *
            * * * * * * * * * * * * * * * * *  

        """)


def execute_turkish_tests():
    keys = [
        "TERAZİ",
        "MATEMATİK",
        "ÇOKÇOKÇOKUZUNBİRANAHTAR",
        "KISA",
        "Aaa",
        "büYüKveKüçükharf",
        "iİıIçÇüÜuöÖşŞ",
        "boşluk ek le sem"
    ]

    messages = [
        "ADALET MÜLKÜN TEMELİDİR",
        "Mülkün temeli adalettir ve dolayısıyla adalet mülkün temeildir",
        "buraya inanılmaz uzun bir cümle yazdığım halde acaba program çöker mi falan yoksa gerektiği gibi gene çalışır mı yani mesela devam edip hiç durmasam yazmaya devam devam devam devam valla bir hata vermyior gerçekten çok ilginç analaşılan ki çok iyi bir program yazmış oldum hahahahaha helal olsun bana",
        "vay beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    ]

    total = 0
    total_correct = 0

    incorrect_combos = []

    for key in keys:
        for message in messages:
            total += 1
            is_correct = test_program(key, message, lang="TR", verbose=False)

            if is_correct:
                total_correct += 1

            else:
                incorrect_combos.append([key, message])

    print(f"Got {total_correct} correct out of {total}")

    if incorrect_combos:
        print("\nFaulty Combinations:")
        [print(row) for row in incorrect_combos]

    else:
        print("""

            * * * * * * * * * * * * * * * * *  
            *                               *
            *   ALL TURKISH TESTS PASSED!   *
            *                               *
            * * * * * * * * * * * * * * * * *  

        """)


if __name__ == '__main__':

    execute_english_tests()

    execute_turkish_tests()

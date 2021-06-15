import string
from collections import Counter

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


def luigi_sacco(key, plain_text, lang="TR"):

    # Remove all spaces and symbols and capitalize text
    plain_text = plain_text.replace(' ', '')
    plain_text = plain_text.upper()
    for symbol in string.punctuation:
        plain_text = plain_text.replace(symbol, '')

    # Get column splits from key
    splits = order_key(key, lang)

    initial_matrix = []

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

        initial_matrix.append(message_row)

    # Must fill up 'empty spaces' in message matrix to be able to get the final form
    max_row_length = len(max(initial_matrix, key=len))
    
    for row in initial_matrix:
        while len(row) < max_row_length:
            row.append('_')

    # Transposing to make extracting final message easier
    transposed_matrix = get_transposed(initial_matrix)

    final_message_matrix = [transposed_matrix[row-1] for row in splits]
    
    # Removing underscores and joining message together
    final_message = ' '.join([''.join(row).replace('_', '') for row in final_message_matrix])

    return final_message



if __name__ == '__main__':

    # NOTE: I've made this key and message ENGLISH temporarily
    key = "TERAZİ"
    plain_text = "ADALET MÜLKÜN TEMELİDİR"

    # key = "CONVENIENCE"
    # plain_text = "HERE IS A SECRET MESSAGE ENCIPHERED BY TRANSPOSITION"

    encrypted_message = luigi_sacco(key, plain_text, lang="TR")

    print(encrypted_message)


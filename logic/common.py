import string


TURKISH_ALPHABET = {letter: letter_index for letter_index,
                    letter in enumerate("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ")}

ENGLISH_ALPHABET = {letter: letter_index for letter_index,
                    letter in enumerate(string.ascii_uppercase)}

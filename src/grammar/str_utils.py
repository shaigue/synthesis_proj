""" This file defines functions on strings, to be used instead of the python builtins """


def str_len(s: str) -> int:
    """
    return the length of s
    """
    return len(s)


def str_prefix_of(pref: str, s: str) -> bool:
    """
    return True iff pref is a prefix of s
    """
    return s.startswith(pref)


def str_suffix_of(suf: str, s: str) -> bool:
    """
    return True iff suf is a suffix of s
    """
    return s.endswith(suf)


def str_contains(a: str, b: str) -> bool:
    """
    return True iff a contains b
    """
    return b in a


def str_get_substring(s: str, offset: int, length: int) -> str:
    """
    get a substring of s
    :param s: string to get substring from
    :param offset: from which offset to start the substring
    :param length: length of the substring
    :return: a substring of s (slice by copy)
    """
    return s[offset:offset+length]


def str_index_of(s: str, sub: str) -> int:
    """
    :param s: string to search
    :param sub: substring to look for in the string
    :return: index of the first occurrence of substring in the string. -1 if not found
    """
    return s.find(sub)


def str_char_at_index(s: str, index: int) -> str:
    """
    get a character of a string at a given index
    Note: when converting to z3, do not use indexing (i.e square brackets). s[i] gives a z3 expression of type "Unicode"
    which cannot be compared with z3 expressions of type "String". For example, the following line is invalid:
    x, y = Strings("x y"); x == y[1]
    :param s: string
    :param index: index of character
    :return: string containing the character.
    :exception: IndexError
    """
    return s[index]


def str_concat(a: str, b: str) -> str:
    """
    :return: A string that is a concatenation of a and b
    """
    return a + b


def str_replace(s: str, src: str, dst: str) -> str:
    """
    replace the first occurrence of src in s with dst
    """
    return s.replace(src, dst, 1)

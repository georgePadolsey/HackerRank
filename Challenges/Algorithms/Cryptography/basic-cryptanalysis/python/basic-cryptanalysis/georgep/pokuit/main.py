__author__ = "George"

"""
    Solution for https://www.hackerrank.com/challenges/basic-cryptanalysis

    Normally I would use many files for this program though hackerrank does only accept one file
"""

# When in use on hacker rank (when files are etc.)
hackRankMode = False

# Debug mode true / false used with log method. If hackRankMode
debug = False

# Ensure if hackRankMode is on then debug must be off
if hackRankMode:
    debug = False

# CONSTANTS
RESOURCE_FOLDER = "../../../../resources/"

# What breaks up each bit of data
DATA_SPLIT_CHARACTER = " "

# For simar methods
TOP_SIMAR_MARK = 1.0
EACH_JUDGE_MARK = 0.5
BOTTOM_SIMAR_MARK = 0.0

if hackRankMode:

    import sys

    DATA = sys.stdin.readlines()

else:

    DATA_FILE = RESOURCE_FOLDER + "data.txt"
    with open(DATA_FILE) as f:
        DATA = f.readlines()

DICTIONARY_FILE = (RESOURCE_FOLDER if not hackRankMode else "") + "dictionary.lst"

# Assert the length of the data is bigger than one
assert len(DATA) >= 1


def log(text):
    """ Simple log method that only logs text when debug mode is on
    :param text: text to log
    """
    print(text) if debug else None


def strip_list(ls):
    """ Method which goes over a string list and strips each string in the list of whitespace
    :param ls: the string list to strip
    :return: the string list stripped of all whitespace
    :see str.strip()
    """
    return list(map(str.strip, ls))


def find_interchange_to_letters(f_word, s_word):
    """ Find the cipher between two words, between the first (the ciphered word) and the solved word
    :param f_word: the ciphered word
    :param s_word: the solved word
    """

    # Assert the words have equal length
    assert len(f_word) == len(s_word)

    _interchange = {}

    # For every letter in each word
    for i in range(0, len(f_word)):
        # Assign dictionary {cipheredLetter -> solvedLetter}
        _interchange[f_word[i]] = s_word[i]

    return _interchange


def solve_data(_data, _letters):
    """ This solves the data with the appropriate interchange letters provided
    :param _data: the data to solve
    :param _letters: the letters to solve the data with
    :return:: the solved data
    """
    _solved_data = []
    for _word in _data:
        # For every word in the data solve the word and append to list to return later
        _solved_data.append(solve_word(_word, _letters))

    return _solved_data


def solve_word(_word, _letters):
    """ This solves an individual word with the appropriate interchange letters provided
    :param _word: the word to solve
    :param _letters: the letters to solve data with
    :return: the solved word
    """
    _temp_word = []

    for word_character in _word:
        # For every character in the word solve if the interchange for that letter is provided
        _temp_word.append(_letters[word_character] if word_character in _letters else word_character)

    # List acting as string
    return "".join(_temp_word)


def sort_by_length(_words):
    """ This sorts words by their length into a dictionary[length -> arr of words with that length]
    :param _words: The words to sort
    :return: Words sorted by their length into a dictionary[length -> arr of words with that length]
    """

    _length_map = {}

    for _word in _words:

        word_length = len(_word)

        if word_length in _length_map.keys():

            _length_map[word_length].append(_word)

        else:

            _length_map[word_length] = [_word]

    return _length_map


def get_words_with_length(_words, _length):
    """ Gets the words with a certain length
    :param _words: the words to check
    :param _length: the length of the word to look for
    :return: The words with a certain length
    """

    words_with_length = []

    for _word in _words:
        if len(_word) == _length:
            words_with_length.append(_word)

    return words_with_length


def get_repeated_chars_pos(_word):
    """ Gets the position of repeated characters in the word and returns an array of each instance of them
    :param _word: The word in for
    :return: An array of each instance of them
    """

    repeated_chars = {}
    i = 0
    for char in _word:
        if char in repeated_chars:
            repeated_chars[char].append(i)

        else:
            repeated_chars[char] = [i]
        i += 1

    new_repeated_char = {}
    for (_char, _arr) in repeated_chars.items():
        if len(_arr) >= 2:
            new_repeated_char[_char] = _arr

    return [item for sublist in new_repeated_char.values() for item in sublist]


def get_simar_mark(word1, word2, _letters):
    """ Works out the similarity between word 1 (when solved) and word 2 (not solved with letters).
    It returns the similarity score out of 1 (float).
    :param word1 first word to check (which is solved with letters)
    :param word2 second word to check (which is not solved)
    :param _letters the interchange letters to solve with
    :return: the similarity mark out of 1 (float)
    """

    # Start mark = 0
    mark = BOTTOM_SIMAR_MARK

    # If they are not the same length then they are definitely different!
    if len(word1) != len(word2):
        return BOTTOM_SIMAR_MARK

    # If words are identical then they are definitely similar!
    if word1 == word2:
        return TOP_SIMAR_MARK

    repeated_chars_1 = get_repeated_chars_pos(word1)
    repeated_chars_2 = get_repeated_chars_pos(word2)

    # Sort before comparing
    repeated_chars_1.sort()
    repeated_chars_2.sort()

    # Get the repeated char pattern of the words and compare the repeated char patterns
    if repeated_chars_1 == repeated_chars_2:
        mark += EACH_JUDGE_MARK

    # Solve just word 1
    word1 = solve_word(word1, _letters)

    point_per_letter = EACH_JUDGE_MARK / len(word1)
    for i in range(0, len(word1)):
        # For each same letter add the appropriate mark
        if word1[i] == word2[i]:
            mark += point_per_letter

    return mark


# DICTIONARY WORDS:
with open(DICTIONARY_FILE) as f:
    # Trim list
    dic_words = strip_list(f.readlines())

# Assume there is more than 1 dictionary word
assert len(dic_words) >= 1

# Parse data
parsed_data = DATA[0].split(DATA_SPLIT_CHARACTER)
unsolved_data = list(parsed_data)

length_map = sort_by_length(dic_words)

log(length_map)

# Set Variables
solved_letters = {}
quick_indicators = []
sure_letters = {}
solved_data = []
min_indicate = 0

while len(quick_indicators) == 0:
    quick_indicators = length_map[sorted(length_map.keys(), reverse=True)[min_indicate]]
    min_indicate += 1

solved = False
timeout = 600
redo_indicator = False
while not solved:
    # Every time round remove one from timeout
    # It is done at top as continue is called so this is normally missed at top
    timeout -= 1

    # Only check every 5 times round, as solving is a intensive method
    if timeout % 5 == 0:
        solved_data = solve_data(parsed_data, solved_letters)
        if len(solved_data) - len(unsolved_data) <= 0:
            solved = True

    log("TIMEOUT:" + str(timeout))

    if timeout <= 0:
        solved = True
        # Cannot solve fully ;(

    if redo_indicator:
        quick_indicators = {}
        if min_indicate >= len(length_map):
            min_indicate = 0

        while len(quick_indicators) == 0:
            quick_indicators = length_map[sorted(length_map.keys(), reverse=True)[min_indicate]]
            min_indicate += 1
        redo_indicator = False

    quick_indicator_length = len(quick_indicators[0])

    words = get_words_with_length(unsolved_data, quick_indicator_length)

    # Quick one if there is only one of certain type of word
    if len(quick_indicators) == 1:

        log(str(words) + str(quick_indicators))

        if len(words) <= 0:
            redo_indicator = True
            continue

            # If words more than one length then that just means the word has been used more than once
            # Atleast in this encryption, so it is fine to just get the first one
        word = words[0]

        interchange = find_interchange_to_letters(word, quick_indicators[0])

        solved_letters.update(interchange)

        sure_letters.update(interchange)

        unsolved_data.remove(word)

        redo_indicator = True
    else:

        if len(words) <= 0:
            redo_indicator = True
            continue

        for word in words:
            simar_marks = {}
            for indicator in quick_indicators:
                simar_marks.update({indicator: get_simar_mark(word.lower(), indicator.lower(), solved_letters)})

            simar_marks = sorted([(value, key) for (key, value) in simar_marks.items()], reverse=True)

            log(simar_marks)
            log("%s %s" % (word, solve_word(word, solved_letters)))

            max_indicator = simar_marks[0][1]

            interchange = find_interchange_to_letters(word.lower(), max_indicator.lower())

            log("!!WATCH ME\n" * 2) if len([i for i in sure_letters.keys() if i in interchange.keys()]) >= 1 else None

            log("WATCH ME!!!!!!\n" + interchange["p"] + " LOOKUP" + solve_word(word, solved_letters)) \
                if "p" in interchange and \
                   interchange[
                       "p"] != sure_letters else None

            solved_letters.update(interchange)

            log("%s -> %s" % (word, max_indicator))

            unsolved_data.remove(word)

            redo_indicator = True

    # Check for words that have been solved indirectly by the letter crypt found
    for word in unsolved_data:
        solved_word = solve_word(word, solved_letters)
        if solved_word in dic_words:
            solved_letters.update(find_interchange_to_letters(word, solved_word))

            unsolved_data.remove(word)

# Solve the data with the cipher
solved_data = solve_data(parsed_data, solved_letters)

log(len(solved_letters))
log(len(solved_data) - len(unsolved_data))
log(solved_letters)

log(solved_data) if debug else print(" ".join(solved_data))

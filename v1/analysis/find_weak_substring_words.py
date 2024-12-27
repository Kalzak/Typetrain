from analysis.find_weak_substrings import find_weak_substrings
import re
import random


def read_words_from_file(filename):
    word_list = []
    
    try:
        with open(filename, 'r') as file:
            for line in file:
                word = line.strip()  # Remove leading/trailing whitespace and newline characters
                if word:
                    word_list.append(word)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return word_list

def find_weak_substring_words(word_len_limit, numwords):
    substrings = find_weak_substrings()

    words_list = read_words_from_file('./analysis/google-10000-english-no-swears.txt')

    print(words_list)

    temp_words_list = []
    for word in words_list:
        if len(word) <= word_len_limit:
            temp_words_list.append(word)
        
    words_list = temp_words_list


    total_freq = sum(substring['freq'] for substring in substrings)

    paragraph = []

    for _ in range(numwords):
        rand_val = random.randint(1, total_freq)
        cumulative_freq = 0

        for substring in substrings:
            cumulative_freq += substring['freq']
            if rand_val <= cumulative_freq:
                regexpattern = re.compile(".*" + substring['substring'].replace(" ", ".") + ".*")
                re.compile(regexpattern)

                found = False
                count = 0
                while found == False and count < 500:
                    rand_word = random.choice(words_list)
                    count += 1
                    if regexpattern.match(rand_word):
                        paragraph.append(rand_word)
                        found = True
                        break

                break
            
    return paragraph
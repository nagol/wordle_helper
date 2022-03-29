# Wordle Helper

# Background:
# Make guess of n-digit word
# each letter is either 1.) Not contained in the target word [GREY]
#                       2.) Contained in the target word but in the wrong position [YELLOW]
#                           -> Generates contains(letter) and word[position] != letter 
#                       3.) Contained in the target word AND in the correct position [GREEN]
#                           -> Generates contains(letter) and word[position] != letter





def get_possible_words(
    english_dictionary,
    word_length = 5, 
    contains_list = [], 
    does_not_contain_list = [], 
    position_known_dict = [], 
    position_not_known_dict = []):
    
    '''
        english_dictionary - dictionary containing word and word metadata
        word_length - integer indicating the word length for the puzzle (commonly 5 or 6)
        contains_list - list of letters known to be in the target word (YELLOW or GREEN)
            ex. ['a', 't']
        does_not_contain_list - list of letters known to not be in target word (GREY)
            ex. ['h']
        position_known_dict - dictionary with letter postions as keys (GREEN)
            ex. {1:'a', '5:'t'}

        position_not_known_dict - dictionary with letter position as keys and values
            in a list since there may be many known non-letters for a given position
            ex. {1:['b', 'c'], 4: ['t]}

    '''
    
    # subset to desired length
    english_dictionary = english_dictionary[(english_dictionary.word_length == word_length)]

    # remove impossible words
    if contains_list:

        for letter in contains_list:
            english_dictionary = english_dictionary[
                (english_dictionary.word.str.contains(letter, regex = True))
                ]

    if does_not_contain_list:

        for letter in does_not_contain_list:
            english_dictionary = english_dictionary[
                (~english_dictionary.word.str.contains(letter, regex = True))
                ]

    if position_known_dict:

        for key, value in position_known_dict.items():
             english_dictionary = english_dictionary[
                (english_dictionary.word.str.slice(start = key-1, stop = key, step = 1) == value)
                ]

    if position_not_known_dict:

        for key, value in position_not_known_dict.items():
            for letter in value:
                english_dictionary = english_dictionary[
                    (english_dictionary.word.str.slice(start = key-1, stop = key, step = 1) != letter)
                    ]

    print(f"There are currently {len(english_dictionary.index)} possible words")
    print(f"Here are the top 50 based on the information provided:")
    print(english_dictionary.head(50))

    return english_dictionary

# Example usage
# print(
#     get_possible_words(
#         word_length = 10,
#         contains_list = ['i','r','s','t','y'],
#         does_not_contain_list = ['u','n','v','e'],
#         position_known_dict = {8:'i',9:'t',10:'y'}, 
#         position_not_known_dict = {3:['i'], 6:['r'], 7:['s']}
#         )
# )



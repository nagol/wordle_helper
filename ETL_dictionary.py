import pandas as pd

# Load data with word, word freq over trillion word coupus
word_dictionary = pd.read_csv("./data/unigram_freq.csv")

# remove null words
word_dictionary = word_dictionary[word_dictionary.word.notnull()]

# create column with word lengths
word_dictionary['word_length'] = word_dictionary.word.str.len().astype(int)
word_dictionary['distinct_letters'] = word_dictionary.word.apply(lambda x: len(set(x)))

# export transformed data
word_dictionary.to_csv("./data/transformed_dictionary.csv", index = False)
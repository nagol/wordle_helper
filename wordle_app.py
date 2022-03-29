import streamlit as st
import pandas as pd
from get_possible_words import *

st.set_page_config(
    page_title="Wordle Helper", 
    page_icon="📊", 
    initial_sidebar_state="expanded"
)

# Load data with word, word freq over trillion word coupus
word_dictionary = pd.read_csv("./data/transformed_dictionary.csv")

# Set helper variables
alphabet = ['', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
VERBOSE = False



st.write(
    """
# Wordle Helper
*data + python to the rescue!*

Use the sidebar filters to input information about the target word.

Each guess at the target word provides new information about:
+ letters that are contained in the target word [YELLOW and GREEN]
+ letters that are not contained in the target word [GREY]
+ letters in target word whose position are known [GREEN]
+ letters in target word whose position is forbidden in a particular position [YELLOW]

The table below contains words meeting the selected criteria **sorted by how common the word is in common usage**.
You can use your best judgement about what word to actually use as your next guess but generally you will have
very good results just by always choosing the most common word meeting the criteria selected.

## Table of Words Meeting Criteria
"""
)

st.sidebar.write(
    """
    # Parameters:
"""
)

number = st.sidebar.slider(
    'How many letters in the puzzle?',
    min_value = 1,
    max_value = 20,
    value = 5,
    step = 1)

# get letters known to be in the target word
known_letters = st.sidebar.multiselect(
     'What letters are known to be included in the target word?',
     alphabet,
     [])

# get letters known to not be in the target word
known_nonletters = st.sidebar.multiselect(
     'What letters are known to NOT be included in the target word?',
     alphabet,
     [])

# get known position information
known_positions = {index:'' for index in range(1, number + 1)}
for pos in known_positions:
    known_positions[pos] = st.sidebar.selectbox(
        f"What letter is known for string index {pos}?",
        alphabet,
        key = 'known' + str(pos))

# get known non-position information
known_nonpositions = {index:[] for index in range(1, number + 1)}
for pos in known_nonpositions:
    
    known_nonpositions[pos] = st.sidebar.multiselect(
        f"What letter(s) are forbidden for string index {pos}?",
        alphabet,
        key = 'unknown' + str(pos))


# convert the input data structures into form originally intended for get_possible_words()
known_position_dict = {}
for index in range(1, number + 1):
    if known_positions[index] != '':
        known_position_dict[index] = known_positions[index]

known_nonpositions_dict = {}
for index in range(1, number + 1):
    if known_nonpositions[index] != []:
        known_nonpositions_dict[index] = known_nonpositions[index]


dictionary_data = get_possible_words(
    word_dictionary,
    word_length = number,
    contains_list = known_letters,
    does_not_contain_list = known_nonletters,
    position_known_dict = known_position_dict, 
    position_not_known_dict = known_nonpositions_dict
    )
st.write(dictionary_data, height = 500)

st.markdown("The data used is from [Kaggle](https://www.kaggle.com/datasets/rtatman/english-word-frequency).")
st.markdown("The code to build this app are located [github](https://github.com/nagol/wordle_helper).")
# For debugging
#"st.session_state object", st.session_state

if VERBOSE:
    st.write('Puzzle word size: ', number)
    st.write('Current known letters are:', ', '.join(known_letters))
    st.write('Current known non-letters are:', ', '.join(known_nonletters))
    
    for pos in range(1, number + 1):
        st.write(f"The letter in position {pos} is known to be:", known_positions[pos])
        st.write(f"The letter in position {pos} is forbidden to be:", ', '.join(known_nonpositions[pos]))


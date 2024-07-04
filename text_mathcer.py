# Let's create a function to check if all provided words are included in the text

import random
import spacy
import pyinflect
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import re

# Ensure the required nltk data is downloaded
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

def get_word_forms_(word):
    words = classify_words(word)

    return words

def classify_words(word):
    noun_forms = None
    verb_forms = None
    adjective_forms = None
    adverb_forms = None

    if is_adjective(word):
        adjective_forms = get_list_forms(word, 'JJ')
    
    if is_adverb(word):
        adverb_forms = get_list_forms(word, 'RB')

    if is_noun(word):
        noun_forms = get_list_noun_forms(word)
    
    if is_verb(word):
        verb_forms = get_list_verb_forms(word)

    return noun_forms, verb_forms, adjective_forms, adverb_forms

def is_noun(word):
    # Check if the word has any noun synsets in WordNet
    return any(ss.pos() == 'n' for ss in wn.synsets(word))

def is_verb(word):
    # Check if the word has any verb synsets in WordNet
    return any(ss.pos() == 'v' for ss in wn.synsets(word))

def is_adjective(word):
    # Check if the word has any adjective synsets in WordNet
    return any(ss.pos() == 'a' or ss.pos() == 's' for ss in wn.synsets(word))

def is_adverb(word):
    # Check if the word has any adverb synsets in WordNet
    return any(ss.pos() == 'r' for ss in wn.synsets(word))


def get_list_forms(word, pos):
    doc = nlp(word)
    token = doc[0]

    base_form = token.text
    comparative_form = token._.inflect(f'JJR' if pos == 'JJ' else 'RBR') if token._.inflect(f'JJR' if pos == 'JJ' else 'RBR') else word
    superlative_form = token._.inflect(f'JJS' if pos == 'JJ' else 'RBS') if token._.inflect(f'JJS' if pos == 'JJ' else 'RBS') else word
    
    return base_form, comparative_form, superlative_form
    

def get_list_noun_forms(word):
    doc = nlp(word)
    token = doc[0]

    singular_form = token._.inflect('NN') if token._.inflect('NN') else word
    plural_form = token._.inflect('NNS') if token._.inflect('NNS') else word
    
    return singular_form, plural_form
    
def get_list_verb_forms(word):
    if word.lower() == "be":
        return 'be', 'was', 'were', 'being', 'been', 'am', 'is', 'are'
        
    base_form = lemmatizer.lemmatize(word, 'v')
    
    return base_form,conjugate_verb(base_form, 'VBD'),conjugate_verb(base_form, 'VBG'),conjugate_verb(base_form, 'VBN'),base_form, conjugate_verb(base_form, 'VBZ')

def get_list_idiom_forms(word):
    
    first_word = word.split()[0]
    rest_of_words = ' '.join(word.split()[1:])

    if first_word.lower() == "be":
        return 'be'+' '+ rest_of_words, 'was'+' '+ rest_of_words, 'were'+' '+ rest_of_words, 'being'+' '+ rest_of_words, 'been'+' '+ rest_of_words, 'am'+' '+ rest_of_words, 'is'+' '+ rest_of_words, 'are'+' '+ rest_of_words

    base_form = lemmatizer.lemmatize(first_word, 'v')
    return base_form +' '+ rest_of_words,conjugate_verb(base_form, 'VBD')+' '+ rest_of_words,conjugate_verb(base_form, 'VBG')+' '+ rest_of_words,conjugate_verb(base_form, 'VBN')+' '+ rest_of_words,base_form+' '+ rest_of_words, conjugate_verb(base_form, 'VBZ')+' '+ rest_of_words

def conjugate_verb(base, tense):
    doc = nlp(base)
    token = doc[0]
    if tense == 'VBD':
        return token._.inflect("VBD")
    elif tense == 'VBG':
        return token._.inflect("VBG")
    elif tense == 'VBN':
        return token._.inflect("VBN")
    elif tense == 'VBZ':
        return token._.inflect("VBZ")
    return base


def convert_to_unique_list(input_str):
    """
    Converts a string representation of a list of tuples to a list of unique values,
    removing any 'None' values.
    
    Args:
        input_str (str): The input string to be processed.
    
    Returns:
        list: A list of unique values.
    """
    # Remove the parentheses and quotes
    cleaned_str = re.sub(r'[()"]', '', input_str)
    # Split the string into a list of tuples
    tuples = [tuple(x.strip().split(', ')) for x in cleaned_str.split('), (')]
    # print("tuples1: ", tuples)
    
    # Flatten the list of tuples and remove duplicates
    result = list(set([item for tup in tuples for item in tup]))
    
    # Remove any 'None' values
    result = [x for x in result if x != 'None']

    result = [item.strip("'") for item in result]

    return result


def string_to_random_list(input_string):
    """
    Takes a comma-separated string as input and returns a list of strings in random order.
    """
    word_list = [word.strip() for word in input_string.split(',')]
    random.shuffle(word_list)
    return list(set(word_list))

def check_words_in_text(text, words):
    if type(words) is not list:
        words = string_to_random_list(words)
        
    # Convert both text and words to lowercase
    text = text.lower()
    words = [word.lower() for word in words]    
    
    # missing_words = [word for word in words if word not in text]
    
    for word in words :
        word_forms = get_word_forms_(word) # from word
        word_forms_list = convert_to_unique_list(str(word_forms))
        if len(word_forms_list) == 0:
            idioms_forms = None
            word_forms_list.append(word)
            if is_verb(word.split()[0]): 
                idioms_forms = list(get_list_idiom_forms(word))
                for idiom in idioms_forms:
                    word_forms_list.append(idiom)
                word_forms_list= list(set(word_forms_list))
        word_flag = False
        for each_word in word_forms_list:
            if each_word in text:
                word_flag = True
        if word_flag == True: pass
        elif word_flag == False:
            missing_words.append(word) 

    return missing_words


words_list = None
story_text = ""
missing_words = []

# Provided words list
# Given story text
story_text = "The quick brown fox jumps over the lazy dog. It give off, are made up of, **sprang up** and **comprised**"
words_list = "Spring up, Comprise, Flight, Cat, Dog, give off, be made up of"


# Check for missing words
missing_words = check_words_in_text(story_text, words_list)
print(missing_words)
print(len(missing_words))

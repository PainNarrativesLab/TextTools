# Used for WordFilters
import re

import nltk
from nltk.corpus import wordnet as wn

from TextProcessors.Filters import *

from TextProcessors.NgramFilters import *
from TextProcessors.Modifiers import *

# from nltk.replacers import RegexpReplacer

#
# class IFilter(object):
#     """
#     Interface for text processing objects which take a word as input and
#     either return True or False.
#
#     A list of these will be passed in to objects like TweetTextWordBagMaker
#     """
#
#     def __init__(self):
#         pass
#
#     def run(self, word):
#         """Runs the operation on the string. This is the main method"""
#         raise NotImplementedError
#

# class IModifier(object):
#     """
#     Interface for classes which modify the input string and return the
#     modified string. Used for tasks like stemming lemmatizing etc
#     """
#
#     def __init__(self):
#         pass
#
#     def run(self, text, **kwargs):
#         raise NotImplementedError
#
#     def _check_is_single_word(self, text):
#         """
#         Some implmentations of IModifier allow for sentences. Others
#         want just one word at a time. This is called by the latter
#         and checks to make sure that it has the correct input
#         :param text: String to screen for multiple words
#         """
#         assert (type(text) is str)
#         assert (text.count(" ") is 0)
#
#
# class IModifierList(object):
#     """
#     Interface for classes which act on a list of strings by modifying
#     the input strings and returning a list of modified strings.
#     Used for tasks like lemmatizing etc
#     """
#
#     def __init__(self):
#         pass
#
#     def run(self, wordbag, **kwargs):
#         """
#         Processes list of strings
#         :param wordbag: List of strings to run
#         :param kwargs:
#         :return: List of strings, modified
#         """
#         raise NotImplementedError
#
#
# class INgramFilter(object):
#     """
#     Interface for filters on ngrams
#     """
#
#     def __init__(self, **kwargs):
#         pass
#
#     def filter(self, collocation_finder):
#         """
#         Arguments:
#             collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
#         Returns:
#             The collocation_finder after has been filtered
#         """
#         raise NotImplementedError


#####################################
# IFilter implementations          #
#####################################


# class URLFilter(IFilter):
#     """
#     Removes some urls from tweets
#     TODO: Make this better
#     """
#
#     def __init__(self):
#         IFilter.__init__(self)
#
#     def run(self, word):
#         if word[ 0:6 ] != '//t.co':
#             return True
#         else:
#             return False
#
#
# class UsernameFilter(IFilter):
#     """
#     Filters out twitter usernames
#     """
#
#     def __init__(self):
#         IFilter.__init__(self)
#
#     def run(self, word):
#         assert (type(word) is str)
#         if word[ 0 ] != '@' and word[ 0:1 ] != '.@':
#             return True
#         else:
#             return False
#
#
# class NumeralFilter(IFilter):
#     """
#     Filters out all non-alphanumeric characters
#     """
#
#     def __init__(self):
#         IFilter.__init__(self)
#
#     def run(self, word):
#         if type(word) is str:
#             return word.isalpha()
#         else:
#             return False
#

#############################
# IModifier                 #
#############################
#
# class RegexpReplacer(IModifier):
#     """
#     Executes regex replacement on text input based on stored
#     regex patterns.
#     By default will replace contractions
#     Properties:
#         _patterns: Tuple of compiled regex replacement patterns to apply
#     """
#
#     def __init__(self, replace_contractions=True):
#         """
#         Initialize regex and load default patterns
#         :param replace_contractions:  Whether to load patterns for contractions
#         """
#         self._patterns = ()
#         self.contraction_patterns = [
#             (r'won\'t', 'will not'),
#             (r'Won\'t', 'will not'),
#             (r'can\'t', 'cannot'),
#             (r'Can\'t', 'cannot'),
#             (r'i\'m', 'i am'),
#             (r'I\'m', 'i am'),
#             (r'ain\'t', 'is not'),
#             (r'Ain\'t', 'is not'),
#             (r'(\w+)\'ll', '\g<1> will'),
#             (r'(\w+)n\'t', '\g<1> not'),
#             (r'(\w+)\'ve', '\g<1> have'),
#             (r'(\w+t)\'s', '\g<1> is'),
#             (r'(\w+)\'re', '\g<1> are'),
#             (r'(\w+)\'d', '\g<1> would'),
#         ]
#         if replace_contractions:
#             # Add contraction patterns to stored list
#             self.patterns = self.contraction_patterns
#
#     @property
#     def patterns(self):
#         """
#         Getter for the compiled patterns
#         :return: tuple
#         """
#         return self._patterns
#
#     @patterns.setter
#     def patterns(self, patterns):
#         """
#         Adds to the regex replacement patterns.
#         The pattern should be a tuple with format (regex expression, string to insert).
#         The input can be either a tuple with that pattern, a list of such tuples, or a tuple of such tuples.
#         :param patterns: tuple, list
#         """
#         # Usually patterns is a tuple, so start by listifying it
#         self._patterns = list(self._patterns)
#
#         # Now figure out what the hell we just received
#         if isinstance(patterns, tuple) and isinstance(patterns[ 0 ], str):
#             # The input is a single replacement pattern, so wrap it in a list
#             patterns = list(patterns)
#
#         # Now the input is (hopefully) something iterable containing pattern tuples
#         for p in patterns:
#             new_pattern = (re.compile(p[ 0 ]), p[ 1 ])
#             self._patterns.append(new_pattern)
#
#         # re-tuple the stored patterns
#         self._patterns = tuple(self._patterns)
#
#     def run(self, text, **kwargs):
#         """
#         Arguments:
#             text: The text to subject to regex replacement
#             :param kwargs:
#             :returns: Modified text if regex found, original if not
#         """
#         s = text
#         for (pattern, repl) in self._patterns:
#             (s, count) = re.subn(pattern, repl, s)
#         return s
#
#     def add_compiled_regex_pattern(self, compiled_pattern, replacement):
#         """
#         After several hours of trying to figure out how to pass in raw strings to add
#         regex patterns, I gave up and added this. Grrr.
#         :param compiled_pattern: A compiled regex pattern to apply
#         :param replacement: The string to replace the pattern with
#         """
#         self._patterns = list(self._patterns)
#         self._patterns.append((compiled_pattern, replacement))
#         # re-tuple the stored patterns
#         self._patterns = tuple(self._patterns)
#
#
# class Lemmatizer(IModifierList):
#     """
#     Wrapper on nltk.stem.WordNetLemmatizer plus the part of speech tagger
#     for lemmatizing words
#
#     Attributes:
#         lemmatizer: The nltk wordnet lemmatizer instance
#     """
#
#     def __init__(self):
#         IModifierList.__init__(self)
#         self.lemmatizer = nltk.stem.WordNetLemmatizer()
#
#     def run(self, wordbag):
#         """
#         Lemmatizes the words in wordbag, taking into consideration their part of speech
#         Args:
#             wordbag: Bag of words (list of strings)
#         Returns:
#             Lemmatized list of strings
#         """
#         try:
#             lemmatized = [ ]
#             tagged = self._get_pos_tags(wordbag)
#             for word, tag in tagged:
#                 # if the part of speech wasn't determined, lemmatize without pos
#                 if tag is None:
#                     lemmatized.append(self.process_token(word))
#                 else:
#                     lemmatized.append(self.lemmatizer.lemmatize(word, tag))
#             return lemmatized
#         except Exception as e:
#             print(e)
#
#     def process_token(self, text, **kwargs):
#         """
#         Lemmatizes a single token. Does not take into account pos
#         Args:
#             text: Single word string to be lemmatized
#         Returns:
#             Lemmatized string
#         """
#         try:
#             # self._check_is_single_word(text)
#             assert (type(text) is str)
#             return self.lemmatizer.lemmatize(text)
#         except Exception as e:
#             print(e)
#
#     def _get_pos_tags(self, word_list):
#         """
#         Tags each word with its part of speech
#         Args:
#             word_list: Word bag (list of strings)
#         Returns:
#             Returns a list of tuples with the format (word, pos) where pos is the wordnet pos tag
#         """
#         return PartOfSpeechClassification.get_pos_tags(word_list)
#
#         # def _convert_treebank_tag_to_wordnet_pos(self, treebank_tag):
#         #     """
#         #     The nltk.pos_tag() is trained on the treebank corpus. So it returns
#         #     a different representation of the part of speech than the wordnet
#         #     lemmatizer is expecting. This handles the conversion.
#         #     :return: string
#         #     """
#         #     ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
#         #     if treebank_tag.startswith('J'):
#         #         return ADJ
#         #     elif treebank_tag.startswith('V'):
#         #         return VERB
#         #     elif treebank_tag.startswith('N'):
#         #         return NOUN
#         #     elif treebank_tag.startswith('R'):
#         #         return ADV
#         #     else:
#         #         return ''
#
#
# class PorterStemmer(IModifier):
#     """
#     Wrapper on nltk's porter-stemmer
#     """
#
#     def __init__(self):
#         IModifier.__init__(self)
#         self.stemmer = nltk.stem.PorterStemmer()
#
#     def run(self, text, **kwargs):
#         """
#         TODO: Make sure only a single word passed in
#         Executes the porter stem and returns the stemmed word
#         Args:
#             text: String to stem
#         Returns:
#             Porter stemmed string
#         """
#         try:
#             self._check_is_single_word(text)
#             assert (type(text) is str)
#             return self.stemmer.stem(text)
#         except Exception as e:
#             print(e)
#

# ###################################
# # INgramFilter implementations    #
# ###################################
#
# class CustomFilter(INgramFilter):
#     """
#     Wrapper for applying arbitrary filter to the collocation finder
#     e.g., for getting where 'and' is at trigram[1] but not beginning or end: lambda w1, w2, w3: 'and' in (w1, w3)
#     """
#
#     def __init__(self):
#         self.filter_function = lambda x: x
#         INgramFilter.__init__(self)
#
#     def set_filter(self, filter_function):
#         self.filter_function = filter_function
#
#     def filter(self, collocation_finder):
#         """
#         Arguments:
#             collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
#         """
#         assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
#         return collocation_finder.apply_ngram_filter(self.filter_function)
#
#
# class WordFilter(INgramFilter):
#     """
#     Wrapper for filtering by specific strings
#     Make sure to set filter_words before calling filter
#     Attributes:
#         _filter_words: Tuple holding words to filter by, can be set with string, tuple, or list
#     """
#
#     def __init__(self):
#         self._filter_words = ()
#         INgramFilter.__init__(self)
#
#     @property
#     def filter_words(self):
#         return self._filter_words
#
#     @filter_words.setter
#     def filter_words(self, words):
#         """
#         adds words to the internally held tuple of filter_words
#         Arguments:
#             :param words: Tuple, list, or individual word to add to the filter words
#         """
#         self._filter_words = list(self._filter_words)
#         if isinstance(words, list):
#             self._filter_words += words
#         elif isinstance(words, str):
#             self._filter_words.append(words)
#         elif isinstance(words, tuple):
#             self._filter_words += list(words)
#         self._filter_words = tuple(self._filter_words)
#
#     def filter(self, collocation_finder):
#         """
#         Arguments:
#             collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
#         """
#         assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
#         return collocation_finder.apply_word_filter(lambda w: w in self.filter_words)
#

class PartOfSpeechClassification(object):
    """
    Tools for classifying part of speech
    """

    @classmethod
    def get_pos_tags(cls, word_list):
        """
        Tags each word with its part of speech
        Args:
            word_list: Word bag (list of strings)
        Returns:
            Returns a list of tuples with the format (word, pos) where pos is the wordnet pos tag
        """
        return [ (word, cls._convert_treebank_tag_to_wordnet_pos(tag)) for word, tag in nltk.pos_tag(word_list) ]

    @classmethod
    def _convert_treebank_tag_to_wordnet_pos(cls, tag):
        """
        The nltk.pos_tag() is trained on the treebank corpus. So it returns
        a different representation of the part of speech than the wordnet
        lemmatizer is expecting. This handles the conversion.

        Args:
            tag: String penn_treebank tag

        Returns:
            Wordnet part of speech tag or None
        """

        def is_noun(tag):
            return tag in [ 'NN', 'NNS', 'NNP', 'NNPS' ]

        def is_verb(tag):
            return tag in [ 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ' ]

        def is_adverb(tag):
            return tag in [ 'RB', 'RBR', 'RBS' ]

        def is_adjective(tag):
            return tag in [ 'JJ', 'JJR', 'JJS' ]

        if is_adjective(tag):
            return wn.ADJ
        elif is_noun(tag):
            return wn.NOUN
        elif is_adverb(tag):
            return wn.ADV
        elif is_verb(tag):
            return wn.VERB
        return None


if __name__ == '__main__':
    pass

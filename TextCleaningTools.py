# Used for WordFilters
import nltk
import re

# from nltk.replacers import RegexpReplacer


class ICleaner(object):
    """
    Interface for text processing objects which take a word as input and
    either return True or False.

    A list of these will be passed in to objects like TweetTextWordBagMaker
    """

    def __init__(self):
        pass

    def clean(self, word):
        raise NotImplementedError


class IModifier(object):
    """
    Interface for classes which modify the input string and return the
    modified string. Used for tasks like stemming lemmatizing etc
    """

    def __init__(self):
        pass

    def process(self, text, **kwargs):
        raise NotImplementedError

    def _check_is_single_word(self, text):
        """
        Some implmentations of IModifier allow for sentences. Others
        want just one word at a time. This is called by the latter
        and checks to make sure that it has the correct input
        :param text: String to screen for multiple words
        """
        assert (type(text) is str)
        assert (text.count(" ") is 0)


class INgramFilter(object):
    """
    Interface for filters on ngrams
    """

    def __init__(self, **kwargs):
        pass

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        Returns:
            The collocation_finder after has been filtered
        """
        raise NotImplementedError


#####################################
# ICleaner implementations          #
#####################################


class URLCleaner(ICleaner):
    """
    Removes some urls from tweets
    TODO: Make this better
    """

    def __init__(self):
        ICleaner.__init__(self)

    def clean(self, word):
        if word[0:6] != '//t.co':
            return True
        else:
            return False


class UsernameCleaner(ICleaner):
    """
    Filters out twitter usernames
    """

    def __init__(self):
        ICleaner.__init__(self)

    def clean(self, word):
        assert (type(word) is str)
        if word[0] != '@' and word[0:1] != '.@':
            return True
        else:
            return False


class NumeralCleaner(ICleaner):
    """
    Filters out all non-alphanumeric characters
    """

    def __init__(self):
        ICleaner.__init__(self)

    def clean(self, word):
        if type(word) is str:
            return word.isalpha()
        else:
            return False


#############################
# IModifier                 #
#############################


class RegexpReplacer(IModifier):
    """
    Executes regex replacement on text input based on stored
    regex patterns.
    By default will replace contractions
    Properties:
        _patterns: Tuple of compiled regex replacement patterns to apply
    """
    def __init__(self, replace_contractions=True):
        """
        Initialize regex and load default patterns
        :param replace_contractions:  Whether to load patterns for contractions
        """
        self._patterns = ()
        self.contraction_patterns = [
            (r'won\'t', 'will not'),
            (r'can\'t', 'cannot'),
            (r'i\'m', 'i am'),
            (r'ain\'t', 'is not'),
            (r'(\w+)\'ll', '\g<1> will'),
            (r'(\w+)n\'t', '\g<1> not'),
            (r'(\w+)\'ve', '\g<1> have'),
            (r'(\w+t)\'s', '\g<1> is'),
            (r'(\w+)\'re', '\g<1> are'),
            (r'(\w+)\'d', '\g<1> would'),
        ]
        if replace_contractions:
            # Add contraction patterns to stored list
            self.patterns = self.contraction_patterns

    @property
    def patterns(self):
        """
        Getter for the compiled patterns
        :return: tuple
        """
        return self._patterns

    @patterns.setter
    def patterns(self, patterns):
        """
        Adds to the regex replacement patterns.
        The pattern should be a tuple with format (regex expression, string to insert).
        The input can be either a tuple with that pattern, a list of such tuples, or a tuple of such tuples.
        :param patterns: tuple, list
        """
        # Usually patterns is a tuple, so start by listifying it
        self._patterns = list(self._patterns)

        # Now figure out what the hell we just received
        if isinstance(patterns, tuple) and isinstance(patterns[0], str):
            # The input is a single replacement pattern, so wrap it in a list
            patterns = list(patterns)

        # Now the input is (hopefully) something iterable containing pattern tuples
        for p in patterns:
            new_pattern = (re.compile(p[0]), p[1])
            self._patterns.append(new_pattern)

        # re-tuple the stored patterns
        self._patterns = tuple(self._patterns)

    def process(self, text, **kwargs):
        """
        Arguments:
            text: The text to subject to regex replacement
            :param kwargs:
            :returns: Modified text if regex found, original if not
        """
        s = text
        for (pattern, repl) in self._patterns:
            (s, count) = re.subn(pattern, repl, s)
        return s

    def add_compiled_regex_pattern(self, compiled_pattern, replacement):
        """
        After several hours of trying to figure out how to pass in raw strings to add
        regex patterns, I gave up and added this. Grrr.
        :param compiled_pattern: A compiled regex pattern to apply
        :param replacement: The string to replace the pattern with
        """
        self._patterns = list(self._patterns)
        self._patterns.append((compiled_pattern, replacement))
        # re-tuple the stored patterns
        self._patterns = tuple(self._patterns)


class Lemmatizer(IModifier):
    """
    Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
    """

    def __init__(self):
        IModifier.__init__(self)
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def process(self, text, **kwargs):
        """
        Args:
            text: String to be lemmatized
        Returns:
            Lemmatized string
        """
        try:
            self._check_is_single_word(text)
            assert (type(text) is str)
            return self.lemmatizer.lemmatize(text)
        except Exception as e:
            print(e)


class PorterStemmer(IModifier):
    """
    Wrapper on nltk's porter-stemmer
    """

    def __init__(self):
        IModifier.__init__(self)
        self.stemmer = nltk.stem.PorterStemmer()

    def process(self, text, **kwargs):
        """
        TODO: Make sure only a single word passed in
        Executes the porter stem and returns the stemmed word
        Args:
            text: String to stem
        Returns:
            Porter stemmed string
        """
        try:
            self._check_is_single_word(text)
            assert (type(text) is str)
            return self.stemmer.stem(text)
        except Exception as e:
            print(e)

###################################
# INgramFilter implementations    #
###################################


class CustomFilter(INgramFilter):
    """
    Wrapper for applying arbitrary filter to the collocation finder
    e.g., for getting where 'and' is at trigram[1] but not beginning or end: lambda w1, w2, w3: 'and' in (w1, w3)
    """

    def __init__(self):
        self.filter_function = lambda x: x
        INgramFilter.__init__(self)

    def set_filter(self, filter_function):
        self.filter_function = filter_function

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        """
        assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
        return collocation_finder.apply_ngram_filter(self.filter_function)


class WordFilter(INgramFilter):
    """
    Wrapper for filtering by specific strings
    Make sure to set filter_words before calling filter
    Attributes:
        _filter_words: Tuple holding words to filter by, can be set with string, tuple, or list
    """

    def __init__(self):
        self._filter_words = ()
        INgramFilter.__init__(self)

    @property
    def filter_words(self):
        return self._filter_words

    @filter_words.setter
    def filter_words(self, words):
        """
        adds words to the internally held tuple of filter_words
        Arguments:
            :param words: Tuple, list, or individual word to add to the filter words
        """
        self._filter_words = list(self._filter_words)
        if isinstance(words, list):
            self._filter_words += words
        elif isinstance(words, str):
            self._filter_words.append(words)
        elif isinstance(words, tuple):
            self._filter_words += list(words)
        self._filter_words = tuple(self._filter_words)

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        """
        assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
        return collocation_finder.apply_word_filter(lambda w: w in self.filter_words)


class TextClassification(object):
    """
    Tools for classifying text
    """

    @staticmethod
    def tag_parts_of_speech(word_list):
        return nltk.pos_tag(word_list)


# ------------------------------------------------------------ deprecated ---------------------------------

#
# class TextFilters(object):
#     """
#     @deprecated
#     DEPRECATED
#     This has filters for removing various strings and string components.
#     This really shouldn't be used
#
#     """
#
#
#     @staticmethod
#     @deprecated
#     def remove_numerals(word_list):
#         """
#         DEPRECATED
#         Filters out all non-alphanumeric characters
#         :param word_list:
#         :return:
#         """
#         return [word for word in word_list if word.isalpha() is True]
#
#
#     @staticmethod
#     @deprecated
#     def remove_fragments(wordlist):
#         """
#         DEPRECATED
#         Filters string fragments from the list and returns the filtered list
#
#         Args:
#             wordlist: A list of words to have fragments removed from
#
#         Returns:
#             The filtered list
#         """
#         wordlist = [w for w in wordlist if w not in Ignore.fragments]  # remove fragments
#         return wordlist
#
#     @staticmethod
#     @deprecated
#     def remove_punctuation(word_list):
#         """
#         DEPRECATED
#         Filters out punctuation from input list. Does not filter at the word level (e.g., will not remove the period in "cat.")
#
#         Args:
#             word_list: A list of strings to be filtered for list items which are punctuation marks.
#
#         Returns:
#             The filtered list
#         """
#         punctuation = string.punctuation
#         punctuation = ['.', ',', '--', '?', ')', '(', ':', '\'', '"', '""', '-', '}', '{',
#                              '://', '/"', '\xc2\xb2', '...', '???', '..']
#         [punctuation.append(x) for x in string.punctuation]
#         return [w for w in word_list if w not in punctuation]
#
#     @staticmethod
#     @deprecated
#     def filter_stopwords(wordlist):
#         """
#         DEPRECATED
#         Uses NLTK English stopwords corpus to remove stopwords.
#
#         Args:
#             wordlist: List of strings to be filtered
#
#         Returns:
#             Filtered list
#         """
#         return [w for w in wordlist if w not in nltk.corpus.stopwords.words('english')]
#
#     @staticmethod
#     @deprecated
#     def lemmatize(word_list):
#         """
#         DEPRECATED
#         Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
#         Args:
#             word_list: List of words
#         Returns:
#             List of lemmatized words
#         """
#
#         try:
#             assert(type(word_list) is list)
#             lemmatizer = nltk.stem.WordNetLemmatizer()
#             return [lemmatizer.lemmatize(w) for w in word_list]
#         except Exception as e:
#             print(e)
#
#     @staticmethod
#     @deprecated
#     def porter_stem(word_list):
#         """
#         DEPRECATED
#         Wrapper on porterstemmer
#
#         Args:
#             word_list: List of words
#         Returns:
#             Porter stemmed list
#         """
#         try:
#             assert(type(word_list) is list)
#             stemmer = nltk.stem.PorterStemmer()
#             return [stemmer.stem(w) for w in word_list]
#         except Exception as e:
#             print(e)

if __name__ == '__main__':
    pass

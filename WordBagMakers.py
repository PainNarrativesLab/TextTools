"""
Created by adam on 11/11/15
Formerly in TextTools
"""
__author__ = 'adam'

from TextCleaningTools import *

from ProcessingTools.ProcessingModulesBases import IProcessor
# class IProcessor(object):
#
#     def __init__(self):
#         self._modifiers = []
#         self._listmodifiers = [ ]
#         self._filters = []
#         self._ngram_filters = []
#
#     def add_to_modifiers(self, imodifier):
#         """
#         Adds an object which does modification to the que of modifiers which get
#         called by _check_unwanted()
#         Example:
#             bagmaker.add_to_cleaners(URLFilter())
#             bagmaker.add_to_cleaners(UsernameFilter())
#             bagmaker.add_to_cleaners(NumeralFilter())
#
#         Args:
#             icleaner: IFilter inheriting object
#         """
#         if isinstance(imodifier, IModifier):
#             self._modifiers.append(imodifier)
#         elif isinstance(imodifier, IModifierList):
#             self._modifiers.append( imodifier )
#         else:
#             raise ValueError
#
#     def add_to_filters(self, ifilter):
#         """
#         Adds an object which does filtration to the que of filtration
#         Example:
#             bagmaker.add_to_cleaners(URLFilter())
#             bagmaker.add_to_cleaners(UsernameFilter())
#             bagmaker.add_to_cleaners(NumeralFilter())
#
#         Args:
#             ifilter: IFilter inheriting object
#         """
#         if isinstance(ifilter, IFilter):
#             self._filters.append(ifilter)
#         elif isinstance(ifilter, INgramFilter):
#             self._ngram_filters.append(ifilter)
#         else:
#             raise ValueError
#
#     def process(self, to_process, **kwargs):
#         """
#         The main interface
#         Args:
#             to_process: Something which will be processed
#         """
#         raise NotImplementedError

class WordBagMaker(IProcessor):
    """
    General class for taking something with strings and processing the text for bag of words type analyses.

    Before running the run command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of IFilter objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
    """

    def __init__(self):
        super().__init__()
        self._ignore = ()
        # self._modifiers = []
        # self._listmodifiers = [ ]
        # self._filters = []
        # self._cleaners = []
        self.masterbag = []

    def add_to_ignorelist(self, list_to_ignore):
        """
        Add a list of strings to the internally held tuple of strings to ignore in processing text
        Example:
            bagmaker = WordBagMaker()
            bagmaker.add_to_ignorelist(ignore.get_list())
            bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
            bagmaker.add_to_ignorelist(list(string.punctuation))

        Args:
            list_to_ignore: List of strings to ignore.
        """
        self._ignore = list(self._ignore)
        [self._ignore.append(i) for i in list_to_ignore]
        self._ignore = set(self._ignore)
        self._ignore = tuple(self._ignore)

    # def add_to_cleaners(self, icleaner):
    #     """
    #     Adds an object which does cleaning to the que of cleaners which get
    #     called by _check_unwanted()
    #     Example:
    #         bagmaker.add_to_cleaners(URLFilter())
    #         bagmaker.add_to_cleaners(UsernameFilter())
    #         bagmaker.add_to_cleaners(NumeralFilter())
    #
    #     Args:
    #         icleaner: IFilter inheriting object
    #     """
    #     assert(isinstance(icleaner, IFilter))
    #     self._cleaners.append(icleaner)
    #
    # def add_to_modifiers(self, imodifier):
    #     """
    #     Adds an object which does modification to the que of modifiers which get
    #     called by _check_unwanted()
    #     Example:
    #         bagmaker.add_to_cleaners(URLFilter())
    #         bagmaker.add_to_cleaners(UsernameFilter())
    #         bagmaker.add_to_cleaners(NumeralFilter())
    #
    #     Args:
    #         icleaner: IFilter inheriting object
    #     """
    #     if isinstance(imodifier, IModifier):
    #         self._modifiers.append(imodifier)
    #     elif isinstance(imodifier, IModifierList):
    #         self._modifiers.append( imodifier )
    #     else:
    #         raise ImportWarning
    #
    # def add_to_filters(self, ifilter):
    #     """
    #     Adds an object which does filtration to the que of filtration
    #     Example:
    #         bagmaker.add_to_cleaners(URLFilter())
    #         bagmaker.add_to_cleaners(UsernameFilter())
    #         bagmaker.add_to_cleaners(NumeralFilter())
    #
    #     Args:
    #         ifilter: IFilter inheriting object
    #     """
    #     assert(isinstance(ifilter, INgramFilter))
    #     self._filters.append(ifilter)


    def process(self, to_process):
        """
        Processes list of strings into a word bag stored in self.masterbag

        Args:
            to_process: List of strings to run
        """
        assert(isinstance(to_process, list))
        for t in to_process:
            # run text
            words = self._make_wordbag(t)
            words = [w for w in words if self._check_unwanted(w) and w not in self._ignore]
            self.masterbag += words

    def _make_wordbag(self, text):
        """
        Takes a bunch of sentences and extracts all the words, makes them lowercase, and returns them in a list

        Args:
            text: String text to be word tokenized

        Returns:
            List of words, all lower case
        """
        return [word.lower() for sent in nltk.tokenize.sent_tokenize(text) for word in nltk.tokenize.word_tokenize(sent)]

    def _check_unwanted(self, word):
        """
        Args:
            word: String to evaluate with IFilter objects in _cleaners
        Returns:
            False if the the string is to be left out
            True if the string is to be included
        """
        for cleaner in self._cleaners:
            if cleaner.clean(word) is False:
                return False
        return True


class TweetTextWordBagMaker(WordBagMaker):
    """
    This takes a list of dictionaries containing tweetID and tweetText and processes the texts for bag of words type analyses.

    Before running the run command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of IFilter objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
        tweet_tuples: List containing tuples with the structure (tweetID, [list of words in tweet])
    """
    def __init__(self):
        self.tweet_tuples = []
        WordBagMaker.__init__(self)

    def process(self, to_process):
        """
        Args:
            to_process: List of tweet dictionary objects with keys 'tweetID' and 'tweetText'

        Best time 225.85651803

        Example
        bagmaker = TweetTextWordBagMaker()
        bagmaker.add_to_ignorelist(ignore.get_list())
        bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        """
        for t in to_process:
            tweetid = t['tweetID']
            # run text
            words = self._make_wordbag(t['tweetText'])
            words = [w for w in words if self._check_unwanted(w) and w not in self._ignore]
            # run tuple
            tweet_tuple = (tweetid, words)
            self.tweet_tuples.append(tweet_tuple)
            self.masterbag += words


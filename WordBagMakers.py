"""
Created by adam on 11/11/15
Formerly in TextTools
"""
__author__ = 'adam'


class WordBagMaker(object):
    """
    General class for taking something with strings and processing the text for bag of words type analyses.

    Before running the process command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of ICleaner objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
    """

    def __init__(self):
        self._ignore = ()
        self._cleaners = []
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

    def add_to_cleaners(self, icleaner):
        """
        Adds an object which does cleaning to the que of cleaners which get
        called by _check_unwanted()
        Example:
            bagmaker.add_to_cleaners(URLCleaner())
            bagmaker.add_to_cleaners(UsernameCleaner())
            bagmaker.add_to_cleaners(NumeralCleaner())

        Args:
            :param icleaner: ICleaner inheriting object
        """
        assert(isinstance(icleaner, ICleaner))
        self._cleaners.append(icleaner)

    def process(self, to_process):
        """
        Processes list of strings into a word bag stored in self.masterbag

        Args:
            :param to_process: List of strings to process
        """
        assert(isinstance(to_process, list))
        for t in to_process:
            # process text
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
            word: String to evaluate with ICleaner objects in _cleaners
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

    Before running the process command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of ICleaner objects
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
            # process text
            words = self._make_wordbag(t['tweetText'])
            words = [w for w in words if self._check_unwanted(w) and w not in self._ignore]
            # process tuple
            tweet_tuple = (tweetid, words)
            self.tweet_tuples.append(tweet_tuple)
            self.masterbag += words

    # def OLDprocess(self, list_of_dicts):
    #     for t in list(self.results):
    #         tweetid = t['tweetID']
    #         #process text
    #         words = [word for sent in sent_tokenize(t['tweetText']) for word in word_tokenize(sent)]
    #         words = [w.lower() for w in words]
    #         words = [w for w in words if w not in Ignore.punctuation]  #remove punctuation
    #         words = [w for w in words if w not in Ignore.fragments]  #remove fragments
    #         words = [w for w in words if w[0] != '@']  #Get rid of usernames
    #         words = [w for w in words if w[0:6] != '//t.co']  #Remove some urls
    #         words = [w for w in words if w not in Ignore.words['socialmediaterms']]  #Remove terms from social media
    #         words = [w for w in words if w not in nltk.corpus.stopwords.words('english')]  #Remove stopwords
    #         #process tuple
    #         tweet_tuple = (tweetid, words)
    #         self.tweet_tuples.append(tweet_tuple)
    #         self.masterbag += words
        # def process(self, list_of_dicts):
    #     """
    #     Processes the tweet texts
    #     Most recent execution time 599.286342144 sec for 732683 tweets
    #     Moved stopwords filtration first: 891.928412914 for 732683 tweets
    #     Merged stopwords into ignore list: 234.204810858
    #     1 loops, best of 3: 14min 56s per loop
    #
    #     Args:
    #         list_of_dicts: List of dictionaries with keys tweetID and tweetText
    #     """
    #     for t in list_of_dicts:
    #         tweetid = t['tweetID']
    #         # process text
    #         words = self._make_wordbag(t['tweetText'])
    #         # words = self._filter_stopwords(words)
    #         words = self._filter_ignored_terms(words)
    #         words = self._filter_usernames(words)
    #         words = self._filter_urls(words)
    #         # process tuple
    #         tweet_tuple = (tweetid, words)
    #         self.tweet_tuples.append(tweet_tuple)
    #         self.masterbag += words

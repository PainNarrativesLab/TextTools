import string


class Ignore(object):
    """
    This contains terms to be filtered .
    It gets instantiated by other classes which do cleaning
    
    Attributes:
        fragments: (Class attribute) String fragments which should be filtered out
        words: (Class attribute) Dictionary with categories of irrelevant terms as
            keys (placenames, smallwords, socialmediaterms, irrelevant)
        word_tuple: (Class attribute and instance attribute) Tuple with everything to ignore
    """
    fragments = ["'s", "amp", '...', '//t.co', "'re'", "'m"]

    # Note these are in addition to string.punctuation which gets added on instantiation
    punctuation = ['.', ',', '--', '?', ')', '(', ':', '\'', '"', '""', '-', '}', '{',
                   '://', '/"', '\xc2\xb2', '...', '???', '..']
    words = {
        'placenames': ('tn', 'nashville', 'memphis', 'tennessee', 'knoxville', 'fl', 'tx', 'sc', 'nc', 'co',
                       'nyc', 'va', 'ga', 'twittoma', 'team243'),
        'smallwords': ('no', 'be', 'my', 'the', 'like', 'in', 'i', 'a', 'you', 'is', 'of', 'and', 'it', 'to',
                       'this', 'so', 'for', 'on', 'up'),
        'socialmediaterms': ('hashtag', 'selfie', 'repost', 'nofilter',
                             'instagram', 'instamood', 'instalike',
                             'instadaily', 'picoftheday', 'photo', 'instapic',
                             'http', 'rt', 'mt'),
        'irrelevant': ('recordstoreday', 'vinyl', 'naruto', 'bread')
    }

    def __init__(self):
        self._construct()
        self.word_tuple = Ignore.word_tuple

    def generator(self):
        """
        Generator which returns ignore words
        Example:
            generator = Ignore.generator()
            next(generator)
        """
        for word in self.word_tuple:
            yield word

    @classmethod
    def get_list(cls):
        """
        Returns a list of everything to ignore
        """
        cls._construct()
        return list(cls.word_tuple)

    @classmethod
    def _construct(cls):
        """
        Constructs the list of things to ignore at the class level from
        various sources.
        Note: This uses the string built in list of punctuation
        """
        word_list = []
        word_list += cls.fragments
        word_list += cls.punctuation
        [word_list.append(x) for x in string.punctuation]
        [word_list.append(word) for k in list(Ignore.words.keys()) for word in Ignore.words[k]]
        cls.word_tuple = tuple(word_list)


if __name__ == '__main__':
    pass

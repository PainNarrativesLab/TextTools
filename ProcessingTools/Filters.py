"""
This contains text modification tools which
receive a string and return a boolean for whether
that string should be included in the resulting data

Created by adam on 11/8/16
"""
__author__ = 'adam'


class IFilter( object ):
    """
    Interface for text processing objects which take a word as input and
    return True or False to indicate whether the string should be
    included in the resulting data

    These are normally placed in a queue and then ran in sequence as part
    of a list comprehension. Objects like TweetTextWordBagMaker receive
    a list of these objects
    """

    def __init__(self):
        pass

    def run( self, word, **kwargs ):
        """Runs the operation on the string. This is the main method"""
        raise NotImplementedError

#####################################
# IFilter implementations          #
#####################################

class IgnoreListFilter(IFilter):
    """
        Detects whether the string is in the ignore list and returns
        a boolean so it can be removed.
        TODO: Make this better
        """
    __name__ = 'IgnoreListFilter'

    def __init__( self ):
        super( ).__init__(  )
        self._ignore = ()

    def run( self, word, **kwargs ):
        if word in self._ignore:
            return False
        else:
            return True

    def add_to_ignorelist( self, to_ignore ):
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
        #wrap in list so can accept non-iterables
        to_ignore = [to_ignore] if isinstance(to_ignore, str) else to_ignore
        self._ignore = list( self._ignore )
        [ self._ignore.append( i ) for i in to_ignore ]
        self._ignore = set( self._ignore )
        self._ignore = tuple( self._ignore )


class URLFilter( IFilter ):
    """
    Detects whether the string is a url and returns
    a boolean so it can be removed.
    NB, This is tweet url specific
    TODO: Make this better
    """
    __name__ = 'URLFilter'

    def __init__( self ):
        super().__init__(  )

    def run( self, word, **kwargs ):
        if word[ 0:6 ] != '//t.co':
            return True
        else:
            return False


class UsernameFilter( IFilter ):
    """
    Filters out twitter usernames
    """
    __name__ = 'UsernameFilter'

    def __init__( self ):
        super().__init__(  )

    def run( self, word, **kwargs ):
        assert (type( word ) is str)
        if word[ 0 ] != '@' and word[ 0:1 ] != '.@':
            return True
        else:
            return False


class NumeralFilter( IFilter ):
    """
    Filters out all non-alphanumeric characters
    """
    __name__ = 'NumeralFilter'

    def __init__( self ):
        super( ).__init__(  )

    def run( self, word, **kwargs ):
        if isinstance(word,  str):
            return word.isalpha( )
        else:
            return False


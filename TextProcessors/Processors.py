"""
These bind together a set of filters, modifiers, and tokenizers into an
object which handles the actual processing tasks.

However, these processors do not provide any other handling or control.
Those are the responsibility of the consumer of these objects.

Created by adam on 11/8/16
"""
__author__ = 'adam'

# import ProcessingModulesBases

import TextProcessors
# import TextProcessors.Filters as Filters
import TextProcessors.Modifiers
import TextProcessors.NgramFilters


class IProcessor(object):
    """
    This is the base class for the single operation modules
    which are used to process text
    """

    def __init__(self):
        self._modifiers = []
        self._listmodifiers = [ ]
        self._filters = []
        self._ngram_filters = []

    def add_to_modifiers(self, imodifier):
        """
        Adds an object which does modification to the que of modifiers which get
        called by _check_unwanted()
        Example:
            bagmaker.add_to_cleaners(URLFilter())
            bagmaker.add_to_cleaners(UsernameFilter())
            bagmaker.add_to_cleaners(NumeralFilter())

        Args:
            imodifier: IModifier or IModifierList inheriting object
        """
        if isinstance(imodifier, TextProcessors.Modifiers.IModifier):
            self._modifiers.append(imodifier)
        elif isinstance(imodifier, TextProcessors.Modifiers.IModifierList):
            self._modifiers.append( imodifier )
        else:
            raise ValueError

    def add_to_filters(self, ifilter):
        """
        Adds an object which does filtration to the stack of filters
        Example:
            bagmaker.add_to_cleaners(URLFilter())
            bagmaker.add_to_cleaners(UsernameFilter())
            bagmaker.add_to_cleaners(NumeralFilter())

        Args:
            ifilter: IFilter inheriting object
        """
        # print(type(ifilter))
        if isinstance(ifilter, TextProcessors.Filters.IFilter):
            print("Adding filter %s to filters stack" % ifilter.__name__)
            self._filters.append(ifilter)
        elif issubclass(ifilter, TextProcessors.NgramFilters.INgramFilter):
            self._ngram_filters.append(ifilter)
        else:
            print("Error attempting to add filter %s to filters stack" % ifilter.__name__)
            raise ValueError

    def set_initial_transforms(self, listOfModifiers, **kwargs ):
        """
        Sets some modifiers to run before any other operations happen.
        """
        raise NotImplementedError

    def process(self, to_process, **kwargs):
        """
        The main interface
        Args:
            to_process: Something which will be processed
        """
        raise NotImplementedError


class SingleWordProcessor( IProcessor ):
    """
    Runs filtration and transformation operations on one
    string at a time returning either the modified string
    or None
    """
    def __init__( self ):
        super( ).__init__( )

    def process( self, to_process ):
        """
        Processes one word at a time by first running all modifiers
        in stack and then running all filters in stack

        Args:
            to_process: Single word to process
        """
        # print( 'start: %s' % to_process )
        assert (isinstance( to_process, str ))

        # Run modifiers first so will be in a standard form
        to_process = self._run_modifiers( to_process )

        # Run filters and return tokens which aren't screened out
        if self._run_filters( to_process ) is True:
            # print( 'filter complete: %s' % to_process )
            return to_process
        else:
            # Return none if the token was filtered out
            return None

    def _run_modifiers( self, text ):
        if len( self._modifiers ) > 0:
            for modifier in self._modifiers:
                text = modifier.run( text )
                # print( text )
        return text

    def _run_filters( self, word ):
        """Runs all filters"""
        if len( self._filters ) > 0:
            for f in self._filters:
                # print( 'running filter \n filtername: %s \n word: %s' % (f.__name__, word) )
                if f.run( word ) is False:
                    # print( 'filter %s failed: %s' % (f.__name__, word) )
                    return False
        return True
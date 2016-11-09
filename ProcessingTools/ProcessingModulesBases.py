"""
Created by adam on 11/8/16
"""
__author__ = 'adam'

from Filters import *
from Modifiers import *
from NgramFilters import *


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
            icleaner: IFilter inheriting object
        """
        if isinstance(imodifier, IModifier):
            self._modifiers.append(imodifier)
        elif isinstance(imodifier, IModifierList):
            self._modifiers.append( imodifier )
        else:
            raise ValueError

    def add_to_filters(self, ifilter):
        """
        Adds an object which does filtration to the que of filtration
        Example:
            bagmaker.add_to_cleaners(URLFilter())
            bagmaker.add_to_cleaners(UsernameFilter())
            bagmaker.add_to_cleaners(NumeralFilter())

        Args:
            ifilter: IFilter inheriting object
        """
        if isinstance(ifilter, IFilter):
            self._filters.append(ifilter)
        elif isinstance(ifilter, INgramFilter):
            self._ngram_filters.append(ifilter)
        else:
            raise ValueError

    def set_initial_transforms(self, listOfModifiers, **kwargs ):
        """
        Sets some modifiers to run before any other operations happen.
        This is """

        pass

    def process(self, to_process, **kwargs):
        """
        The main interface
        Args:
            to_process: Something which will be processed
        """
        raise NotImplementedError


if __name__ == '__main__':
    pass
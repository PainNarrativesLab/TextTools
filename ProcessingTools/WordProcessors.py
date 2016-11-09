"""
Created by adam on 11/8/16
"""
__author__ = 'adam'
from ProcessingModulesBases import *


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
        Processes one word at a time

        Args:
            to_process: Single word to process
        """
        print( 'start: %s' % to_process )
        assert (isinstance( to_process, str ))

        # Run modifiers first so will be in a standard form
        to_process = self._run_modifiers( to_process )
        if self._run_filters( to_process ) is True:
            print( 'filter complete: %s' % to_process )
            return to_process
        else:
            print( 'filter failed: %s' % (to_process) )
            return None

    def _run_modifiers( self, text ):
        if len( self._modifiers ) > 0:
            for modifier in self._modifiers:
                text = modifier.run( text )
                print( text )
        return text

    def _run_filters( self, word ):
        """Runs all filters"""
        if len( self._filters ) > 0:
            for f in self._filters:
                print( 'running filter \n filtername: %s \n word: %s' % (f.__name__, word) )
                if f.run( word ) is False:
                    return False
        return True


if __name__ == '__main__':
    pass
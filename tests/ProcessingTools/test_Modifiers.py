import unittest

from ProcessingTools import Modifiers as M

class CaseConverterTest( unittest.TestCase ):
    def test_happy_lower( self ):
        obj = M.CaseConverter()
        self.assertEqual( 'taco', obj.run( ' TACO' ) )


    def test_happy_upper( self ):
        obj = M.CaseConverter(False)
        self.assertEqual( 'TACO', obj.run( 'Taco ' ) )


if __name__ == '__main__':
    unittest.main( )

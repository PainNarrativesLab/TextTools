import unittest
import string
from Filters import IgnoreListFilter as ILF
from Filters import NumeralFilter as NF
from Filters import UsernameFilter as UF
from Filters import PunctuationFilter as PF

class IgnoreListFilterTest( unittest.TestCase ):
    def test_add_to_ignorelist_list( self ):
        self.obj = ILF()
        test = ['taco', 'cat', 'fish']
        self.obj.add_to_ignorelist(test)
        self.assertIsInstance(self.obj._ignore, tuple)
        [self.assertIn( w, self.obj._ignore) for w in test]


    def test_add_to_ignorelist_string( self ):
        self.obj = ILF()
        test = 'taco'
        self.obj.add_to_ignorelist( test )
        self.assertIsInstance( self.obj._ignore, tuple )
        self.assertEqual( self.obj._ignore, tuple( [test] ) )




class NumeralFilterTest( unittest.TestCase ):
    def test_happy_path_is_string( self ):
        self.obj = NF()
        test = 'taco'

        self.assertTrue(self.obj.run(test))

    def test_happy_path_not_string( self ):
        self.obj = NF()
        test = 5
        self.assertFalse(self.obj.run(test))


    def test_happy_path_num_string( self ):
        self.obj = NF( )
        test = '5'
        self.assertFalse( self.obj.run( test ) )



class PunctuationFilterTest( unittest.TestCase ):
    def test_happy_path_string( self ):
        self.obj = PF()
        test = 'taco'

        self.assertTrue(self.obj.run(test))

    def test_happy_path_punctuation( self ):
        self.obj = PF()
        [self.assertFalse(self.obj.run(i)) for i in list(string.punctuation)]


    def test_happy_path_num_string( self ):
        self.obj = PF( )
        test = '5'
        self.assertTrue( self.obj.run( test ) )


    def test_happy_path_number( self ):
        self.obj = PF( )
        test = 5
        self.assertTrue( self.obj.run( test ) )


if __name__ == '__main__':
    unittest.main( )

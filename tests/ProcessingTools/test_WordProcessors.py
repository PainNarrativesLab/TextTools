import unittest

import Processors
import Filters

from faker import Faker

class SingleWordProcessorTest( unittest.TestCase ):
    def setUp(self):
        self.obj = Processors.SingleWordProcessor( )
        self.faker = Faker()

    def test_happy_process( self ):
        self.skipTest( 'TODO: WRITE TEST' )

    def test_happy_run_modifiers(self):
        self.skipTest('TODO: WRITE TEST')

    def test_happy_run_filters(self):
        test = self.faker.word( )
        nf = Filters.NumeralFilter( )
        print(type(nf))
        self.assertTrue(isinstance(nf, Filters.IFilter))
        self.obj.add_to_filters(nf)
        self.obj.add_to_filters(Filters.PunctuationFilter())

        self.assertTrue(len(self.obj._filters) is 2)

        self.assertEquals(True, self.obj._run_filters(test))
        self.assertEquals(False, self.obj._run_filters('5'))
        self.assertEquals(False, self.obj._run_filters( '.' ) )

    def test_process_none_loaded( self ):
        test = self.faker.word()
        result = self.obj.process(test)
        self.assertEqual( test, result )

    def test_run_modifiers_no_modifiers(self):
        test = self.faker.word( )
        result = self.obj._run_modifiers( test )
        self.assertEqual( test, result )

    def test_run_filters_no_filters(self):
        test = self.faker.word( )
        result = self.obj._run_filters( test )
        self.assertEqual( True, result )

if __name__ == '__main__':
    unittest.main( )

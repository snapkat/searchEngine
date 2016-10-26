from crawler import crawler as c
import unittest


class CrawlerTest(unittest.TestCase):
    ignored_tags = set([
        'meta', 'script', 'link', 'meta', 'embed', 'iframe', 'frame',
        'noscript', 'object', 'svg', 'canvas', 'applet', 'frameset',
        'textarea', 'style', 'area', 'map', 'base', 'basefont', 'param',
    ])

    ignored_words = set([
        '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
    ])

    URL1 = 'http://localhost:8080/test/1/testcode1.html'
    URL2 = 'http://localhost:8080/test/1/testcode2.html'
    URL3 = 'http://localhost:8080/test/1/testcode3.html'

    TEST1_1 = '''testing code 1 the cat in the hat to
                        testcode2 to testcode3 '''
    TEST1_2 = '''testing code 2 the quick fox jumped over to testcode4 '''
    TEST1_3 = '''testing code 3 the lazy brown
                 dog to testcode6 to testcode7 '''

    def setUp(self):
        print '!!!Make sure to have server.py running at localhost:8080!!!'
        print 'Check the server requests to ensure things running correctly!'
        print "(If not, restart server)"

    def test1(self):
        ''' Checks that words are correctly found
        '''
        bot = c(None, 'test1.txt')
        bot.crawl(depth=0)
        inv_index = bot.get_resolved_inverted_index()
        words = set(inv_index.keys())

        ground_truth = CrawlerTest.test1_1
        ground_truth = set(ground_truth.split()) - CrawlerTest.ignored_words
        self.assertTrue(words == ground_truth)

    def test2(self):
        ''' Checks the crawler goes across pages and keeps correct
            document to word mappings
        '''
        bot = c(None, 'test1.txt')
        bot.crawl(depth=1)
        inv_index = bot.get_resolved_inverted_index()
        words = set(inv_index.keys())

        secnd_page_words = CrawlerTest.test1_2

        # Check that all words in doc2 references doc2
        # and that nothing else does.
        for word in inv_index:
            if word in secnd_page_words:
                self.assertTrue(CrawlerTest.URL2 in inv_index[word])
            else:
                self.assertTrue(CrawlerTest.URL2 not in inv_index[word])

        # Compare the lists of found words to ensure
        # that first 3 pages have been visited (and only the first three)
        ground_truth = CrawlerTest.TEST1_1 + CrawlerTest.TEST1_2 + CrawlerTest.TEST1_3
        ground_truth = set(ground_truth.split()) - CrawlerTest.ignored_words
        self.assertTrue(words == ground_truth)


if __name__ == "__main__":
    unittest.main()

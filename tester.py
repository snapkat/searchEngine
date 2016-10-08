from crawler import crawler as c
import server
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

    def setUp(self):
        server.main()

    def test1(self):
        ''' Checks that words are correctly found
        '''
        bot = c(None, 'test1.txt')
        bot.crawl(depth=0)
        inv_index = bot.get_resolved_inverted_index()
        words = set(inv_index.keys())

        ground_truth = '''testing code 1 the cat in the hat to
                        testcode2 to testcode3'''
        ground_truth = set(ground_truth.split()) - CrawlerTest.ignored_words
        self.assertTrue(words == ground_truth)


if __name__ == "__main__":
    unittest.main()

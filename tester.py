from crawler import crawler as c
import unittest


class CrawlerTest(unittest.TestCase):

    def test1(self):
        bot = c(None, 'test1.txt')
        bot.crawl(depth=0)
        inv_index = bot.get_resolved_inverted_index()
        words = set(inv_index.keys())

        ground_truth = '''testing code 1 the cat in the hat to test
                        code2 to testcode3'''
        ground_truth = set(ground_truth.split())

        self.assertTrue(words == ground_truth)


if __name__ == "__main__":
    unittest.main()

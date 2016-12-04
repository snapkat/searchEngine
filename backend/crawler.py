# Copyright (C) 2011 by Peter Goodman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import urllib2
import urlparse
from BeautifulSoup import *
from collections import defaultdict
import re
import json
from HTMLParser import HTMLParser

import redis
from pg_rank import page_rank


def attr(elem, attr):
    """An html attribute from an html element. E.g. <a href="">, then
    attr(elem, "href") will get the href or an empty string."""
    try:
        return elem[attr]
    except:
        return ""


WORD_SEPARATORS = re.compile(r'\s|\n|\r|\t|[^a-zA-Z0-9\-_]')
redis_host = ""
with open('redis_host.json') as f:
    redis_host = json.loads(f.read())['host']

class crawler(object):
    """Represents 'Googlebot'. Populates a database by crawling and indexing
    a subset of the Internet.
    This crawler keeps track of font sizes and makes it simpler to manage word
    ids and document ids."""

    def __init__(self, db_conn, url_file):
        """Initialize the crawler with a connection to the database to populate
        and with the file containing the list of seed URLs to begin indexing.
        """

        self._url_queue = []
        self.r = redis.StrictRedis(host=redis_host, port=6379, db=0)
        self.r_rank = redis.StrictRedis(host=redis_host, port=6379, db=1)
        self.h = HTMLParser()

        '''
        self._id_to_url = {}
        self._id_to_word = {}
        self._word_id_to_doc_ids = {}
        self._word_to_id = {}
        self._doc_to_id = {}
        '''

        # Directed Graph; list of from-to tuple pairs
        self._url_graph = []

        # functions to call when entering and exiting specific tags
        self._enter = defaultdict(lambda *a, **ka: self._visit_ignore)
        self._exit = defaultdict(lambda *a, **ka: self._visit_ignore)

        # add a link to our graph, and indexing info to the related page
        self._enter['a'] = self._visit_a

        # record the currently indexed document's title an increase
        # the font size
        def visit_title(*args, **kargs):
            self._visit_title(*args, **kargs)
            self._increase_font_factor(7)(*args, **kargs)

        # increase the font size when we enter these tags
        self._enter['b'] = self._increase_font_factor(2)
        self._enter['strong'] = self._increase_font_factor(2)
        self._enter['i'] = self._increase_font_factor(1)
        self._enter['em'] = self._increase_font_factor(1)
        self._enter['h1'] = self._increase_font_factor(7)
        self._enter['h2'] = self._increase_font_factor(6)
        self._enter['h3'] = self._increase_font_factor(5)
        self._enter['h4'] = self._increase_font_factor(4)
        self._enter['h5'] = self._increase_font_factor(3)
        self._enter['title'] = visit_title

        # decrease the font size when we exit these tags
        self._exit['b'] = self._increase_font_factor(-2)
        self._exit['strong'] = self._increase_font_factor(-2)
        self._exit['i'] = self._increase_font_factor(-1)
        self._exit['em'] = self._increase_font_factor(-1)
        self._exit['h1'] = self._increase_font_factor(-7)
        self._exit['h2'] = self._increase_font_factor(-6)
        self._exit['h3'] = self._increase_font_factor(-5)
        self._exit['h4'] = self._increase_font_factor(-4)
        self._exit['h5'] = self._increase_font_factor(-3)
        self._exit['title'] = self._increase_font_factor(-7)

        # never go in and parse these tags
        self._ignored_tags = set([
            'meta', 'script', 'link', 'meta', 'embed', 'iframe', 'frame',
            'noscript', 'object', 'svg', 'canvas', 'applet', 'frameset',
            'textarea', 'style', 'area', 'map', 'base', 'basefont', 'param',
        ])

        # set of words to ignore
        self._ignored_words = set([
            '', 'the', 'of', 'at', 'on', 'in', 'is', 'it',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', 'and', 'or',
        ])

        # TODO remove me in real version
        self._next_doc_id = 1
        self._next_word_id = 1

        # keep track of some info about the page we are currently parsing
        self._curr_depth = 0
        self._curr_url = ""
        self._curr_doc_id = 0
        self._font_size = 0
        self._curr_words = None

        # get all urls into the queue
        try:
            with open(url_file, 'r') as f:
                for line in f:
                    self._url_queue.append(
                        (self._fix_url(line.strip(), ""), 0))
        except IOError:
            pass

    def get_inverted_index(self, cursor, count):
        """Returns inverted index mapping (from word id to document ids that
        contain the word)"""
        inv_ind = {}
        for k in self.r.scan_iter(match="word_id_to_doc_ids:*"):
            w_id = int(k.split(":", 1)[1])
            inv_ind[w_id] = self.r.smembers(k)

        return inv_ind

    def get_resolved_inverted_index(self):
        """Returns inverted index mapping, with ids replaced with words and
        urls"""
        r_inv_index = {}
        for word_id in self.r.scan_iter(match="word_id_to_doc_ids:*"):
            doc_id_set = self.r.smembers(word_id)
            word_id = word_id.split(":")[1]
            word = self.r.hget("id_to_word", word_id)
            doc_list = []
            for doc_id in doc_id_set:
                doc_list.append(self.r.hget("id_to_doc", doc_id))

            r_inv_index[word] = set(doc_list)
        return r_inv_index

    # TODO remove me in real version
    def _insert_document(self, url):
        """A function that pretends to insert a url into a document db table
        and then returns that newly inserted document's id."""
        doc_id = self._next_doc_id
        self._next_doc_id += 1
        self.r.hset("doc_to_id", url, doc_id)
        self.r.hset("id_to_doc", doc_id, url)
        return doc_id

    def _insert_word(self, word):
        """A function that pretends to instert a word into the lexicon db table
        and then returns that newly inserted word's id."""
        word_id = self._next_word_id
        self._next_word_id += 1
        self.r.hset("word_to_id", word, word_id)
        self.r.hset("id_to_word", word_id, word)
        return word_id

    def word_id(self, word):
        """Returns the word id of some specific word."""
        word_id = self.r.hget("word_to_id", word)
        if not word_id:
            word_id = self._insert_word(word)
        # TODO: 1) add the word to the lexicon, if that fails, then the
        #          word is in the lexicon
        #       2) query the lexicon for the id assigned to this word,
        #          store it in the word id cache, and return the id.
        return word_id

    def document_id(self, url):
        """Get the document id for some url."""
        doc_id = self.r.hget("doc_to_id", url)
        if not doc_id:
            doc_id = self._insert_document(url)
        # TODO: just like word id cache, but for documents. if the document
        #       doesn't exist in the db then only insert the url and leave
        #       the rest to their defaults.

        return doc_id

    def _fix_url(self, curr_url, rel):
        """Given a url and either something relative to that url or another url,
        get a properly parsed url."""

        rel_l = rel.lower()
        if rel_l.startswith("http://") or rel_l.startswith("https://"):
            curr_url, rel = rel, ""

        # compute the new url based on import
        curr_url = urlparse.urldefrag(curr_url)[0]
        parsed_url = urlparse.urlparse(curr_url)
        return urlparse.urljoin(parsed_url.geturl(), rel)

    def add_link(self, from_doc_id, to_doc_id):
        """Add a link into the database, or increase the number of links between
        two pages in the database."""
        # TODO

    def _visit_title(self, elem):
        """Called when visiting the <title> tag."""
        title_text = self._text_of(elem).strip()
        self.r.hset("doc_id_title", self._curr_doc_id, self.h.unescape(title_text))
        print "document title=" + repr(title_text)

        # TODO update document title for document id self._curr_doc_id

    def _visit_a(self, elem):
        """Called when visiting <a> tags."""

        dest_url = self._fix_url(self._curr_url, attr(elem, "href"))

        # print "href="+repr(dest_url), \
        #      "title="+repr(attr(elem,"title")), \
        #      "alt="+repr(attr(elem,"alt")), \
        #      "text="+repr(self._text_of(elem))

        # add the just found URL to the url queue
        self._url_queue.append((dest_url, self._curr_depth))

        # add a link entry into the database from the current document to the
        # other document
        self.add_link(self._curr_doc_id, self.document_id(dest_url))

        # TODO add title/alt/text to index for destination url

    # def _build_graph(self, elem):
        """Called when visiting <a> tags."""
        # Builds directed graph
        #dest_url = self._fix_url(self._curr_url, attr(elem, "href"))

        # Add current edge to graph
        dest_url_id = int(self.document_id(dest_url))
        curr_edge = (int(self._curr_doc_id), dest_url_id)
        self._url_graph.append(curr_edge)

    def _add_words_to_document(self):
        # TODO: knowing self._curr_doc_id and the list of all words and their
        #       font sizes (in self._curr_words), add all the words into the
        #       database for this document

        for word_id, _ in self._curr_words:
            self.r.sadd("word_id_to_doc_ids:%s" % word_id,
                        self._curr_doc_id)

        print "    num words=" + str(len(self._curr_words))

    def _increase_font_factor(self, factor):
        """Increade/decrease the current font size."""
        def increase_it(elem):
            self._font_size += factor
        return increase_it

    def _visit_ignore(self, elem):
        """Ignore visiting this type of tag"""
        pass

    def _add_text(self, elem):
        """Add some text to the document. This records word ids and word font sizes
        into the self._curr_words list for later processing."""
        words = WORD_SEPARATORS.split(elem.string.lower())
        for word in words:
            word = word.strip()
            if word in self._ignored_words:
                continue
            self._curr_words.append((self.word_id(word), self._font_size))

    def _text_of(self, elem):
        """Get the text inside some element without any tags."""
        if isinstance(elem, Tag):
            text = []
            for sub_elem in elem:
                text.append(self._text_of(sub_elem))

            return " ".join(text)
        else:
            return elem.string

    # def _get_doc_info(self, elem):
        """Gets the title and first 12 words of webpage"""

    def _index_document(self, soup):
        """Traverse the document in depth-first order and call functions when
        entering and leaving tags. When we come accross some text, add it into
        the index. This handles ignoring tags that we have no business looking
        at."""
        class DummyTag(object):
            next = False
            name = ''

        class NextTag(object):
            def __init__(self, obj):
                self.next = obj

        tag = soup.html
        stack = [DummyTag(), soup.html]

        while tag and tag.next:
            tag = tag.next

            # html tag
            if isinstance(tag, Tag):

                if tag.parent != stack[-1]:
                    self._exit[stack[-1].name.lower()](stack[-1])
                    stack.pop()

                tag_name = tag.name.lower()

                # ignore this tag and everything in it
                if tag_name in self._ignored_tags:
                    if tag.nextSibling:
                        tag = NextTag(tag.nextSibling)
                    else:
                        self._exit[stack[-1].name.lower()](stack[-1])
                        stack.pop()
                        tag = NextTag(tag.parent.nextSibling)

                    continue

                # enter the tag
                self._enter[tag_name](tag)
                stack.append(tag)

            # text (text, cdata, comments, etc.)
            else:
                self._add_text(tag)

    def crawl(self, depth=2, timeout=3):
        """Crawl the web!"""
        self.r.flushall()
        self.r_rank.flushall()

        seen = set()
        while len(self._url_queue):

            url, depth_ = self._url_queue.pop()

            # skip this url; it's too deep
            if depth_ > depth:
                continue

            doc_id = self.document_id(url)

            # we've already seen this document
            if doc_id in seen:
                continue

            seen.add(doc_id)  # mark this document as haven't been visited

            socket = None
            try:
                socket = urllib2.urlopen(url, timeout=timeout)
                soup = BeautifulSoup(socket.read())

                self._curr_depth = depth_ + 1
                self._curr_url = url
                self._curr_doc_id = doc_id
                self._font_size = 0
                self._curr_words = []
                self._index_document(soup)
                self._add_words_to_document()
                print "    url=" + repr(self._curr_url)

            except Exception as e:
                print e
                pass
            finally:
                if socket:
                    socket.close()

        # Gets the page rankings for each doc id
        doc_id_ranks = page_rank(self._url_graph)

        url_ranks = defaultdict()

        # For documents without outgoing links, set page rank to 0
        doc_id_to_url = self.r.hgetall("id_to_doc")

        all_doc_ids = doc_id_to_url.keys()
        int_doc_ids = [int(i) for i in all_doc_ids]

        # print type(doc_id_to_url[0])
        # Set pages with no outgoing links to rank 0
        for id in int_doc_ids:
            if id not in doc_id_ranks:
                doc_id_ranks[id] = 0

        # Url to rank mapping
        for doc_id, rank in doc_id_ranks.iteritems():
            curr_url = doc_id_to_url[str(doc_id)]
            url_ranks[curr_url] = rank

        # Save rankings to persistent storage
        self.r_rank.hmset("doc_id_ranks", doc_id_ranks)
        self.r_rank.hmset("url_ranks", url_ranks)

        # Get the resolved inverted index and save it
        resolved_inv_index = self.get_resolved_inverted_index()
        self.r_rank.hmset("resolved_inv_index", resolved_inv_index)


if __name__ == "__main__":
    bot = crawler(None, "urls.txt")
    bot.crawl(depth=1)
    print bot.get_resolved_inverted_index()

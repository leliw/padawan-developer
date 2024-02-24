"""Basic sententizer tests"""
import unittest
import sys
import logging

project_path = '/'.join(__file__.split('/')[:-3])
if project_path not in sys.path:
    sys.path.append(project_path)
logging.basicConfig(level=logging.DEBUG)

from tokenizer.basic_tokenizer import BasicTokenizer
from tokenizer.basic_sentencizer import BasicSentencizer

class TestBasicSentencizer(unittest.TestCase):


    def test_sentences(self):
        tokenizer = BasicTokenizer()
        code = """
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        """
        tokens = list(tokenizer.tokenize(code))
        sentencizer = BasicSentencizer()
        sentences = sentencizer.sentencize(tokens)
        self.assertEqual(3, len(sentences))

    def test_block(self):
        tokenizer = BasicTokenizer()
        code = """{
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        }"""
        tokens = list(tokenizer.tokenize(code))
        sentencizer = BasicSentencizer()
        sentences = sentencizer.sentencize(tokens)
        self.assertEqual(1, len(sentences))
        tokens2 = tokens[sentences[0].start:sentences[0].end]
        sentences = sentencizer.sentencize(tokens2)
        self.assertEqual(3, len(sentences))

    def test_block_in_block(self):
        tokenizer = BasicTokenizer()
        code = """{
        "port": 8999,
        "inner": { "a": "b" }
        }"""
        tokens = tokenizer.tokenize(code)
        tokens = [t for t in tokenizer.remove_whitespaces(tokens).values()]
        sentencizer = BasicSentencizer()
        sentences = sentencizer.sentencize(tokens)
        self.assertEqual(1, len(sentences))
        tokens2 = tokens[sentences[0].start:sentences[0].end]
        sentences = sentencizer.sentencize(tokens2)
        _ = [print(s) for s in sentences]
        self.assertEqual(2, len(sentences))
        self.assertEqual("\"port\":8999", sentences[0].get_body())
        self.assertEqual("\"inner\":{\"a\":\"b\"}", sentences[1].get_body())



if __name__ == '__main__':
    unittest.main()

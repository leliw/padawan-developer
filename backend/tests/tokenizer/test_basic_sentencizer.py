import unittest
import sys
import logging

project_path = '/'.join(__file__.split('/')[:-3])
print(project_path)
if (project_path not in sys.path):
    sys.path.append(project_path)
print(sys.path)
logging.basicConfig(level=logging.DEBUG)

from tokenizer.basic_tokenizer import BasicTokenizer
from tokenizer.basic_sentencizer import BasicSentencizer

class TestBasicSentencizer(unittest.TestCase):

    def test_basic(self):
        tokenizer = BasicTokenizer()
        code = """{
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        }"""
        tokens = tokenizer.tokenize(code)
        sentencizer = BasicSentencizer()
        sentences = sentencizer.sentencize(tokens)
        self.assertEqual(1, len(sentences))
        tokens2 = tokens[sentences[0].start:sentences[0].end]
        sentences = sentencizer.sentencize(tokens2)
        self.assertEqual(3, len(sentences))


if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import logging

project_path = '/'.join(__file__.split('/')[:-3])
print(project_path)
if (project_path not in sys.path):
    sys.path.append(project_path)
print(sys.path)
logging.basicConfig(level=logging.DEBUG)

from tokenizer.basic_tokenizer import Token, BasicTokenizer, basic_rules

class TestBasicTokenizer(unittest.TestCase):

    def test_basic_storage_string(self):
        tokenizer = BasicTokenizer(basic_rules)
        code = """{
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        }"""
        tokens = tokenizer.tokenize(code)
        tokenizer.print_tokens(tokens)
        self.assertEqual(24, len(tokens))


if __name__ == '__main__':
    unittest.main()
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

    def test_tokenize(self):
        tokenizer = BasicTokenizer()
        code = """{
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        }"""
        tokens = tokenizer.tokenize(code)
        tokenizer.print_tokens(tokens)
        self.assertEqual(24, len(tokens))

    def test_detokenize(self):
        tokenizer = BasicTokenizer()
        code = """{
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        }"""
        tokens = tokenizer.tokenize(code)
        tokenizer.print_tokens(tokens)
        string = tokenizer.detokenize(tokens)
        self.assertEqual(code, string)

    def test_conversion_to_ids(self):
        tokenizer = BasicTokenizer()
        code = """{
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        }"""
        tokens = tokenizer.tokenize(code)
        tokenizer.print_tokens(tokens)
        ids = [tokenizer._convert_token_to_id(token) for token in tokens]
        print(ids)
        self.assertEqual(24, len(ids))
    
    def test_conversion_to_tokens(self):
        tokenizer = BasicTokenizer()
        code = """{
        "port": 8999,
        "target_url": "https://example.com",
        "status": "working"
        }"""
        tokens = tokenizer.tokenize(code)
        ids = [tokenizer._convert_token_to_id(token) for token in tokens]
        print(ids)
        t2 = [tokenizer._convert_id_to_token(id_) for id_ in ids]   
        self.assertEqual(
            [str(t) for t in tokens], 
            [str(t) for t in t2]
            )


if __name__ == '__main__':
    unittest.main()
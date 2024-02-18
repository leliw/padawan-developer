import unittest
import sys
import logging

project_path = '/'.join(__file__.split('/')[:-3])
print(project_path)
if (project_path not in sys.path):
    sys.path.append(project_path)
print(sys.path)
logging.basicConfig(level=logging.DEBUG)

from tokenizer.ts_tokenizer import TsTokenizer


TEST_CODE = """export interface Status {
    status: string;
    port: number;
    target_url: string
}"""

class TestTsTokenizer(unittest.TestCase):

    def test_tokenize(self):
        tokenizer = TsTokenizer()
        tokens = tokenizer.tokenize(TEST_CODE)
        tokenizer.print_tokens(tokens)
        self.assertEqual(29, len(tokens))
    
    def test_detokenize(self):
        tokenizer = TsTokenizer()
        tokens = tokenizer.tokenize(TEST_CODE)
        tokenizer.print_tokens(tokens)
        string = tokenizer.detokenize(tokens)
        self.assertEqual(TEST_CODE, string)

    def test_conversion_to_tokens(self):
        tokenizer = TsTokenizer()
        tokens = tokenizer.tokenize(TEST_CODE)
        ids = [tokenizer._convert_token_to_id(token) for token in tokens]
        print(ids)
        t2 = [tokenizer._convert_id_to_token(id_) for id_ in ids]   
        self.assertEqual(
            [str(t) for t in tokens], 
            [str(t) for t in t2]
            )
        

if __name__ == '__main__':
    unittest.main()
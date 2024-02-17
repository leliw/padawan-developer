

from tokenizer.basic_tokenizer import Token

class Sentence:
   
    def __init__(self, type: str, start: int, end: int):
       self.type = type
       self.start = start
       self.end = end

    def __str__(self):
        return f'Token({self.type}, ({self.start}, {self.end}))'

class BasicSentencizer:
  
  def __init__(self, block_start='LBRACE', block_end='RBRACE', separator='COMMA'):
    self.block_start = block_start
    self.block_end = block_end
    self.separator = separator

  def sentencize(self, tokens: list[Token]) -> list:
    sentences = []
    start = None
    last = (0,0)
    for index, token in enumerate(tokens):
        if token.type == self.block_start and start is None:
            start = index+1
        elif token.type == self.block_end and start is not None:
            last = (start, index)
            start = None
            sentences.append(last)
        elif token.type == self.separator and start is None:
            last = (last[1], index+1)
            sentences.append(last)
    if last[1] < len(tokens)-1:
        last = (last[1], len(tokens))
        sentences.append(last)
    ret = []
    for s in sentences:
        if tokens[s[1]-1].type == self.separator:
            ret.append((s[0], s[1]-1))
        else:
            ret.append((s[0], s[1]))
    return ret
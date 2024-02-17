

from tokenizer.basic_tokenizer import Token

class Sentence:
   
    def __init__(self, type: str, start: int, end: int):
       self.type = type
       self.start = start
       self.end = end

    def __str__(self):
        return f'Token({self.type}, ({self.start}, {self.end}))'

class BasicSentencizer:
  
  def __init__(self, block_start='[LBRACE]', block_end='[RBRACE]', separator='[COMMA]'):
    self.block_start = block_start
    self.block_end = block_end
    self.separator = separator

  def sentencize(self, tokens: list[Token]) -> list[Sentence]:
    sentences: list[Sentence] = []
    start = None
    last = Sentence(None, 0,0)
    for index, token in enumerate(tokens):
        if token.type == self.block_start and start is None:
            start = index+1
        elif token.type == self.block_end and start is not None:
            last = Sentence("BLOCK", start, index)
            start = None
            sentences.append(last)
        elif token.type == self.separator and start is None:
            last = Sentence("SENTENCE", last.end, index+1)
            sentences.append(last)
    if last.end < len(tokens)-1:
        last = Sentence("SENTENCE", last.end, len(tokens))
        sentences.append(last)
    ret: list[Sentence] = []
    for s in sentences:
        if tokens[s.end-1].type == self.separator:
            ret.append(Sentence(s.type, s.start, s.end-1))
        else:
            ret.append(s)
    return ret
from tokenizer.basic_tokenizer import BasicTokenizer


# JavaScript and TypeScript keywords
js_keywords = ("break", "case","catch","class","const","continue","debugger",
               "default","delete","do","else","export","extends","false",
               "finally","for","function","if","import","in","instanceof",
               "new","null","return","super","switch","this","throw",
               "true","try","typeof","var","void","while","with","yield")
ts_keywords = js_keywords + \
            ("any","as","asserts","async","await","boolean","constructor",
              "declare","enum","from","get","implements","infer","interface",
              "is","keyof","let","module","namespace","never","readonly",
              "require","number","object","of","package","private","protected",
              "public","set","static","string","symbol","type","undefined",
              "unique","unknown","void")

class TypeScriptTokenizer(BasicTokenizer):
    """A simple regex-based tokenizer for TypeScript."""
    def __init__(self):
        super().__init__(keywords=ts_keywords)
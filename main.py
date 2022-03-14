# Parsing toolkit for Python
from lark import Lark

with open("grammar.lark") as grammar:
    grammar = grammar.read()

with open("test/document.txt") as source_text:
    source_text = source_text.read()

# Earley parser is an algorithm for parsing strings that belong to a given context-free language
parser = Lark(grammar, parser='earley', maybe_placeholders=False)
tree = parser.parse(source_text)

print(tree.pretty())
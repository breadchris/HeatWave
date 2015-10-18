#!/usr/bin/env python3
c_types = ['char', 'short', 'int', 'long']

class Node(object):
    possible_children = []
    """ Not actually instantiable, but used as a base so possible children can match on it for "anything goes" """
    pass

class Literal(Node):
    possible_children = [(str, int)
                        ]
    def __init__(self, value):
        self.value = value
    def dump(self):
        return repr(self.value).replace("'", '"')

class Variable(Node):
    possible_children = [(str)
                        ]
    def __init__(self, name):
        self.name = name
    def dump(self):
        return self.name

class Decl(Node):
    possible_children = [(Variable),
                         (Variable, Literal, None)
                        ]
    def __init__(self, typ, name, value=None):
        self.typ = typ
        self.name = name
        self.value = value
    def dump(self):
        return self.typ + ' ' + self.name.dump() + (' = ' + self.value.dump() if self.value else '')

class Block(Node):
    possible_children = [(Node),
                         ...
                        ]
    def __init__(self, elements=None):
        self.elements = elements if elements else []
    def dump(self):
        return '{\n' + ';\n'.join([x.dump() for x in self.elements]) + ';\n}\n'

class IfStmt(Node):
    possible_children = [(Literal, Variable),
                         (Node),
                         (Node, None)
                        ]
    def __init__(self, condition, true_part, false_part=None):
        self.condition = condition
        self.true_part = true_part
        self.false_part = false_part
    def dump(self):
        return "if (" + self.condition.dump() + ")\n" + self.true_part.dump() + (' else ' + self.false_part.dump() if self.false_part else '') 


if __name__ == '__main__':
    prologue = "int main() {"
    epilogue = "return 0;}"
    print(prologue + Block([Decl('int', Variable('x'), Literal(1)), Literal("234"), IfStmt(Literal(1), Block([Literal("asdf"), Literal("fsad")]), Literal('1'))]).dump() + epilogue)

#!/usr/bin/env python3
import sys
sys.setrecursionlimit(2**16)
c_types = ['char', 'short', 'int', 'long']


class Node(object):
    possible_children = []
    """ Not actually instantiable, but used as a base so possible children can match on it for "anything goes" """
    pass

class TypeName(Node):
    possible_children = [(str,)]
    def __init__(self, typ):
        self.typ = random.choice(c_types)
    def dump(self):
        return str(self.typ)

class Literal(Node):
    possible_children = [(int,)
                        ]
    def __init__(self, value):
        self.value = value
    def dump(self):
        return repr(self.value).replace("'", '"')

class Variable(Node):
    possible_children = [(str,)
                        ]
    def __init__(self, name):
        self.name = name
    def dump(self):
        return self.name

class Decl(Node):
    possible_children = [(TypeName,),
                         (Variable,),
                         (Literal, None)
                        ]
    def __init__(self, typ, name, value=None):
        self.typ = typ
        self.name = name
        self.value = value
    def dump(self):
        return self.typ.dump() + ' ' + self.name.dump() + (' = ' + self.value.dump() if self.value else '')

class Block(Node):
    possible_children = [(...,),
                         ...
                        ]
    def __init__(self, *elements):
        self.elements = elements if elements else []
    def dump(self):
        return '{\n' + ';\n'.join([x.dump() for x in self.elements]) + ';\n}\n'

class IfStmt(Node):
    possible_children = [(Literal,),
                         (Block, Literal,),
                        ]
    def __init__(self, condition, true_part, false_part=None):
        self.condition = condition
        self.true_part = true_part
        self.false_part = false_part
    def dump(self):
        return "if (rand())\n" + self.true_part.dump() + ('; else ' + self.false_part.dump() + '' if self.false_part else ';') 

import random

def generate_thing():
    kinds = Node.__subclasses__()
    node_cl = random.choice(kinds)
    print(node_cl)
    print(node_cl.possible_children)

def generate_children_for(node_cl, remaining_depth=3):
    if remaining_depth == 0:
        return Variable("printf(\"lolhitrecursionlimit\\n\")")
    possible = node_cl.possible_children
    variadic = possible[-1] == ...
    choices = []
    if variadic:
        if possible[0][0] == ...:
            choices = [random.choice([IfStmt, Literal])]
            ext_choices = list(map(random.choice, [[IfStmt, Literal]] * random.randint(0, 100)))
        else:
            choices = list(map(random.choice, possible[:-1]))
            ext_choices = list(map(random.choice, [possible[-2]] * random.randint(0, 100)))
        choices += ext_choices
    else:
        choices = list(map(random.choice, possible))
    def initialize_node(node):
        if node:
            if issubclass(node, Node):
                return generate_children_for(node, remaining_depth-1)
            else:
                if node is str:
                    return ''.join(map(random.choice, ["abcdefghijklmonp"]*3))
                elif node is int:
                    return 1
                else:
                    print("WTF %r isn't a type I know about!?!?"%node)
        else:
            return None
    children = list(map(initialize_node, choices))
    return node_cl(*children)
    


if __name__ == '__main__':
    prologue = "#include <stdio.h>\nint main() {"
    epilogue = "return 0;}"
    print(prologue + generate_children_for(Block).dump() + epilogue)
    #print(prologue + Block([Decl('int', Variable('x'), Literal(1)), Literal("234"), IfStmt(Literal(1), Block([Literal("asdf"), Literal("fsad")]), Literal('1'))]).dump() + epilogue)

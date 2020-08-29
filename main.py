class Tree(object):
    def __init__(self):
        self.children = None
        self.data = None


tokens = []
c = 0
Token = None


def get_tokens():
    global tokens
    return tokens


def set_tokens(to):
    global tokens
    global c
    tokens = to
    c = 0


def getToken():
    global Token
    global c
    if c < len(tokens)-1:
        Token = tokens[c+1]
    c += 1


def match(expectedToken):
    if expectedToken == Token[1]:
        getToken()
    else:
        raise Exception(f"Error matching token {c} [{Token[0]}]\nExpected {expectedToken}")


def program():
    global Token
    global tokens
    Token = tokens[c]
    return stmt_sequence()


def stmt_sequence():
    statements = [statement()]

    while Token[1] == 'SEMICOLON':
        match('SEMICOLON')
        statements.append(statement())

    return statements


def statement():
    if Token[1] == 'IF':
        return if_stmt()
    elif Token[1] == 'IDENTIFIER':
        return assign_stmt()
    elif Token[1] == 'READ':
        return read_stmt()
    elif Token[1] == 'WRITE':
        return write_stmt()
    elif Token[1] == 'REPEAT':
        return repeat_stmt()
    else:
        raise Exception(f"Error in statement sequence at token {c}: {Token}")


def if_stmt():
    node = Tree()
    node.data = 'IF'
    match('IF')

    left = exp()
    match('THEN')

    right = stmt_sequence()

    if Token[1] == 'END':
        match('END')
        node.children = [left, right]

    elif Token[1] == 'ELSE':
        match('ELSE')
        else_node = stmt_sequence()
        node.children = [left, right, else_node]
        match('END')

    else:
        raise Exception(f"Error in if statement at token {c}: {Token}")
    return node


def repeat_stmt():
    match('REPEAT')
    left = stmt_sequence()
    match('UNTIL')
    right = exp()

    node = Tree()
    node.data = 'REPEAT'
    node.children = [left, right]

    return node


def assign_stmt():
    node = Tree()
    node.data = 'ASSIGN\n' + str(Token[0])
    match('IDENTIFIER')
    match('ASSIGN')
    node.children = [exp()]
    return node


def read_stmt():
    match('READ')
    temp = Tree()
    temp.data = f'READ\n{exp().data[3:]}'
    return temp


def write_stmt():
    match('WRITE')
    temp = Tree()
    temp.data = ' WRITE'
    temp.children = [exp()]
    return temp


def exp():
    temp = simple_exp()
    left = temp

    while Token[0] == '<' or Token[0] == '=':
        op = Tree()
        op.data = f"op\n({Token[0]})"
        if Token[0] == '<':
            match('LESSTHAN')
        else:
            match('EQUAL')

        x = simple_exp()
        right = x

        op.children = [left, right]
        left = op

    return left


def simple_exp():
    temp = term()
    left = temp

    while Token[0] == '+' or Token[0] == '-':
        op = Tree()
        op.data = f"op\n({Token[0]})"
        if Token[0] == '+':
            match('PLUS')
        else:
            match('MINUS')

        x = term()
        right = x

        op.children = [left, right]
        left = op

    return left


def term():
    temp = factor()

    left = temp

    while Token[0] == '*' or Token[0] == '/':
        op = Tree()
        op.data = f"op\n({Token[0]})"
        if Token[0] == '*':
            match('MULT')
        else:
            match('DIV')

        x = factor()
        right = x

        op.children = [left, right]
        left = op

    return left


def factor():
    if Token[0] == '(':
        match('OPENBRACKET')
        temp = simple_exp()
        match('CLOSEDBRACKET')
    elif Token[1] == "NUMBER":
        temp = Tree()
        temp.data = f"const\n({Token[0]})"
        match(Token[1])
    else:
        temp = Tree()
        temp.data = f"id\n({Token[0]})"
        match('IDENTIFIER')

    return temp

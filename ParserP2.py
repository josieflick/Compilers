class DeclarationListNode:
    def __init__(self, declaration, declarationList=None):
        self.declaration = declaration
        self.declarationList = declarationList

    def analyze(self):
        self.declaration.analyze()
        if self.declarationList is not None:
            self.declarationList.analyze()


last_decl_main = False


class ProgramNode:
    def __init__(self, declarationList):
        self.declarationList = declarationList

    def analyze(self):
        self.declarationList.analyze()
        if not last_decl_main:
            raise Exception()


class DeclarationNode:
    def __init__(self, funDeclaration, varDeclaration=None):
        self.funDeclaration = funDeclaration
        self.varDeclaration = varDeclaration

    def analyze(self):
        if self.funDeclaration is not None:
            self.funDeclaration.analyze()
        if self.varDeclaration is not None:
            self.varDeclaration.analyze()
            global last_decl_main
            last_decl_main = False


# vartab = [{}] #variables in compoundstate

class varTab:
    variables = [[]]

    def __init__(self):
        pass

    def append(self, type, ID, array):
        group = [type, ID, array]
        if ID in [group[1] for group in self.variables[-1]]:  # pulling out all the IDs out of variables
            raise Exception()
        self.variables[-1].append(group)

    def push_scope(self):
        self.variables.append([])

    def pop_scope(self):
        self.variables.pop()

    def search(self, ID):
        for scope in reversed(self.variables):
            for group in scope:
                if ID == group[1]:
                    return group
        raise Exception()


vtab = varTab()


class funcTab:
    variables = []

    def __init__(self):
        pass

    def append(self, type, ID, params):
        group = [type, ID, params]
        if ID in [group[1] for group in self.variables]:
            raise Exception()
        self.variables.append(group)


    def search(self, ID):
        for group in self.variables:
            if ID == group[1]:
                return group
        raise Exception()


ftab = funcTab()


class VarDeclartionNode:
    def __init__(self, type, ID, num=None):
        self.type = type
        self.ID = ID
        self.num = num

    def analyze(self):
        if self.type[1] == "void":
            raise Exception()
        vtab.append(self.type[1], self.ID[1], self.num is not None)


class ReturnTypeHolder:
    def __init__(self, type):
        self.type = type
        self.hit = type == "void"


ret = ReturnTypeHolder("void")


class FunDeclarationNode:
    def __init__(self, type, ID, params, compoundState):
        self.type = type
        self.ID = ID
        self.params = params
        self.compoundState = compoundState

    def analyze(self):
        global ret
        ret = ReturnTypeHolder(self.type[1])
        ftab.append(self.type[1], self.ID[1], self.params)

        vtab.push_scope()
        self.params.analyze()
        self.compoundState.analyze(False)
        vtab.pop_scope()

        if not ret.hit:
            raise Exception()
        global last_decl_main
        last_decl_main = self.type[1] == "void" and self.ID[1] == "main" and self.params.paramList is None


class ParamsNode:
    def __init__(self, paramList=None):
        self.paramList = paramList

    def analyze(self):
        if self.paramList is not None:
            self.paramList.analyze()


class ParamListNode:
    def __init__(self, param, paramList=None):
        self.param = param
        self.paramList = paramList

    def analyze(self):
        self.param.analyze()
        if self.paramList is not None:
            self.paramList.analyze()


# CHECK FOR CORRECTION

class ParamNode:
    def __init__(self, type, ID, arr=False):
        self.type = type
        self.ID = ID
        self.arr = arr

    def analyze(self):
        if self.type[1] == "void":
            raise Exception()
        vtab.append(self.type[1], self.ID[1], self.arr)


class CompState:
    def __init__(self, localDeclaration, stateList):
        self.localDeclaration = localDeclaration
        self.stateList = stateList

    def analyze(self, pushscope=True):
        if pushscope:
            vtab.push_scope()
        self.localDeclaration.analyze()
        self.stateList.analyze()
        if pushscope:
            vtab.pop_scope()


class LocalDeclaration:
    def __init__(self, varDeclaration=None, localDeclaration=None):
        self.varDeclaration = varDeclaration
        self.localDeclaration = localDeclaration

    def analyze(self):
        if self.varDeclaration is not None:
            self.varDeclaration.analyze()
        if self.localDeclaration is not None:
            self.localDeclaration.analyze()


class StateList:
    def __init__(self, statement=None, statementList=None):  # DOES THIS NEED TO BE =NONE
        self.statement = statement
        self.statementList = statementList

    def analyze(self):
        if self.statement is not None:
            self.statement.analyze()
        if self.statementList is not None:
            self.statementList.analyze()


class Statement:
    def __init__(self, expressionState, compoundState, selectionState, iterationState, returnState):
        self.expressionState = expressionState
        self.compundState = compoundState
        self.selectionState = selectionState
        self.iterationState = iterationState
        self.returnState = returnState

    def analyze(self):
        if self.expressionState is not None:
            self.expressionState.analyze()
        if self.compundState is not None:
            self.compundState.analyze()
        if self.selectionState is not None:
            self.selectionState.analyze()
        if self.iterationState is not None:
            self.iterationState.analyze()
        if self.returnState is not None:
            self.returnState.analyze()


class ExpressionState:
    def __init__(self, expression=None):
        self.expression = expression

    def analyze(self):
        if self.expression is not None:
            self.expression.analyze()


class SelectionState:
    def __init__(self, expr, ifStatement, elseStatement=None):
        self.expr = expr
        self.elseStatement = elseStatement
        self.ifStatement = ifStatement

    def analyze(self):
        t = self.expr.analyze()
        if t != ["int", False]:
            raise Exception()
        self.ifStatement.analyze()
        if self.elseStatement is not None:
            self.elseStatement.analyze()


class IterationState:
    def __init__(self, expr, whileStatement):
        self.expr = expr
        self.whileStatement = whileStatement

    def analyze(self):
        x = self.expr.analyze()
        if x != ["int", False]:
            raise Exception()
        self.whileStatement.analyze()


class ReturnState:
    def __init__(self, returnExpression=None):
        self.returnExpression = returnExpression

    def analyze(self):
        if self.returnExpression is None and ret.type != "void":
            raise Exception()
        if self.returnExpression is not None:
            t = self.returnExpression.analyze()
            if t != [ret.type, False]:
                raise Exception()
            ret.hit = True


class Expression:
    def __init__(self, var, expr, simpleExpression=None):
        self.var = var
        self.expr = expr
        self.simpleExpression = simpleExpression

    def analyze(self):
        if self.var is not None:
            a = self.var.analyze()
            b = self.expr.analyze()
            if a != b:
                raise Exception()
            if a[1]:
                raise Exception()
            return a
        if self.simpleExpression is not None:
            return self.simpleExpression.analyze()


class Var:
    def __init__(self, ID, expression=None):
        self.ID = ID
        self.expression = expression

    # expression[2+2}
    def analyze(self):
        group = vtab.search(self.ID[1])
        if self.expression is None:
            return [group[0], group[2]]
        else:
            if not group[2]:
                raise Exception()
            t = self.expression.analyze()
            if t != ["int", False]:
                raise Exception()
            return t


class SimpleExpression:  # x!=y or x>y or x<y or x==y ...
    def __init__(self, lhs, relop=None, rhs=None):
        self.lhs = lhs
        self.relop = relop
        self.rhs = rhs

    def analyze(self):
        if self.rhs is not None:
            a = self.lhs.analyze()
            b = self.rhs.analyze()
            if a != b:
                raise Exception()
            if a[1]:  # if a is an array
                raise Exception()
            if a[0] == "void":
                raise Exception()
            return ["int", False]
        else:
            return self.lhs.analyze()


class AdditiveExpression:
    def __init__(self, lhs, addop=None, rhs=None):
        self.lhs = lhs
        self.addop = addop
        self.rhs = rhs

    def analyze(self):
        if self.rhs is not None:
            a = self.lhs.analyze()
            b = self.rhs.analyze()
            if a != b:
                raise Exception()
            if a[1]:  # if a is an array
                raise Exception()
            if a[0] == "void":
                raise Exception()
            return a
        else:
            return self.lhs.analyze()


class Term:  # x*y / x/y
    def __init__(self, factor, mulop=None, term=None):
        self.factor = factor
        self.mulop = mulop
        self.term = term

    def analyze(self):
        if self.term is not None:
            a = self.factor.analyze()
            b = self.term.analyze()
            if a != b:
                raise Exception()
            if a[1]:  # if a is an array
                raise Exception()
            if a[0] == "void":
                raise Exception()
            return a
        else:
            return self.factor.analyze()


class Factor:
    def __init__(self, expression, var, call, number):
        self.expression = expression
        self.var = var
        self.call = call
        self.number = number

    def analyze(self):
        if self.expression is not None:
            return self.expression.analyze()
        if self.var is not None:
            return self.var.analyze()
        if self.call is not None:
            return self.call.analyze()
        if self.number is not None:
            return ["int", False]


class Call:
    def __init__(self, ID, args):
        self.ID = ID
        self.args = args

    def analyze(self):
        func = ftab.search(self.ID[1])
        type = func[0]
        params = func[2]
        if params.paramList is None:
            if self.args.argsList is not None:
                raise Exception()
            else:
                return [type, False]
        elif self.args.argsList is None:
            raise Exception()

        def analyze_rec(param_list, arg_list):
            if param_list.paramList is None:
                if arg_list.argList is not None:
                    raise Exception()
                else:
                    return
            elif arg_list.argList is None:
                raise Exception()
            ptype = [param_list.param.type[1], param_list.param.arr]
            atype = arg_list.expression.analyze()
            if ptype != atype:
                raise Exception()
            analyze_rec(param_list.paramList, arg_list.argList)

        analyze_rec(params.paramList, self.args.argsList)

        return [type, False]


class Args:
    def __init__(self, argsList=None):
        self.argsList = argsList


class ArgList:
    def __init__(self, expression, argList=None):
        self.expression = expression
        self.argList = argList


lexmemes = [
    ("TYPE", "int"),
    ("ID", "main"),
    ("(", "("),
    ("TYPE", "void"),
    (")", ")"),
    ("{", "{"),
    ("}", "}"),
    ("[", "["),
    ("]", "]"),
    (";", ";"),
    (",", ","),
    ("RELOP", ">="),
    ("KEYWORD", "else"),
    ("KEYWORD", "if"),
    ("KEYWORD", "return"),
    ("KEYWORD", "while"),
    ("RELOP", ">="),
    ("RELOP", ">"),
    ("RELOP", "<="),
    ("RELOP", "=="),
    ("RELOP", "!="),
    ("ADDOP", r"\+|-"),
    ("MULOP", "*"),
    ("MULOP", "/"),
    ("NUM", r"[0-9]+"),
    ("ID", r"[a-zA-Z]+"),
]

index = 0


def current_lexmeme():
    global index
    return lexmemes[index]


def next_lexmeme():
    return lexmemes[index + 1] if index < len(lexmemes) - 1 else ("", "")


def accept_lexmeme():
    global index
    index += 1


def out_of_tokens():
    if index == len(lexmemes):
        return True
    else:
        return False


def program(lm2):
    global lexmemes
    lexmemes = lm2
    dec = declaration_list()
    if index < len(lexmemes):
        raise Exception()
    return ProgramNode(dec)


def declaration_list():
    global index
    dec = declaration()
    indexOld = index
    try:
        dec1 = declaration_list()
        return DeclarationListNode(dec, dec1)
    except:
        index = indexOld
        return DeclarationListNode(dec)


def declaration():
    global index
    index_old = index
    try:
        dec = var_declaration()
        return DeclarationNode(None, dec)
    except:
        index = index_old
        dec1 = fun_declaration()
        return DeclarationNode(dec1)


def var_declaration():
    global index
    indexOld = index
    if current_lexmeme()[0] != "TYPE":
        raise Exception()
    t = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[0] != "ID":
        raise Exception()
    i = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[1] == ";":
        accept_lexmeme()
        return VarDeclartionNode(t, i)
    elif current_lexmeme()[1] == "[":
        accept_lexmeme()
        if current_lexmeme()[0] != "INT":
            raise Exception()
        z = current_lexmeme()
        accept_lexmeme()
        if current_lexmeme()[1] != "]":
            raise Exception()
        accept_lexmeme()
        if current_lexmeme()[1] != ";":
            raise Exception()
        accept_lexmeme()
        return VarDeclartionNode(t, i, z)
    else:
        raise Exception()


def fun_declaration():
    global index
    indexOld = index
    if current_lexmeme()[0] != "TYPE":
        raise Exception()
    x = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[0] != "ID":
        raise Exception()
    y = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[1] != "(":
        raise Exception()
    accept_lexmeme()
    z = params()
    if current_lexmeme()[1] != ")":
        raise Exception()
    accept_lexmeme()
    w = compoundStmt()
    return FunDeclarationNode(x, y, z, w)


def params():
    global index
    indexOld = index
    if current_lexmeme()[1] == "void" and next_lexmeme()[1] == ")":
        accept_lexmeme()
        return ParamsNode()
    else:
        index = indexOld
        y = paramList()
        return ParamsNode(y)


def paramList():
    global index
    x = param()
    if current_lexmeme()[1] == ",":
        accept_lexmeme()
        y = paramList()
        return ParamListNode(x, y)
    else:
        return ParamListNode(x)


def param():
    global index
    indexOld = index

    if current_lexmeme()[0] != "TYPE":
        raise Exception()
    x = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[0] != "ID":
        raise Exception()
    y = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[1] == "[":
        accept_lexmeme()
        if current_lexmeme()[1] != "]":
            raise Exception()
        accept_lexmeme()
        return ParamNode(x, y, True)
    else:
        return ParamNode(x, y)


def compoundStmt():
    global index
    # indexOld = index
    if current_lexmeme()[1] != "{":
        raise Exception()
    accept_lexmeme()
    x = localDeclarations()
    y = statementList()
    if current_lexmeme()[1] != "}":
        raise Exception()
    accept_lexmeme()
    return CompState(x, y)


def localDeclarations():
    try:
        x = var_declaration()
        y = localDeclarations()
        return LocalDeclaration(x, y)
    except:
        return LocalDeclaration()


def statementList():
    global index
    indexold = index
    try:
        x = statement()
        if indexold == index:
            return StateList()
        y = statementList()
        return StateList(x, y)
    except:
        index = indexold
        return StateList()


# CHECK FOR CORRECTIOn
def statement():
    global index
    indexOld = index
    try:
        x = expressionState()
        return Statement(x, None, None, None, None)
    except:
        index = indexOld
        try:
            x = compoundStmt()
            return Statement(None, x, None, None, None)
        except:
            index = indexOld
            try:
                index = indexOld
                x = selectionState()
                return Statement(None, None, x, None, None)
            except:
                index = indexOld
                try:
                    x = iterationState()
                    return Statement(None, None, None, x, None)
                except:
                    index = indexOld
                    x = returnState()
                    return Statement(None, None, None, None, x)


def expressionState():
    global index
    indexOld = index
    if current_lexmeme()[1] == ";":
        accept_lexmeme()
        return ExpressionState()
    else:
        x = expression()
        if current_lexmeme()[1] != ";":
            raise Exception()
        accept_lexmeme()
        return ExpressionState(x)


def selectionState():
    global index
    # indexOld = index
    if current_lexmeme()[1] != "if":
        raise Exception()
    accept_lexmeme()
    if current_lexmeme()[1] != "(":
        raise Exception()
    accept_lexmeme()
    x = expression()
    if current_lexmeme()[1] != ")":
        raise Exception()
    accept_lexmeme()
    y = statement()
    if current_lexmeme()[1] != "else":
        return SelectionState(x, y)
    accept_lexmeme()
    z = statement()
    return SelectionState(x, y, z)


def iterationState():
    global index
    # indexOld = index
    if current_lexmeme()[1] != "while":
        raise Exception()
    accept_lexmeme()
    if current_lexmeme()[1] != "(":
        raise Exception()
    accept_lexmeme()
    x = expression()
    if current_lexmeme()[1] != ")":
        raise Exception()
    accept_lexmeme()
    y = statement()
    return IterationState(x, y)


def returnState():
    global index
    if current_lexmeme()[1] != "return":
        raise Exception()
    accept_lexmeme()
    if current_lexmeme()[1] == ";":
        accept_lexmeme()
        return ReturnState()
    else:
        x = expression()
        if current_lexmeme()[1] != ";":
            raise Exception()
        accept_lexmeme()
        return ReturnState(x)


def expression():
    global index
    oldIndex = index
    try:
        x = var()
        if current_lexmeme()[1] != "=":
            raise Exception()
        accept_lexmeme()
        y = expression()
        return Expression(x, y)
    except:
        index = oldIndex
        x = simpleExpression()
        return Expression(None, None, x)


def var():
    global index
    if current_lexmeme()[0] != "ID":
        raise Exception()
    x = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[1] != "[":
        return Var(x)
    accept_lexmeme()
    y = expression()
    if current_lexmeme()[1] != "]":
        raise Exception
    accept_lexmeme()
    return Var(x, y)


def simpleExpression():
    global index
    x = additiveExpression()
    if current_lexmeme()[0] == "RELOP":
        y = current_lexmeme()
        accept_lexmeme()
        z = additiveExpression()
        return SimpleExpression(x, y, z)
    else:
        return SimpleExpression(x)


def additiveExpression():
    global index
    x = term()
    if current_lexmeme()[0] == "ADDOP":
        y = current_lexmeme()
        accept_lexmeme()
        z = additiveExpression()
        return AdditiveExpression(x, y, z)
    else:
        return AdditiveExpression(x)


def term():
    global index
    x = factor()
    if current_lexmeme()[0] == "MULOP":
        y = current_lexmeme()
        accept_lexmeme()
        z = term()
        return Term(x, y, z)
    else:
        return Term(x)


def factor():
    global index
    oldIndex = index
    try:
        if current_lexmeme()[1] != "(":
            raise Exception()
        accept_lexmeme()
        x = expression()
        if current_lexmeme()[1] != ")":
            raise Exception()
        accept_lexmeme()
        return Factor(x, None, None, None)
    except:
        try:
            index = oldIndex
            x = call()
            return Factor(None, None, x, None)
        except:
            try:
                index = oldIndex
                x = var()
                return Factor(None, x, None, None)
            except:
                index = oldIndex
                x = current_lexmeme()
                if current_lexmeme()[0] == "INT":
                    accept_lexmeme()
                else:
                    raise Exception()
                return Factor(None, None, None, x)


def call():
    global index
    indexOld = index
    if current_lexmeme()[0] != "ID":
        raise Exception()
    x = current_lexmeme()
    accept_lexmeme()
    if current_lexmeme()[1] != "(":
        raise Exception()
    accept_lexmeme()
    y = args()
    if current_lexmeme()[1] != ")":
        raise Exception()
    accept_lexmeme()
    return Call(x, y)


def args():
    global index
    indexOld = index
    try:
        x = argList()
        return Args(x)
    except:
        index = indexOld
        return Args()


def argList():
    global index
    index = index
    x = expression()
    if current_lexmeme()[1] == ",":
        accept_lexmeme()
        y = argList()
        return ArgList(x, y)
    else:
        return ArgList(x)

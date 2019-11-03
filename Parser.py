class ProgramNode:
    def __init__(self, declarationList):
        self.declarationList = declarationList

class DeclarationListNode:
    def __init__(self, declaration, declarationList=None):
        self.declaration = declaration
        self.declarationList = declarationList

class DeclarationNode:
    def __init__(self,funDeclaration,varDeclaration=None):
        self.funDeclaration = funDeclaration
        self.varDeclaration = varDeclaration

class VarDeclartionNode:
    def __init__(self, type, ID, num=None):
        self.type = type
        self.ID = ID
        self.num = num

class TypeSpeciferNode:
    def __init__(self, void, int=None):
        self.void = void
        self.int = int

class FunDeclarationNode:
    def __init__(self,type, ID, params, compoundState):
        self.type = type
        self.ID = ID
        self.params = params
        self.compoundState = compoundState

class ParamsNode:
    def __init__(self, paramList, void):
        self.paramList = paramList
        self.void = void

class ParamListNode:
    def __init__(self,param, paramList=None):
        self.param = param
        self.paramList = paramList

#CHECK FOR CORRECTION

class ParamNode:
    def __init__(self,type, ID):
        self.type = type
        self.ID= ID

class CompState:
    def __init__(self, localDeclaration, stateList):
        self.localDeclaration = localDeclaration
        self.stateList = stateList

class LocalDeclaration:
    def __init__(self,varDeclaration, localDeclaration, epsilon):
        self.varDeclaration = varDeclaration
        self.localDeclaration = localDeclaration


class StateList:
    def __init__(self, statement, statementList): #DOES THIS NEED TO BE =NONE
        self.statement = statement
        self.statementList = statementList

class Statement:
    def __init__(self, expressionState, compoundState, selectionState, iterationState, returnState):
        self.expressionState = expressionState
        self.compundState = compoundState
        self.selectionState = selectionState
        self.interationState = iterationState
        self.returnState = returnState

class ExpressionState:
    def __init__(self,;SYMBOL,expression=None):
        self.;SYMBOL = symbol
        self.expression = expression

class SelectionState:
    def __init__(self, elseStatement, ifStatement = None):
        self.elseStatement = elseStatement
        self.ifStatement = ifStatement

class IterationState:
    def __init__(self, whileStatement):
        self.whileStatement = whileStatement
#WHAT DO I DO WITH THE ;
class ReturnState:
    def __init__(self, returnExpression, ):
        self.returnExpression = returnExpression

class Expression:
    def __init__(self, varExpression, simpleExpression):
        self.varExpression = varExpression
        self.simpleExpression = simpleExpression

class Var:
    def __init__(self, ID, expression):
        self.ID = ID
        self.expression = expression

class SimpleExpression:
    def __init__(self, additiveExpression, additiveExpressionRelop = None ):
        self.additiveExpression = additiveExpression
        self.additiveExpressionRelop = additiveExpressionRelop

class Relop:
    def __init__(self, Symbol):
        self.Symbol = Symbol

class AdditiveExpression:
    def __init__(self, term, additiveExpressionAddop = None):
        self.term = term
        self.additiveExpressionAddop = additiveExpressionAddop

class Addop:
    def __init__(self, plus, minus):
        self.plus = plus
        self.minus = minus

class Term:
    def __init__(self, factor, termMulop = None):
        self.factor = factor
        self.termMulop = termMulop

class Mulop:
    def __init__(self, multiply, divide):
        self.multiply = multiply
        self.divide = divide

class Factor:
    def __init__(self, expression, var, call, number):
        self.expression = expression
        self.var = var
        self.call = call
        self.number = number

class Call:
    def __init__(self, ID):
        self.ID = ID

class Args:
    def __init__(self, argsList, #):
                 self.argsList = argsList
        self.# = #??????

class ArgList:
        def __init__(self, expression, argList = None):
            self.expression = expression
            self.argList = argList





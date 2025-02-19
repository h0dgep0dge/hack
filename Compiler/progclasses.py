from astprint import ASTPrettyPrint as ASTPrint

class AST:
    def __repr__(self):
        return ASTPrint.visit(self)
    
    def accept(self,visitor):
        return getattr(visitor,type(self).__name__)(self)

# Program Structure

class JClass(AST):
    def __init__(self,className,classVarDecList,subroutineDecList):
        self.className = className
        self.classVarDecList = classVarDecList
        self.subroutineDecList = subroutineDecList

class ClassVarDec(AST):
    def __init__(self,scope,datatype,varNameList):
        self.scope = scope
        self.datatype = datatype
        self.varNameList = varNameList

class SubroutineDec(AST):
    def __init__(self,funcType,datatype,subroutineName,parameterList,subroutineBody):
        self.funcType = funcType
        self.datatype = datatype
        self.subroutineName = subroutineName
        self.parameterList = parameterList
        self.subroutineBody = subroutineBody

class Parameter(AST):
    def __init__(self,datatype,varName):
        self.datatype = datatype
        self.varName = varName

class SubroutineBody(AST):
    def __init__(self,varDecList,statementList):
        self.varDecList = varDecList
        self.statementList = statementList

class VarDec(AST):
    def __init__(self,datatype,varNameList):
        self.datatype = datatype
        self.varNameList = varNameList

# Statements

class LetStatement(AST):
    def __init__(self,varName,expression):
        self.varName = varName
        self.expression = expression

class SubscriptLetStatement(AST):
    def __init__(self,varName,index,expression):
        self.varName = varName
        self.index = index
        self.expression = expression

class IfStatement(AST):
    def __init__(self,condition,statementList,elseStatementList):
        self.condition = condition
        self.statementList = statementList
        self.elseStatementList = elseStatementList

class WhileStatement(AST):
    def __init__(self,condition,statementList):
        self.condition = condition
        self.statementList = statementList

class ReturnStatement(AST):
    def __init__(self,expression):
        self.expression = expression

# Expressions

class LitTerm(AST):
    def __init__(self,token):
        self.token = token

class SubscriptTerm(AST):
    def __init__(self,varName,indexExpr):
        self.varName = varName
        self.indexExpr = indexExpr

class UnaryTerm(AST):
    def __init__(self,op,term):
        self.op = op
        self.term = term

class SubCall(AST):
    def __init__(self,that,name,exprList):
        self.that = that
        self.name = name
        self.exprList = exprList

class Expression(AST):
    def __init__(self,term,opterms):
        self.term = term
        self.opterms = opterms
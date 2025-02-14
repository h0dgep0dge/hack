# Program Structure

class JClass:
    def __init__(self,className,classVarDecList,subroutineDecList):
        self.className = className
        self.classVarDecList = classVarDecList
        self.subroutineDecList = subroutineDecList

class ClassVarDec:
    def __init__(self,scope,datatype,varNameList):
        self.scope = scope
        self.datatype = datatype
        self.varNameList = varNameList

class SubroutineDec:
    def __init__(self,funcType,datatype,subroutineName,parameterList,subroutineBody):
        self.funcType = funcType
        self.datatype = datatype
        self.subroutineName = subroutineName
        self.parameterList = parameterList
        self.subroutineBody = subroutineBody

class Parameter:
    def __init__(self,datatype,varName):
        self.datatype = datatype
        self.varName = varName

class SubroutineBody:
    def __init__(self,varDecList,statementList):
        self.varDecList = varDecList
        self.statementList = statementList

class VarDec:
    def __init__(self,datatype,varNameList):
        self.datatype = datatype
        self.varNameList = varNameList

# Statements

class LetStatement:
    def __init__(self,varName,expression):
        self.varName = varName
        self.expression = expression

class SubscriptLetStatement:
    def __init__(self,varName,index,expression):
        self.varName = varName
        self.index = index
        self.expression = expression

class IfStatement:
    def __init__(self,condition,statementList,elseStatementList):
        self.condition = condition
        self.statementList = statementList
        self.elseStatementList = elseStatementList

class WhileStatement:
    def __init__(self,condition,statementList):
        self.condition = condition
        self.statementList = statementList

class ReturnStatement:
    def __init__(self,expression):
        self.expression = expression

# Expressions

class LitTerm:
    def __init__(self,token):
        self.token = token
    
    def __repr__(self):
        return f"LitTerm( {repr(self.token)} )"
        return self.token.source

class Expression:
    def __init__(self,term,opterms):
        self.term = term
        self.opterms = opterms
    
    def __repr__(self):
        return f"Expression( {self.term} , {self.opterms} )"
        r = repr(self.term)
        for opterm in self.opterms:
            r += opterm[0].source + repr(opterm[1])
        return f"({r})"

class SubscriptTerm:
    def __init__(self,varName,indexExpr):
        self.varName = varName
        self.indexExpr = indexExpr
    
    def __repr__(self):
        return f"SubscriptTerm( {self.varName} , {self.indexExpr} )"

class UnaryTerm:
    def __init__(self,op,term):
        self.op = op
        self.term = term
    
    def __repr__(self):
        return f"UnaryTerm( {self.op} , {self.term} )"

class SubCall:
    def __init__(self,that,name,exprList):
        self.that = that
        self.name = name
        self.exprList = exprList
    
    def __repr__(self):
        return f"OpTerm( {self.that} , {self.name} , {self.exprList} )"
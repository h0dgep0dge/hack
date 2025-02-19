class ASTPrettyPrint:
    def visit(obj):
        return "\n"+obj.accept(ASTPrettyPrint)+"\n"
    
    def JClass(self):
        return f"JClass( {self.className} , {self.classVarDecList} , {self.subroutineDecList} )"

    def ClassVarDec(self):
        return f"ClassVarDec( {self.scope} , {self.datatype} , {self.varNameList} )"

    def SubroutineDec(self):
        return f"SubroutineDec( {self.funcType} , {self.datatype} , {self.subroutineName} , {self.parameterList} , {self.subroutineBody} )"

    def Parameter(self):
        return f"Parameter( {self.datatype} , {self.varName} )"

    def SubroutineBody(self):
        return f"SubroutineBody( {self.varDecList} , {self.statementList} )"

    def VarDec(self):
        return f"VarDec( {self.datatype} , {self.varNameList} )"

    def LetStatement(self):
        return f"LetStatement( {self.varName} , {self.expression} )"

    def SubscriptLetStatement(self):
        return f"SubscriptLetStatement( {self.varName} , {self.index} , {self.expression} )"

    def IfStatement(self):
        return f"IfStatement( {self.condition} , {self.statementList} , {self.elseStatementList} )"

    def WhileStatement(self):
        return f"WhileStatement( {self.condition} , {self.statementList} )"
        
    def ReturnStatement(self):
        return f"ReturnStatement( {self.expression} )"

    def LitTerm(self):
        return f"LitTerm( {self.token} )"
        return self.token.source

    def Expression(self):
        return f"Expression( {self.term} , {self.opterms} )"
        r = repr(self.term)
        for opterm in self.opterms:
            r += opterm[0].source + repr(opterm[1])
        return f"({r})"

    def SubscriptTerm(self):
        return f"SubscriptTerm( {self.varName} , {self.indexExpr} )"

    def UnaryTerm(self):
        return f"UnaryTerm( {self.op} , {self.term} )"

    def SubCall(self):
        return f"SubCall( {self.that} , {self.name} , {self.exprList} )"

class ASTPrintTemplate:
    def visit(obj):
        return obj.accept(ASTPrintTemplate)
    
    def JClass(self):
        self.className # identifier
        self.classVarDecList # list of ClassVarDec
        self.subroutineDecList # list of SubroutineDec

    def ClassVarDec(self):
        self.scope # static or field
        self.datatype # datatype token
        self.varNameList # list of identifiers

    def SubroutineDec(self):
        self.funcType # constr or func or meth
        self.datatype # datatype token
        self.subroutineName # identifier
        self.parameterList # list of Parameter
        self.subroutineBody # instance of SubroutineBody

    def Parameter(self):
        self.datatype # datatype token
        self.varName # identifier

    def SubroutineBody(self):
        self.varDecList # list of CarDec
        self.statementList # list of statements

    def VarDec(self):
        self.datatype # datatype token
        self.varNameList # list of ident tokens

    def LetStatement(self):
        self.varName # ident token
        self.expression # expression

    def SubscriptLetStatement(self):
        self.varName # ident token
        self.index # expression
        self.expression # expression

    def IfStatement(self):
        self.condition # expression
        self.statementList # list of statements
        self.elseStatementList # list of statements

    def WhileStatement(self):
        self.condition # expression
        self.statementList # list of statements

    def ReturnStatement(self):
        self.expression # expression

    def LitTerm(self):
        self.token # intlit or strlit

    def Expression(self):
        self.term # first term in the expression
        self.opterms # list of tuples with operators and further terms

    def SubscriptTerm(self):
        self.varName # identifier
        self.indexExpr # expression for the index

    def UnaryTerm(self):
        self.op # unary operator
        self.term # sub term

    def SubCall(self):
        self.that # name of the class being called on
        self.name # name of the function being called
        self.exprList # list of expressions
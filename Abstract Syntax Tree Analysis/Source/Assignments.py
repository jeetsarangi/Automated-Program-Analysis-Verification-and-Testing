import json
from ast import parse
from ast2json import ast2json

filename = input("Enter the Filename:")
var = ast2json(parse(open(filename).read()))
body = var["body"]

body = var["body"]

# This function takes the operator node and returns the
def getSymbol(node):
    if node["_type"] == "Add" or node["_type"] == "UAdd":
        return "+"
    if node["_type"] == "Mult":
        return "*"
    if node["_type"] == "Div":
        return "/"
    if node["_type"] == "Mod":
        return "%"
    if node["_type"] == "Sub" or node["_type"] == "USub":
        return "-"
    if node["_type"] == "FloorDiv":
        return "//"
    if node["_type"] == "LShift":
        return "<<"
    if node["_type"] == "RShift":
        return ">>"
    if node["_type"] == "BitOr":
        return "|"
    if node["_type"] == "BitXor":
        return "^"
    if node["_type"] == "BitAnd":
        return "&"
    if node["_type"] == "MatMult":
        return "@"
    if node["_type"] == "Pow":
        return "**"
    if node["_type"] == "Eq":
        return "=="
    if node["_type"] == "NotEq":
        return "!="
    if node["_type"] == "Lt":
        return "<"
    if node["_type"] == "LtE":
        return "<="
    if node["_type"] == "Gt":
        return ">"
    if node["_type"] == "GtE":
        return ">="
    if node["_type"] == "Is":
        return " is "
    if node["_type"] == "IsNot":
        return " isnot "
    if node["_type"] == "Not":
        return "not "
    if node["_type"] == "Invert":
        return "~"
    if node["_type"] == "And":
        return " and "
    if node["_type"] == "Or":
        return " or "
    if node["_type"] == "Xor":
        return "xor"
    if node["_type"] == "In":
        return " in "
    return " op "

#This is the Function that is responsible for printing the Main Body
def printBody(body):
    if len(body) <= 0:
        return
    for index in range(len(body)):
        if body[index]["_type"] == "Assign":
            st = "" + expr(body[index]["targets"][0])

            st = st + "=" + expr(body[index]["value"])
            print(st)

        if body[index]["_type"] == "For" or body[index]["_type"] == "If" or body[index]["_type"] == "While":
            printBody(body[index]["body"])
            if(body[index]["_type"] == "If"):
                printBody(body[index]["orelse"])

        if body[index]["_type"] == "AugAssign":
            st = "" + body[index]["target"]["id"]
            st = st + getSymbol(body[index]["op"]) + "=" + expr(body[index]["value"])
            print(st)


        elif body[index]["_type"] == "FunctionDef" or body[index]["_type"] == "ClassDef":

            printBody(body[index]["body"])

#This is a recursive Function that is used to find the expression and return
def expr(input):
    if input["_type"] == "Constant":
        return str(input["value"])
    if input["_type"] == "Name":
        return str(input["id"])


    if input["_type"] == "BinOp":
        left = expr(input["left"])
        right = expr(input["right"])
        operation = getSymbol(input["op"])
        return str(left)+operation+str(right)

    if input["_type"] == "Compare":
        left = expr(input["left"])
        expression = ""
        for compindex in range(len(input["comparators"])):
            expression = expression + getSymbol(input["ops"][compindex]) + expr(input["comparators"][compindex])
        return left + expression


    if input["_type"] == "UnaryOp":
        operation = getSymbol(input["op"])
        operand = expr(input["operand"])
        return operation+operand

    if input["_type"] == "List":
        res = "["
        size = len(input["elts"])
        for i in range(size):
            res = res + expr(input["elts"][i])
            if i < size - 1:
                res = res + ","
        res = res + "]"
        return res

    if input["_type"] == "Call":
        func = "" + input["func"]["id"] + "("
        numOfArguments = len(input["args"])
        for argindex in range(numOfArguments):
            arg = expr(input["args"][argindex])
            func = func + arg
            if argindex + 1 < numOfArguments:
                func += ","
        func += ")"
        return func

    if input["_type"] == "BoolOp":
        operator = getSymbol(input["op"])
        res = ""
        operands = len(input["values"])
        for i in range(operands):
            res = res+expr(input["values"][i])
            if i < operands-1:
                res = res+operator
        return res

    if input["_type"] == "Subscript":
        value = expr(input["value"])
        slice = expr(input["slice"])
        return value+"["+slice+"]"

    if input["_type"] == "Tuple":
        res = "("
        size = len(input["elts"])
        for i in range(size):
            res = res+expr(input["elts"][i])
            if i < size-1:
                res = res+","
        res = res+")"
        return res

    return "Not Known type Assigned Value"
print("Assignment Statements:")
printBody(body)

#This function will print the branch statements in the body
def printBranchConditions(body):
   for index in range(len(body)):
    if body[index]["_type"] == "If":

        testcondition = expr(body[index]["test"])
        print(testcondition)

        printBranchConditions(body[index]["body"])
        printBranchConditions(body[index]["orelse"])
    if body[index]["_type"] == "For" or body[index]["_type"] == "While":
        printBranchConditions(body[index]["body"])

    elif body[index]["_type"] == "FunctionDef" or body[index]["_type"] == "ClassDef":
        printBranchConditions(body[index]["body"])

print("\n \nBranch Conditions:")
printBranchConditions(body)

def printLoopConditions(body):
    for index in range(len(body)):
        if body[index]["_type"] == "For":
            indexvar = body[index]["target"]["id"]+" in "
            testcondition = expr(body[index]["iter"])
            print(indexvar+testcondition)
            printLoopConditions(body[index]["body"])
        elif body[index]["_type"] == "While":
            condition = expr(body[index]["test"])
            print(condition)
        elif body[index]["_type"] == "If":
            printLoopConditions(body[index]["body"])
            printLoopConditions(body[index]["orelse"])
        elif body[index]["_type"] == "FunctionDef" or body[index]["_type"] == "ClassDef":
            printLoopConditions(body[index]["body"])
print("\n \nLoop Conditions:")
printLoopConditions(body)
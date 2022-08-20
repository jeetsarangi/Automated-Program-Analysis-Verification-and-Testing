from z3 import *
import argparse
import json
import sys
# from KachuaCore.interpreter import ConcreteInterpreter
sys.path.insert(0, '../KachuaCore/')
from sExecutionInterface import *
import z3solver as zs
from irgen import *
from interpreter import *
import ast
import sExecution as se

def example(s):
    # To add symbolic variable x to solver
    s.addSymbVar('x')
    s.addSymbVar('y')
    # To add constraint in form of string
    s.addConstraint('x==5+y')
    s.addConstraint('And(x==y,x>5)')
    # s.addConstraint('Implies(x==4,y==x+8')
    # To access solvers directly use s.s.<function of z3>()
    print("constraints added till now",s.s.assertions())
    # To assign z=x+y
    s.addAssignment('z','x+y')
    # To get any variable assigned
    print("variable assignment of z =",s.getVar('z'))

def checkEq(args,ir):

    l = []
    file1 = open("../Submission/testData.json","r+")
    testData=json.loads(file1.read())
    file1.close()
    s = zs.z3Solver()
    k = zs.z3Solver()
    testData = convertTestData(testData)
    # print(testData)
    output = args.output
    # example(s)
    # TODO: write code to check equivalence
    # inputvar = args.output
    # inp = {}
    # print(args)
    # for i in inputvar:
    #     inp[":"+i] = testData["1"]["params"][i]

    # se.symbolicExecutionMain(ir,inp,{}, 100)
    # file1 = open("../Submission/testData.json","r+")
    # testData2=json.loads(file1.read())
    # file1.close()
    # # print(testData2)
    # testData2 = convertTestData(testData2)


    # # print("\n \n"+str(testData2))
    # print(testData["1"]["constraints"][0])
    # print(testData2["1"]["constraints"][0])
    # s.addSymbVar('x')
    # s.addSymbVar('y')
    # k.addSymbVar('x')
    # k.addSymbVar('y')

    # k.addConstraint('x==y')
    # k.addAssignment('x','2')
    # k.addAssignment('y','2')
    # s.addAssignment('x','4')
    # s.addAssignment('y','3')
    # s.addConstraint('x>y')
    # s.addConstraint('x <= 32')
    # s.addConstraint('x == 32')
    # s.addConstraint('x != y')
    # print(s.s.check())
    # s.s.reset()
    # print(s.s.check())

    # print(s.getVar('x'))
    # print(k.getVar('x'))

    # inptr = ConcreteInterpreter(ir)
    # inptr = ConcreteInterpreter(ir)
    # terminated = False
    # inptr.initProgramContext({"x":1,"y":1})
    # while True:
    #     terminated = inptr.interpret()
    #     if terminated:
    #             break
    # print(getattr(inptr.prg,"y"))

    # Lets First use the symbolic execution output of program 1 to make constraints after running them in program 2

    # inptr = ConcreteInterpreter(ir)
    
    for i in testData["1"]["params"].keys():
        s.addSymbVar(i)
    
    for path in testData:
        inptr = ConcreteInterpreter(ir)
        pgcon = {}
        for i in output:
            pgcon[i] = testData[path]["params"][i]
        inptr.initProgramContext(pgcon)
        while True:
            terminated = inptr.interpret()
            if terminated:
                break
        # print(getattr(inptr.prg,"y"))

        # print("aba yz".replace("uu","i"))
        
        for i in output:
            lhs = testData[path]["symbEnc"][i]
            for j in output:
                lhs = lhs.replace(j,str(pgcon[j]))
            # print(lhs)
            constrain = lhs+"=="+str(getattr(inptr.prg,i))
            l.append(constrain)
            s.addConstraint(lhs+" == "+str(getattr(inptr.prg,i)))

    # print(s.s.check())
    # print(s.s.model())


# So,in above actually i have made all constraints on the basis of executing the second program in various
# path test cases from first program in order to check all the paths of first program now to confirm that
# all the paths of second program are also covered in constraint sets the below logic is written
    se.symbolicExecutionMain(ir, {':x':5,':y':100},{}, 100)
    file1 = open("../Submission/testData.json","r+")
    testData2=json.loads(file1.read())
    file1.close()
    testData2 = convertTestData(testData2)


    for path in testData2:
        for i in testData2[path]["params"]:
            # cont = i+"=="+str(testData2[path]["params"][i])
            # k.addConstraint('x==y')
            k.addAssignment(i,testData2[path]["params"][i])

        for path2 in testData:
            condition = testData[path2]["constraints"][0].split(",")
            # print(condition,end=" ")
            for c in condition:
                # print(c.strip(),end="")
                k.addConstraint(c.strip())
            
            if str(k.s.check()) == "sat":
                for i in output:
                    s.addConstraint(testData2[path]["symbEnc"][i]+" == "+testData[path2]["symbEnc"][i])
                l.append(testData2[path]["symbEnc"][i]+" == "+testData[path2]["symbEnc"][i])
            
            k.s.reset()
            

    print("--------------------------------------------------")
    if str(s.s.check()) == "sat":
        print("The Constants values are :")
        print(s.s.model())
    else:
        print("Program constraints are non Satisfiable .Hence, the programs cannot be matched")
    # print(l)
    
    
        



    













if __name__ == '__main__':
    cmdparser = argparse.ArgumentParser(
        description='symbSubmission for assignment Program Synthesis using Symbolic Execution')
    cmdparser.add_argument('progfl')
    cmdparser.add_argument(
        '-b', '--bin', action='store_true', help='load binary IR')
    cmdparser.add_argument(
        '-e', '--output', default=list(), type=ast.literal_eval,
                               help="pass variables to kachua program in python dictionary format")
    args = cmdparser.parse_args()
    ir = loadIR(args.progfl)
    checkEq(args,ir)
    exit()

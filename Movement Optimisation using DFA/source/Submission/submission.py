
from irgen import pretty_print
from irgen import removeInstruction
import sys
sys.path.insert(0, "KachuaCore/interfaces/")
from interfaces.fuzzerInterface import *
from kast import kachuaAST
import irgen

# make sure dot or xdot works and grapviz is installed.

# Uncomment for Assignment-2
# sys.path.append("KachuaCore/kast")
# import kast.kachuaAST
# import graphviz

class CustomCoverageMetric(CoverageMetricBase):
    # Statements covered is used for 
    # coverage information.
    def __init__(self):
        super().__init__()

    # TODO : Implement this
    def compareCoverage(self, curr_metric, total_metric):
        # must compare curr_metric and total_metric
        # True if Improved Coverage else False
        return False

class CustomMutator(MutatorBase):
    def __init__(self):
        pass

    # TODO : Implement this
    def mutate(self, input_data):
        # Mutate the input data and return it
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.
        return input_data

# Reuse code and imports from 
# earlier submissions (if any).
def genCFG(ir):
    # your code here
    cfg = None
    # print(type(ir[0][0].rexpr))
    # k = kachuaAST.ConditionCommand("Injsan")
    # print(type(k))
    # return cfg




def dumpCFG(cfg):
    # dump CFG to a dot file
    
    pass

def optimize(ir):
    noofinstructions = len(ir)
    # irgen.addInstruction(ir, kachuaAST.AssignmentCommand(kachuaAST.Var(":vara"), kachuaAST.Num(5)), 11)
    # print(ir[10][0])
    INOUT = []
    for i in range(noofinstructions+1):
        INOUT.append([False,False])
    
    genkilllist = creategenkill(ir)
    
    flag = True
    count = 0
    while(flag):
        flag = False
        # count+=1
        for i in reversed(range(noofinstructions)):
            succ = getsuccesors(ir[i],i) 
            newout = True
            genkill = genkilllist[i]
            for node in succ:
                newout = newout and INOUT[node][0]
            count+=1
            newin = genkill[0] or (genkill[1] and newout)
            if newin == INOUT[i][0] and newout == INOUT[i][1]:
                flag = False
                continue

            INOUT[i][0] = newin
            INOUT[i][1] = newout
            # count+=1
    
    # irgen.pretty_print(ir)
    # irgen.removeInstruction(ir, 6)
    # irgen.addInstruction(ir, kachuaAST.AssignmentCommand(kachuaAST.Var(":vara"), kachuaAST.Num(5)), 1)
    # irgen.pretty_print(ir)
    
    it = 0
    up = updown(ir)
    right = kachuaAST.MoveCommand("k","ji")
    flag = False
    while it<len(ir):
        if (INOUT[it][1] == "True") and(type(ir[it][0]) == type(right)) and (ir[it][0].direction == "forward") and up[it] == True:
            temp = ir[it][0]
            removeInstruction(ir,it)
            INOUT.insert(it,[False,False])
            up.insert(it,False)
            if not flag:
                irgen.addInstruction(ir, kachuaAST.AssignmentCommand(kachuaAST.Var(":replaced"), temp.expr), it)
                flag = True
            else:
                irgen.addInstruction(ir,kachuaAST.MoveCommand("forward",kachuaAST.BinArithOp(kachuaAST.Var(":replaced"),temp.expr,"+")),it)

        elif (INOUT[it][1] == "False") and (type(ir[it][0]) == type(right)) and (ir[it][0].direction == "forward") and up[it]:
            temp = ir[it][0]
            removeInstruction(ir,it)
            INOUT.insert(it,[False,False])
            up.insert(it,False)
            irgen.addInstruction(ir,kachuaAST.MoveCommand("forward",kachuaAST.BinArithOp(kachuaAST.Var(":replaced"),temp.expr,"+"),it))
        it += 1

    
    return ir

def getsuccesors(line,n):
    result = []
    if line[1] == 1 :
        result.append(n+1)
    else:
        k = kachuaAST.BoolFalse()
        if type(k) == type(line[0].cond):
            result.append(line[1]+n)
        else:
            result.append(line[1]+n)
            result.append(n+1)
    return result
        
def creategenkill(ir):
    n = len(ir)
    genkill = []
    penup = kachuaAST.PenCommand("penup")
    right = kachuaAST.MoveCommand("k","ji")

    for i in range(n):
        if type(ir[i][0]) == type(penup) and ir[i][0].status == "pendown":
            genkill.append((False,False))
        
        elif type(ir[i][0]) == type(right) and (ir[i][0].direction != "forward"):
            genkill.append((False,False))
        elif type(ir[i][0]) == type(right) and (ir[i][0].direction == "forward"):
            genkill.append((True,True))
        else:
            genkill.append((False,True))

    return genkill

def updown(ir):
    up = []
    penup = kachuaAST.PenCommand("penup")
    flag = False
    for i in range(len(ir)):
        if type(ir[i][0]) == type(penup) and ir[i][0].status == "penup":
            flag = True
        elif type(ir[i][0]) == type(penup) and ir[i][0].status == "pendown":
            flag = False
        up.append(flag)
    return up


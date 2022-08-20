import random
import sys
sys.path.insert(0, "KachuaCore/interfaces/")
from interfaces.fuzzerInterface import *
# from fuzzerInterface import*
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
        for e in curr_metric:
            if e not in total_metric:
                return True
        
        return False

    # TODO : Implement this
    def updateTotalCoverage(self, curr_metric, total_metric):
        # Compute the total_metric coverage and return it (list)
        # this changes if new coverage is seen for a 
        # given input.
        for e in curr_metric:
            if e not in total_metric:
                total_metric.append(e)
        total_metric.sort()
        return total_metric

class CustomMutator(MutatorBase):
    def __init__(self):
        pass

    # TODO : Implement this
    def mutate(self, input_data, coverageInfo, irList):
        # Mutate the input data and return it
        # coverageInfo is of type CoverageMetricBase
        # Don't mutate coverageInfo
        # irList : List of IR Statments (Don't Modify)
        # input_data.data -> type dict() with {key : variable(str), value : int}
        # must return input_data after mutation.
        tempinputdict = input_data.data
        funcList = [self.add_bit,self.flip_bit,self.remove_bit,self.addsub]
        for eachkey in tempinputdict.keys():
            target = tempinputdict[eachkey]
            if str(type(target)) != "<class 'int'>":
                continue
            tempinputdict[eachkey] = random.choice(funcList)(target)
        return input_data
    
    def addsub(self,input):
        rand = random.randint(-100,100)
        return rand+input
    
    def flip_bit(self,input):
        # bit = 1<<random.randint(0,8)
        bin = "{0:b}".format(input)
        if input>=0:
            pos = random.randint(0,len(bin)-1)
        else:
            pos = random.randint(1,len(bin)-1)
        new = int(bin[pos])^1
        bin = bin[:pos]+str(new)+bin[pos+1:]
        return int(bin,2)

    def add_bit(self,input):
        bin = "{0:b}".format(input)
        if input>=0:
            pos = random.randint(0,len(bin)-1)
        else:
            pos = random.randint(1,len(bin)-1)
        bin = bin[:pos]+"1"+bin[pos:]
        return int(bin,2)

    def remove_bit(self,input):
        bin = "{0:b}".format(input)
        if input>=0:
            pos = random.randint(0,len(bin)-1)
        else:
            pos = random.randint(1,len(bin)-1)
        bin = bin[:pos]+bin[pos+1:]
        if len(bin) == 0 or bin == "-":
            bin = bin + "0"
        return int(bin,2)


    def forbool(self,input):
        return (not input)
    
    


        
    

# Reuse code and imports from 
# earlier submissions (if any).
def genCFG(ir):
    # your code here
    cfg = None
    return cfg

def dumpCFG(cfg):
    # dump CFG to a dot file
    pass

def optimize(ir):
    # create optimized ir in ir2
    ir2 = ir # currently no oprimization is enabled
    return ir2

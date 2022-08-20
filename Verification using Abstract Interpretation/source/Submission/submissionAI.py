import copy
import math
import sys
from typing import overload
import json
sys.path.insert(0, "../KachuaCore/")
import cfg.kachuaCFG as cfgK
import cfg.cfgBuilder as cfgB
from interfaces.abstractInterpretationInterface import  *
import kast.kachuaAST as kachuaAST
import abstractInterpretation as AI

'''
    Class for interval domain
'''
class Interval(abstractValueBase):

    '''Initialize abstract value'''
    def __init__(self, data = (1,0)):
        self.interval = data

    '''To display abstract values'''
    def __str__(self):
        return str(self.interval)

    '''To check whether abstract value is bot or not'''
    def isBot(self):
        if self.interval[0]>self.interval[1]:
            return True
        return False

    '''To check whether abstract value is Top or not'''
    def isTop(self):
        if self.interval[0] <= -3000 and self.interval[1]>=3000:
            return True
        return False

    '''Implement the meet operator'''
    def meet(self, other):
        
        if self.isBot() or other.isBot():
            return self.Bottom()
        
        a = self.left()
        b = self.right()
        c = other.left()
        d = other.right()
        if int(max(a,c)) > int(min(b,d)):
            return self.Bottom()
        return Interval((max(a,c),min(b,d)))
        

    '''Implement the join operator'''
    def join(self, other):
        if self.isTop() or other.isTop():
            return self.Top()
        if self.isBot():
            return other
        if other.isBot():
            return self
        return Interval((min(self.left(),other.left()),max(self.right(),other.right())))


    '''partial order with the other abstract value'''
    def __le__(self, other):
        if self.isBot() or other.isTop():
            return True
        if self.left() >= other.left() and self.right() <= other.right():
            return True
        return False


    '''equality check with other abstract value'''
    def __eq__(self, other):
        if (self.isTop() and other.isTop()) or (self.isBot() and other.isBot()):
            return True
        if self.left() == other.left() and self.right() == other.right():
            return True
        return False

    def left(self):
        return self.interval[0]
    
    def right(self):
        return self.interval[1]
    def Bottom(self):
        return Interval()
    def Top(self):
        return Interval((-4000,4000))
    def Neg(self):
        return Interval((-self.interval[0],-self.interval[1]))
    def Single(self):
        return self.interval[0] == self.interval[1]
    def neg(self):
        return Interval((-self.interval[0],-self.interval[1]))
    
    '''
        Add here required abstract transformers
    '''
    pass


class ForwardAnalysis():
    def __init__(self):
        pass

    '''
        This function is to initialize in of the basic block currBB
        Returns a dictinary {varName -> abstractValues}
        isStartNode is a flag for stating whether currBB is start basic block or not
    '''
    def initialize(self, currBB, isStartNode):
        val = {"turt_x":Interval((1,0)),"turt_y":Interval((1,0)),"turt_head":Interval((0,0))}
        #Your additional initialisation code if any
        return val

    #just a dummy equallity check function for dictionary
    def isEqual(self, dA, dB):
        for i in dA.keys():
            if i not in dB.keys():
                return False
            if dA[i] != dB[i]:
                return False
        return True

    '''
        Transfer function for basic block 'currBB' 
        args: In val for currBB, currBB
        Returns newly calculated values in a form of list
    '''
    def transferFunction(self, currBBIN, currBB):
        #implement your transfer function here
        outVal = []
        
        if currBB.name == "END":
            return [currBBIN]

        instr = currBB.instrlist[0][0]
        # print(type(instr))

        if type(instr) == kachuaAST.GotoCommand:
            currBBIN["turt_x"] = self.resolve_expr(instr.xcor,currBBIN)
            currBBIN["turt_y"] = self.resolve_expr(instr.ycor,currBBIN)
        if type(instr) == kachuaAST.AssignmentCommand:
            result = currBBIN.copy()
            l_var = instr.lvar.varname
            result[l_var] = self.resolve_expr(instr.rexpr,currBBIN)
            # print(result[l_var])
            outVal = [result]
            # print(len(outVal))
            return outVal

        elif type(instr) == kachuaAST.MoveCommand:
            
            if instr.direction == "forward":
                
                    temp_x = currBBIN["turt_x"].Bottom()
                    temp_y = currBBIN["turt_y"].Bottom()
                    left_x = currBBIN["turt_x"].left()
                    right_x = currBBIN["turt_x"].right()
                    left_y = currBBIN["turt_y"].left()
                    right_y = currBBIN["turt_y"].right()

                    sum = self.resolve_expr(instr.expr,currBBIN)
                    if sum.isBot():
                        outVal.append(currBBIN)
                    
                    else:
                        t_head = currBBIN["turt_head"]
                        for i in range(t_head.left(),t_head.right()+90,90):
                            if i == 0:
                                if currBBIN["turt_x"].isBot():
                                    temp = sum
                                elif currBBIN["turt_x"].isTop():
                                    temp = currBBIN["turt_x"].Top()
                                else:
                                    temp = Interval((left_x+sum.left(),right_x+sum.right()))
                                temp_x = temp_x.join(temp)
                            elif i == 90:
                                if currBBIN["turt_y"].isBot():
                                    temp = sum
                                elif currBBIN["turt_y"].isTop():
                                    temp = currBBIN["turt_y"].Top()
                                else:
                                    temp = Interval((left_y+sum.left(),right_y+sum.right()))
                                temp_y = temp_y.join(temp)
                            elif i == 180:
                                if currBBIN["turt_x"].isBot():
                                    temp = sum.neg()
                                elif currBBIN["turt_x"].isTop():
                                    temp = currBBIN["turt_x"].Top()
                                else:
                                    temp = Interval((left_x-sum.left(),right_x-sum.right()))
                                temp_x = temp_x.join(temp)
                            elif i == 270:
                                if currBBIN["turt_y"].isBot():
                                    temp = sum.neg()
                                elif currBBIN["turt_y"].isTop():
                                    temp = currBBIN["turt_y"].Top()
                                else:
                                    temp = Interval((left_y-sum.left(),right_y-sum.right()))
                                temp_y = temp_y.join(temp)
                        if not temp_x.isBot():
                            currBBIN["turt_x"] = temp_x
                        if not temp_y.isBot():
                            currBBIN["turt_y"] = temp_y
                        outVal.append(currBBIN)




               
            
            if instr.direction == "backward":
                
                    temp_x = currBBIN["turt_x"].Bottom()
                    temp_y = currBBIN["turt_y"].Bottom()
                    left_x = currBBIN["turt_x"].left()
                    right_x = currBBIN["turt_x"].right()
                    left_y = currBBIN["turt_y"].left()
                    right_y = currBBIN["turt_y"].right()

                    sum = self.resolve_expr(instr.expr,currBBIN)
                    if sum.isBot():
                        outVal.append(currBBIN)
                    
                    else:
                        t_head = currBBIN["turt_head"]
                        for i in range(t_head.left(),t_head.right()+90,90):
                            if i == 0:
                                if currBBIN["turt_x"].isBot():
                                    temp = sum.neg()
                                elif currBBIN["turt_x"].isTop():
                                    temp = currBBIN["turt_x"].Top()
                                else:
                                    temp = Interval((left_x-sum.left(),right_x-sum.right()))
                                temp_x = temp_x.join(temp)
                            elif i == 90:
                                if currBBIN["turt_y"].isBot():
                                    temp = sum.neg()
                                elif currBBIN["turt_y"].isTop():
                                    temp = currBBIN["turt_y"].Top()
                                else:
                                    temp = Interval((left_y-sum.left(),right_y-sum.right()))
                                temp_y = temp_y.join(temp)
                            elif i == 180:
                                if currBBIN["turt_x"].isBot():
                                    temp = sum
                                elif currBBIN["turt_x"].isTop():
                                    temp = currBBIN["turt_x"].Top()
                                else:
                                    temp = Interval((left_x+sum.left(),right_x+sum.right()))
                                temp_x = temp_x.join(temp)
                            elif i == 270:
                                if currBBIN["turt_y"].isBot():
                                    temp = sum
                                elif currBBIN["turt_y"].isTop():
                                    temp = currBBIN["turt_y"].Top()
                                else:
                                    temp = Interval((left_y+sum.left(),right_y+sum.right()))
                                temp_y = temp_y.join(temp)
                        if not temp_x.isBot():
                            currBBIN["turt_x"] = temp_x
                        if not temp_y.isBot():
                            currBBIN["turt_y"] = temp_y
                        outVal.append(currBBIN)

            if instr.direction == "right":
                old = currBBIN["turt_head"]
                temp = self.resolve_expr(instr.expr,currBBIN).left()
                one = (old.left()-temp)%360
                two = (old.right()-temp)%360
                currBBIN["turt_head"] = Interval((min(one,two),max(one,two)))
                outVal.append(currBBIN)
            
            if instr.direction == "left":
                old = currBBIN["turt_head"]
                temp = self.resolve_expr(instr.expr,currBBIN).left()
                # print(-180%360)
                one = (old.left()+temp)%360
                two = (old.right()+temp)%360
                currBBIN["turt_head"] = Interval((min(one,two),max(one,two)))
                outVal.append(currBBIN)
            

            

        

        elif type(instr)== kachuaAST.ConditionCommand:
            cond = currBB.instrlist[0][0].cond
            
            # print(type(cond))
            
            
            if type(cond) == kachuaAST.BoolFalse:
                outVal = [currBBIN,currBBIN]

            if type(cond) == kachuaAST.LT:
                lef = cond.lexpr
                rig = cond.rexpr
                if type(lef)!=kachuaAST.Var and type(rig)!= kachuaAST.Var:
                    outVal = [currBBIN,currBBIN]
                else:
                    left = self.resolve_expr(lef,currBBIN)
                    right = self.resolve_expr(rig,currBBIN)
                    result1 = currBBIN.copy()
                    result2 = currBBIN.copy()

                    if left.isBot() or right.isBot():
                        outVal.append([currBBIN,currBBIN])

                    else:
                        a = left.left()
                        b = left.right()
                        c = right.left()
                        d = right.right()

                        if a >= d:
                            if type(lef) == kachuaAST.Var:
                                result1[lef.varname] = left.Bottom()
                                result2[lef.varname] = left
                            if type(rig) == kachuaAST.Var:
                                result1[rig.varname] = right.Bottom()
                                result2[rig.varname] = right
                            
                        elif b < d:
                            if c > a:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((c,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((c,b))
                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((a,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((a+1,d))
                                    result2[rig.varname] = Interval((c,b))
                        else:
                            if c > a:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,d-1))
                                    result2[lef.varname] = Interval((c,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((c,d))

                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,d-1))
                                    result2[lef.varname] = Interval((a,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((a+1,d))
                                    result2[rig.varname] = Interval((c,d))
                    outVal = [result1,result2]

            if type(cond) == kachuaAST.LTE:
                lef = cond.lexpr
                rig = cond.rexpr
                if type(lef)!=kachuaAST.Var and type(rig)!= kachuaAST.Var:
                    outVal = [currBBIN,currBBIN]
                else:
                    left = self.resolve_expr(lef,currBBIN)
                    right = self.resolve_expr(rig,currBBIN)
                    result1 = currBBIN.copy()
                    result2 = currBBIN.copy()

                    if left.isBot() or right.isBot():
                        outVal.append([currBBIN,currBBIN])

                    else:
                        a = left.left()
                        b = left.right()
                        c = right.left()
                        d = right.right()

                        if a > d:
                            if type(lef) == kachuaAST.Var:
                                result1[lef.varname] = left.Bottom()
                                result2[lef.varname] = left
                            if type(rig) == kachuaAST.Var:
                                result1[rig.varname] = right.Bottom()
                                result2[rig.varname] = right
                            
                        elif b < d:
                            if c >= a:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((c,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((c,b))
                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((a+1,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((a+1,d))
                                    result2[rig.varname] = Interval((c,b-1))
                        else:
                            if c > a:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,d))
                                    result2[lef.varname] = Interval((c+1,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((c,d))

                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,d))
                                    result2[lef.varname] = Interval((a+1,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((a,d))
                                    result2[rig.varname] = Interval((c,d))
                    outVal = [result1,result2]

            if type(cond) == kachuaAST.GT:
                lef = cond.lexpr
                rig = cond.rexpr
                if type(lef)!=kachuaAST.Var and type(rig)!= kachuaAST.Var:
                    outVal = [currBBIN,currBBIN]
                else:
                    left = self.resolve_expr(lef,currBBIN)
                    right = self.resolve_expr(rig,currBBIN)
                    result1 = currBBIN.copy()
                    result2 = currBBIN.copy()

                    if left.isBot() or right.isBot():
                        outVal.append([currBBIN,currBBIN])

                    else:
                        a = left.left()
                        b = left.right()
                        c = right.left()
                        d = right.right()

                        if c >= b:
                            if type(lef) == kachuaAST.Var:
                                result1[lef.varname] = left.Bottom()
                                result2[lef.varname] = left
                            if type(rig) == kachuaAST.Var:
                                result1[rig.varname] = right.Bottom()
                                result2[rig.varname] = right
                            
                        elif d < b:
                            if a > c:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((a,d))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((a,d))
                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((c+1,b))
                                    result2[lef.varname] = Interval((a,d))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((c,d))
                        else:
                            if a > c:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((a,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,b-1))
                                    result2[rig.varname] = Interval((a,d))

                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((c+1,b))
                                    result2[lef.varname] = Interval((a,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,b-1))
                                    result2[rig.varname] = Interval((c,d))
                    outVal = [result1,result2]

            if type(cond) == kachuaAST.GTE:
                lef = cond.lexpr
                rig = cond.rexpr
                if type(lef)!=kachuaAST.Var and type(rig)!= kachuaAST.Var:
                    outVal.append([currBBIN,currBBIN])
                else:
                    left = self.resolve_expr(lef,currBBIN)
                    right = self.resolve_expr(rig,currBBIN)
                    result1 = currBBIN.copy()
                    result2 = currBBIN.copy()

                    if left.isBot() or right.isBot():
                        outVal = [currBBIN,currBBIN]

                    else:
                        a = left.left()
                        b = left.right()
                        c = right.left()
                        d = right.right()

                        if c > b:
                            if type(lef) == kachuaAST.Var:
                                result1[lef.varname] = left.Bottom()
                                result2[lef.varname] = left
                            if type(rig) == kachuaAST.Var:
                                result1[rig.varname] = right.Bottom()
                                result2[rig.varname] = right
                            
                        elif d <= b:
                            if a >= c:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((a,d))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((a,d))
                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((c,b))
                                    result2[lef.varname] = Interval((a,d-1))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,d))
                                    result2[rig.varname] = Interval((c+1,d))
                        else:
                            if a >= c:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((a,b))
                                    result2[lef.varname] = Interval((a,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,b))
                                    result2[rig.varname] = Interval((a+1,d))

                            else:
                                if type(lef) == kachuaAST.Var:
                                    result1[lef.varname] = Interval((c,b))
                                    result2[lef.varname] = Interval((a,b))
                                if type(rig) == kachuaAST.Var:
                                    result1[rig.varname] = Interval((c,b))
                                    result2[rig.varname] = Interval((c+1,d))
                    outVal = [result1,result2]

            if type(cond) == kachuaAST.EQ:
                lef = cond.lexpr
                rig = cond.rexpr
                if type(lef)!=kachuaAST.Var and type(rig)!= kachuaAST.Var:
                    outVal = [currBBIN,currBBIN]

                else:
                    left = self.resolve_expr(lef,currBBIN)
                    right = self.resolve_expr(rig,currBBIN)
                    result1 = currBBIN.copy()
                    result2 = currBBIN.copy()

                    if (left.isBot() and right.isBot()) or (left.isTop() and right.isTop()):
                        outVal.append([currBBIN,currBBIN])
                    else:
                        if type(lef) == kachuaAST.Var:
                            result1[lef.varname] = left.meet(right)
                        if type(rig) == kachuaAST.Var:
                            result1[rig.varname] = left.meet(right)

                        if left.Single() and right.Single() and left.left() == right.left():
                            if type(lef) == kachuaAST.Var:
                                result2[lef.varname] = left.Bottom()
                            if type(rig) == kachuaAST.Var:
                                result2[rig.varname] = right.Bottom()

                        else:
                            
                            if type(lef) == kachuaAST.Var:
                                result2[lef.varname] = left
                            if type(rig) == kachuaAST.Var:
                                result2[rig.varname] = right
                        outVal = [result1,result2]

            if type(cond) == kachuaAST.NEQ:
                lef = cond.lexpr
                rig = cond.rexpr
                if type(lef)!=kachuaAST.Var and type(rig)!= kachuaAST.Var:
                    outVal = [currBBIN,currBBIN]

                else:
                    left = self.resolve_expr(lef,currBBIN)
                    right = self.resolve_expr(rig,currBBIN)
                    result1 = currBBIN.copy()
                    result2 = currBBIN.copy()

                    if left.Single() and right.Single():
                        if left.left() == right.left():
                            if type(lef) == kachuaAST.Var:
                                result1[lef.varname] = left.Bottom()
                                result2[lef.varname] = left
                            if type(rig) == kachuaAST.Var:
                                result1[rig.varname] = left.Bottom()
                                result2[rig.varname] = right
                        else:
                            if type(lef) == kachuaAST.Var:
                                result2[lef.varname] = left.Bottom()
                                result1[lef.varname] = left
                            if type(rig) == kachuaAST.Var:
                                result2[rig.varname] = left.Bottom()
                                result1[rig.varname] = right
                    else:
                        if type(lef) == kachuaAST.Var:
                            result1[lef.varname] = left
                            result2[lef.varname] = left.meet(right)
                        if type(rig) == kachuaAST.Var:
                            result1[rig.varname] = right
                            result2[rig.varname] = right.meet(left)

                    outVal = [result1,result2]
        else:
                outVal = [currBBIN,currBBIN]
          
        return outVal

    # def cond_resolve():
   
   
   
    def resolve_expr(self,expr,bin):

        if type(expr) == kachuaAST.Num:
            return Interval((expr.val,expr.val))
        if type(expr) == kachuaAST.Var:
            if expr.varname in bin.keys():
                if bin[expr.varname].isTop():
                    return bin[expr.varname].Top()
                
                if bin[expr.varname].left() <= -3000:
                    return Interval((-3000,bin[expr.varname].right()))

                if bin[expr.varname].right() >= 3000:
                    return Interval((bin[expr.varname].left(),3000)) 

                return bin[expr.varname]
            return Interval()
        if type(expr) == kachuaAST.Sum:
            left_r = self.resolve_expr(expr.lexpr,bin)
            right_r = self.resolve_expr(expr.rexpr,bin)

            if left_r.isBot() or right_r.isBot():
                return right_r.Bottom()
            if left_r.isTop() or right_r.isTop():
                return right_r.Top()
            
            l = left_r.left()+right_r.left()
            r = left_r.right()+right_r.right()

            return Interval((l,r))
        
        
        if type(expr) == kachuaAST.Diff:
            left_r = self.resolve_expr(expr.lexpr,bin)
            right_r = self.resolve_expr(expr.rexpr,bin)

            if left_r.isBot() or right_r.isBot():
                return right_r.Bottom()
            if left_r.isTop() or right_r.isTop():
                return right_r.Top()
            
            l = left_r.left()-right_r.left()
            r = left_r.right()-right_r.right()

            return Interval((l,r))
        return Interval((1,0))

    '''
        Define the meet operation
        Returns a dictinary {varName -> abstractValues}
    '''
    def meet(self, predList):
        assert isinstance(predList, list)
        meetVal = {}
        # print(predList)
        for out in predList:
            for var in out.keys():
                meetVal[var] = Interval((1,0))
        for var in meetVal.keys():
            for out in predList:
                if var in out.keys():
                    # print(var)
                    # print(out[var].isTop())
                    meetVal[var] = meetVal[var].join(out[var])

        return meetVal

def analyzeUsingAI(ir, filename):
    '''
        get the cfg outof IR
        each basic block consists of single statement
    '''
    cfg = cfgB.buildCFG(ir, "cfg", True)
    cfgB.dumpCFG(cfg, "x")

    # call worklist and get the in/out values of each basic block
    bbIn, bbOut = AI.worklistAlgorithm(cfg)
    # print(bbOut)

    # print(bbOut['END'][0]["turt_x"])
    # print(filename)

    #implement your analysis according to the questions on each basic blocks
    final_x = bbOut['END'][0]["turt_x"]
    final_y = bbOut["END"][0]["turt_y"]

    if final_x.isBot():
        final_x = Interval((0,0))
    if final_y.isBot():
        final_y = Interval((0,0))
    
    # print(final_x.__str__()+" "+final_y.__str__())
    # print(final_x.__str__())
    # print(final_y.__str__())

    f = open(filename[:-3]+".json")
    data = json.load(f)
    # print(data['reg'][0])
    lt = data['reg'][0]
    rb = data['reg'][1]
    # print(final_x.__str__())
    # print(final_y.__str__())
    region_x = Interval((min(lt[0],rb[0]),max(lt[0],rb[0])))
    region_y = Interval((min(lt[1],rb[1]),max(lt[1],rb[1])))

    if final_x.meet(region_x).isBot() or final_y.meet(region_y).isBot():
        print("\n \nVerified Out of Danger")
    else:
        print("\n \nEnded In Danger might get eaten")

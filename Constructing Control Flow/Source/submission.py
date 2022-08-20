import graphviz
import sys
sys.path.insert(0, './ast')

import kachuaAST

def genCFG(ir):
    # your code here
    cfg = []
    size = len(ir)
    leaders = []

    for i in range(size):
    #    the start Instruction is always a leader
        if i==0:
            leaders.append(i)
    #   The instruction that is a target of the loop or branch condition is a leader.
        if ir[i][1] != 1:
            target = i+ir[i][1]
            if target < size:
                if target not in leaders:
                    leaders.append(target)
    #    The instruction that immediately follows the loop or branch condition is a leader

            if i < size-1:
                if i+1 not in leaders:
                    leaders.append(i+1)
    
    #   After the for-loop we got the list of leaders but they might not be sorted
    leaders.sort()
    
    # Lets first insert all the statements  

    for index in range(len(leaders)):
        BB = {'Block-No':index,'Instrustions':[],'Links':[]}
        if index < len(leaders)-1:
            for lineno in range(leaders[index],leaders[index+1]):
                BB['Instrustions'].append(ir[lineno][0])

        else:
            for lineno in range(leaders[index],size):
                BB['Instrustions'].append(ir[lineno][0])
        cfg.append(BB)
        
    
    
    
    # Now lets set the links between the basic blocks

    for index in range(len(leaders)-1):
        for lineno in range(leaders[index],leaders[index+1]):
            target = lineno+ir[lineno][1]
            
            if target < leaders[index+1] and target >= leaders[index]:
                continue
            
            
            elif target < size:
                flag = False
                for n in range(len(leaders)):
                    if(leaders[n] > target):
                        if (n-1) not in cfg[index]['Links']:
                            cfg[index]['Links'].append(n-1)
                            flag = True
                            break
                    
                if not flag:
                    if len(leaders)-1 not in cfg[index]['Links']:
                        cfg[index]['Links'].append(len(leaders)-1)
            
            
            
            else:
                if len(leaders) not in cfg[index]['Links']:
                 cfg[index]['Links'].append(len(leaders))
        
        if index+1 not in cfg[index]['Links']:
            cfg[index]['Links'].append(index+1)
        cfg[index]['Links'].sort()

# For the last block lets set links
    start = len(leaders)-1
    for lineno in range(leaders[start],size):
            target = lineno+ir[lineno][1]
            if target < size and target >= leaders[start]:
                continue
            elif target < size:
                for n in range(len(leaders)):
                    if(leaders[n] > target):
                        if n-1 not in cfg[index]['Links']:
                            cfg[start]['Links'].append(n-1)
                            break
                        

            
    if start+1 not in cfg[start]['Links']:
        cfg[start]['Links'].append(start+1)
    cfg[start]['Links'].sort()
    

    BB = {'Block-No':len(leaders),'Instrustions':[],'Links':[]}
    cfg.append(BB)
    
    
    return cfg





def dumpCFG(cfg):
    
    dot = graphviz.Digraph(comment='The Control Flow Graph')
    
    for index in range(len(cfg)):
        
        node_name = str(cfg[index]['Block-No'])
        instructions = ""
        
        for inst in cfg[index]['Instrustions']:
            instructions = instructions+str(inst)+"\n"
        
        dot.node(node_name, instructions)

    # After the nodes are created lets link them
    for index in range(len(cfg)):
        
        for link in cfg[index]['Links']:
            dot.edge(str(index),str(link))

    
    dot.format = 'pdf'
    name = input("\n Enter the name for out file: ")
    dot.render("out/"+name,view=True)
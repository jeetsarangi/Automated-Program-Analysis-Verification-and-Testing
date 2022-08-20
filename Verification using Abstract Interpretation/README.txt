Assignment 6A:Program Verification using Abstract Interpretation 
This assignment was about implementing various components of the Abstract implementation to make it work and then use it for verification of kachua scripts which will verify will the kachua to be safe or die at the end of the execution of a given  kachua script.
Now , to accomplish this I had to implement the abstract Interval class which will provide the abstract domain on which we do operate faster and can guarantee soundness also.
First,I had implemented the components of class interval which had various important functions which forms the basis of the abstract domain (Interval domain) .
Then,I had implemented the methods of the class ForwardAnalysis() which had functions like initialize(),transferfunction(),meet() to do all these I had extensively used the previously coded interval class and both these classes helps the Worklist Algorithm to work smoothly.
Following are the briefs about implementation of the methods:

Functions of class Interval:
* Join():this takes input a new Interval object and return a new joined interval.
* Meet():this takes input a new Interval and return the intersection or meet of them.
* Le and eq:these check if given interval is equal to it or not.
* I have had some self defined functions like left,right,bottom,top,neg,single.

Methods of forward analysis:
* Initialize():takes argument current basic block and if it not start node then it returns a suitbale initialization for bbin in that block.
* Meet():Takes input all predecessors outs and returns the join of them.
* Transfer function():Most crucial and very challenging function how the values of variables change from one program point entry to another at an exit is determined by this function .Hence I did it by making assumption of all possible instruction and how bbin changes for each of them to bbout.

AnalyseUsingAI : This takes input ir and the filename of json file where magarmach region is mentioned.Then I take the range of values of x in magarmach region and same for y now if these possible combination or x.y have any combination intersection with final x and final y ranges which were resulted at end of program as result of Abstract Interpretation then turtle might die else it will not die for sure.

How to run:
1. Unzip the files.
2. I have kept the whole kachua as it is just run as
python kachua.py -ai example/Testcases/Test0.tl

Note:The testcases and there expected outputs are given inside example folder also inside kachua core.
Limitations:
* For right and left (head angle) move instructions only multiples of 90 degree is allowed otherwise will not function as it is.
* For multiple condition statements the tool is not that efficient as for them it over approximates too much hence efficiency get hurts use temporary variables.
* Repeat statements goes into infinite looping even if repeat counter stops counting after reaching 3k or -3k it stops updating but still if there might be inner statements which keeps on updating and never stops .
* May be the framework have the problem so then infinite looping can't be stopped need to rethink.
Conclusion:
It was a fun yet very practical assignment understood Abstact Interpretation very clearly with this in practical applications.

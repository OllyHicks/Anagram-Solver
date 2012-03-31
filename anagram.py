#!/usr/bin/env python
import sys

import enchant
import itertools

class AnagramSolver:
    dictionaries=[]
    
    last_calcs=None
    
    def __init__(self, dictionaries):
        if not hasattr(dictionaries, '__iter__'):
            dictionaries=(dictionaries,)
            
        self.dictionaries=[enchant.Dict(dictionary) for dictionary in dictionaries]
    
    def search(self, letterList, outputLength):
        found=[];
        self.last_calcs=0;
        
        for guess in itertools.permutations(letterList, outputLength):
            # guess is a tuple of chars
            guess="".join(guess).capitalize()
            
            if all(dict.check(guess) for dict in self.dictionaries) and not guess in found:
                yield guess.lower()
                found.append(guess)
            self.last_calcs+=1
    
    def searchAll(self, letterList, minLength=3):
        for outputLength in range(minLength, len(letterList)):
            for word in self.search(letterList, outputLength):
                yield word 

if __name__=="__main__":
    
    if len(sys.argv)==3:
        letterList=sys.argv[1]
        outputLength=int(sys.argv[2])
    elif len(sys.argv)==2:
        letterList=sys.argv[1]
        outputLength=0
    else:
        letterList=raw_input("Letter list: ")
        outputLength=raw_input("Word length: ")
        
        if outputLength=='':
            outputLength=0
        else:
            outputLength=int(outputLength)
        
    print 
    
    solver=AnagramSolver(("en_GB","en_US"))
    if outputLength > 0:
        words=solver.search(letterList, outputLength)
    else:
        if outputLength < 0:
            words=solver.searchAll(letterList, -outputLength)
        else:
            words=solver.searchAll(letterList)
    
    print "Found: "
    for word in words:
        print " "+word

    print 

    print "Calculation: " + str(solver.last_calcs)

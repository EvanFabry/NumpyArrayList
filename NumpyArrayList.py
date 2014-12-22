# -*- coding: utf-8 -*-
import numpy


class NumpyArrayList:

    def __init__(self, initialCapacity=24000, cols=31, multiplier=2):
        self.capacity = initialCapacity
        self.cols = cols
        self.data = numpy.empty((initialCapacity,cols))
        self.data[:] = numpy.NaN
        self.multiplier = multiplier
        self.size = 0
        
    #Redefine bracket operators because 
    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= 0 and key < self.size:
                return self.data[key]
            elif key < 0 and -key < self.size:
                return self.data[self.size + key]
            else:
                print ("key: " + str(key))
                print ("size: " + str(self.size))
                print ("capacity: " + str(self.capacity))
                raise IndexError("Called to uninstantiated value")
        elif isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            if (start < 0): start = start - (self.capacity - self.size)
            if (stop < 0): stop = stop - (self.capacity - self.size)
            elif (stop == None): stop = self.size + 1
            return self.data[start:stop:step]
        else:
            print (type(key))
            print ("key: " + str(key))
            print ("size: " + str(self.size))
            print ("capacity: " + str(self.capacity))
            raise TypeError("index must be int or slice")

    def update(self, row):
        for r in row:
            self.add(r)

    def append(self, x):
        if self.size >= self.capacity:
            self.capacity *= self.multiplier
            newdata = numpy.empty((self.capacity,self.cols))
            newdata[:self.size] = self.data
            self.data = newdata

        self.data[self.size] = x
        self.size += 1
        
    def __len__(self):
        return self.size

    #Remove excess allocated space
    def finalize(self):
        data = self.data[:self.size]
        return numpy.reshape(data, newshape=(self.size, self.cols))
        
    #A binary search. Returns eaither a match or the first element before
    # the target if there is no match when exactMatch is set to False
    def mostRecentBinarySearch(self,target,lo=0,hi=None,exactMatch=False):
        if(hi==None):
            hi=len(self.data)-1
            if (len(self.data) <= 0): 
                print ("raising")
                raise
        index = int((hi+lo)/2)
        if(self.data[index].time()==target):
            return (index-1)
        elif(hi<=lo and exactMatch):
            return -1
        elif(hi<=lo):
            return index-1
        elif(self.data[index].time()>target):
            return self.binaryTimeSearch(target,lo=lo,hi=(index-1))
        elif(self.data[index].time()<target):
            return self.binaryTimeSearch(target,lo=(index+1),hi=hi)
        print ("Should have found and returned something in mostRecentBinarySearch, raising")
        raise
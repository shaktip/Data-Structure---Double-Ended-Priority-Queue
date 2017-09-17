import time
import sys, os
#program is accepting a command line argument of filename to sort
#use python Programname.py argument_value
#to run the python code.

NoOfLines = 100
NoOfLinesInFile = 0

#to get left of ith element in DEPQ
def left(i):
    return (2*i + 1)
#to get right of ith element in DEPQ
def right(i):
    return (2*i + 2)


#to get parent of ith element in DEPQ
def parent(i):
    return ((i-1)/2)
 
#to get min of  DEPQ
def getMin(mylist=[]):
    return mylist[0]
    
#to get max of DEPQ    
def printlist(mylist):
    for item in mylist:
        print item , " ",
 
#to insert Key in DEPQ         
def MinHeapInsertKey(minl, maxl, k):
    minl.append([k,0]);
    i = len(minl) - 1;
    while(i != 0 and minl[parent(i)][0] > minl[i][0]):
        maxl[minl[parent(i)][1]][1] = i
        minl[parent(i)] , minl[i] = minl[i] , minl[parent(i)]
        
        i = parent(i);
    return i;
        
#to insert corresponding key in max heap
def MaxHeapInsertKey(maxl, minl, k):
    maxl.append([k,0]);
    i = len(maxl) - 1;
    while(i != 0 and maxl[parent(i)][0] < maxl[i][0]):
        minl[maxl[parent(i)][1]][1] = i
        maxl[parent(i)] , maxl[i] = maxl[i] , maxl[parent(i)]        
        i = parent(i);
    #print 'Max Insert key ' , k , ' at index i = ' , i    
    return i;
    
#to heapify the DEPQ when element is removed
    
def MaxHeapify(maxl , minl , i):  #downwards
    while True :
        l = left(i);
        r = right(i);
        highest = i;
        if l < len(maxl) and maxl[l][0] > maxl[i][0] :
            highest = l;
        if r < len(maxl) and maxl[r][0] > maxl[highest][0]:
            highest  = r;
        if(highest != i) :
            minl[maxl[i][1]][1] = highest;
            minl[maxl[highest][1]][1] = i;
            maxl[i], maxl[highest] = maxl[highest], maxl[i];
            i = highest;
        else :
            break;    
        #MaxHeapify(maxl, minl , highest);
        
#to heapify the DEPQ when element is removed from DEPQ        
def MinHeapify(minl, maxl ,  i):  #downwards
    while True :
        l = left(i);
        r = right(i);
        smallest = i;
        if l < len(minl) and minl[l][0] < minl[i][0] :
            smallest = l;
        if r < len(minl) and minl[r][0] < minl[smallest][0] :
            smallest = r;
        if(smallest != i) :
            maxl[minl[i][1]][1] = smallest;
            maxl[minl[smallest][1]][1] = i;
            minl[i], minl[smallest] = minl[smallest] , minl[i];
            i = smallest;
        else :
            break;    
        #MinHeapify(minl, maxl , smallest);
        
#to get maximum of DEPQ
def GetMax(maxl):
    if(len(maxl) <= 0):
        return None;
    else:
        x = maxl[0];
        return x;
#to get minimum of DEPQ        
def GetMin(minl):
    if(len(minl) <= 0):
        return None;
    else:
        x = minl[0];
        return x;
        
#to remove Max from DEPQ        
def ExtractMax(maxl, minl):
    if(len(maxl) <= 0):
        return None;
    if(len(maxl) == 1):
        x = maxl[0];
        maxl.pop(0);
        minl.pop(0);
        return x;
    root = maxl[0];
    IndInMinL = maxl[0][1];
    minl[IndInMinL] = minl[len(minl) - 1];
    maxl[minl[len(minl) - 1][1]][1] = IndInMinL;
    minl.pop(len(maxl) - 1);
    i = IndInMinL;
    if i != len(minl) :
        while(i != 0 and minl[parent(i)][0] > minl[i][0]):
            maxl[minl[parent(i)][1]][1] = i
            maxl[minl[i][1]][1] = parent(i)
            minl[parent(i)] , minl[i] = minl[i] , minl[parent(i)]        
            i = parent(i);
        MinHeapify(minl , maxl, IndInMinL);  
    
    maxl[0] = maxl[len(maxl) - 1];
    minl[maxl[len(maxl) - 1][1]][1] = 0;
    maxl.pop(len(maxl) - 1);
    MaxHeapify(maxl , minl , 0);
    return root;

#to remove Min from DEPQ                   
def ExtractMin(minl, maxl):
    if(len(minl) <= 0):
        return None;
    if(len(minl) == 1):
        x = minl[0];
        minl.pop(0);
        maxl.pop(0);
        return x;
        
    root = minl[0];
    IndInMaxL = minl[0][1];
    maxl[IndInMaxL] = maxl[len(maxl) - 1];
    minl[maxl[len(maxl) - 1][1]][1] = IndInMaxL;
    maxl.pop(len(maxl) - 1);
    i = IndInMaxL;
    if i != len(maxl) :
        while(i != 0 and maxl[parent(i)][0] < maxl[i][0]):
            minl[maxl[parent(i)][1]][1] = i
            minl[maxl[i][1]][1] = parent(i)
            maxl[parent(i)] , maxl[i] = maxl[i] , maxl[parent(i)]        
            i = parent(i);
        MaxHeapify(maxl , minl, IndInMaxL);
    
    
    
    minl[0] = minl[len(minl) - 1];
    maxl[minl[len(minl) - 1][1]][1] = 0 ;
    minl.pop(len(minl) - 1);
    MinHeapify(minl, maxl , 0);
    
    return root;    

#partition function of quick sort, divides the word set into 3 files - Left, Middle , Right - where Left contains all the words less than or equal
#to the minimum ascii word of Middle and Right contains all the words greater than or equal to max ascii word of Middle - and combines them at
#end    
def partition(filename, low, high):
    #print "In partition call : " , NoOfLinesInFile
    MinList = list();
    MaxList = list();
    
    fp = open(filename,'r');
    fpLeft = open("Left.txt", "w");
    fpRight = open("Right.txt" , "w");
    fpMiddle = open("Middle.txt", "w");
    for i in range(1, low, 1):
        fp.readline();
    #line = fp.readline();
    #print "Partitions first line is :" ,line;
    up = low ;
    for i in range(0, NoOfLines, 1) :
        if up > high :
            break;
        word = fp.readline();        
        if word is not None:
            up = up + 1;
            while word.endswith("\n"):
                word = word[:-1];
            while word.endswith("\r"):
                word = word[:-1];    
            MinIndex = MinHeapInsertKey(MinList, MaxList , word);
            MaxIndex = MaxHeapInsertKey(MaxList ,MinList ,  word);
            MinList[MinIndex][1] = MaxIndex;
            MaxList[MaxIndex][1] = MinIndex;
        else:
            break;
            
    #print MinList;
    #print "\n";        
    flag = 1; 
    count = low;
    
    while True:         
         if up > high :
             break;
         up = up + 1;
         word = fp.readline();    
         if not word:
             break;
         while word.endswith("\n"):
             word = word[:-1];
         while word.endswith("\r"):
             word = word[:-1];   
              
         small = GetMin(MinList)[0];
         large = GetMax(MaxList)[0];
         #print "small is : " , small , " large is :", large , " Word is :" , word;
         if word <= small :
             fpLeft.write(word + "\n");
             count = count + 1;
         elif word > large :
             fpRight.write(word + "\n");
         else :
              if flag == 1:
                  r = ExtractMin(MinList, MaxList)[0];
                  #print "\nAfter extract from min : " , MinList
                  #print " \n And Maxlist : " , MaxList
                  fpLeft.write(r + "\n");
                  count = count + 1;
                  MinIndex = MinHeapInsertKey(MinList, MaxList , word);
                  MaxIndex = MaxHeapInsertKey(MaxList ,MinList ,  word);
                  MinList[MinIndex][1] = MaxIndex;
                  MaxList[MaxIndex][1] = MinIndex;
                  flag = 0;
              else:
                  r = ExtractMax(MaxList , MinList)[0];
                  #print "\n After extract from max minlist is: " , MinList
                  #print "\n And MaxList is : " , MaxList
                  fpRight.write(r + "\n");
                  MinIndex = MinHeapInsertKey(MinList, MaxList , word);
                  MaxIndex = MaxHeapInsertKey(MaxList , MinList , word);
                  MinList[MinIndex][1] = MaxIndex;
                  MaxList[MaxIndex][1] = MinIndex;
                  flag = 1;
         #print "\nMin list : " , MinList
         #print "\nMax List : " , MaxList      
     
            
    while len(MinList) != 0:
        r = ExtractMin(MinList , MaxList)[0];
        #print r
        fpMiddle.write(r + "\n");
    fp.close();
    fpLeft.close();
    fpRight.close();
    fpMiddle.close();
    result = open("ResultFile.txt" , "w");
    fp = open(filename , "r");        
    fpLeft = open("Left.txt","r");
    fpMiddle = open("Middle.txt","r");
    fpRight = open("Right.txt", "r");
    #print "Value of low is : " , low;
    for i in range(1,low,1):
        #print "Test\n";	
        line = fp.readline();
        result.write(line);
    
    for line in fpLeft:
        result.write(line);
        fp.readline();
        
    for line in fpMiddle:
        result.write(line);
        fp.readline();
        
    for line in fpRight:
        result.write(line);
        fp.readline();
    while True:
        line = fp.readline();
        if not line:
            break;
        result.write(line);
                
    fp.close();
    result.close();
    fpLeft.close();
    fpRight.close();
    fpMiddle.close();
    os.rename("ResultFile.txt",filename);
    return count;         
#recursive quicksort function                 
def quicksort(filename, low, high):
    #print "In Quick Sort call : " , NoOfLinesInFile
    stack = list();
    stack.append(low);
    stack.append(high);
    while len(stack) != 0:
        high = stack.pop(len(stack) - 1);
        low = stack.pop(len(stack) - 1);
        p = partition(filename, low , high);
        print "p:", p ;
        if p > low :
            stack.append(low);
            stack.append(p);
        if p+1+NoOfLines < high :
            stack.append(p+1+NoOfLines);
            stack.append(high);



#  Recursive QuickSort is getting Runtime error of maximum recursion
#depth occurred
#    if low < high:
#        j = partition(filename, low, high);
#        #print "Quick sort partition at : " + str(j);
#        print "." , j
#        quicksort(filename, low , j);
#        quicksort(filename, j+1+NoOfLines , high);        

start_time = time.time(); 
total = len(sys.argv)
cmdargs = str(sys.argv)
#print ("The total numbers of args passed to the script: %d " % total)
#print ("Args list: %s " % cmdargs)
# Pharsing args one by one
if total != 2:
    print ("Insufficient no of arguments");
    exit(0);
     
#print ("Script name: %s" % str(sys.argv[1]))
filename = str(sys.argv[1]);
try :
    fp = open(filename, 'r');
except IOError :
    print "Error in file";
    exit(0);    
#Handle the file not found Error here
  
n = fp.readline();
try:
    NoOfLinesInFile = int(n);
except ValueError:
    print "The first value in file must be integer";
    exit(0);
    
#print "No of lines in the file are :" , NoOfLinesInFile
fp.close();
quicksort(filename, 2, NoOfLinesInFile+1); 
print("Execution time required is : %s seconds" % (time.time() - start_time)); 



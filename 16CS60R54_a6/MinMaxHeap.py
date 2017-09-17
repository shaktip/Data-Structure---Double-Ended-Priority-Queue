import sys, os
key = 0
mylist = list();
#initialization of hash table of size 100
def init():
    global mylist;
    for i in range(0, 100) :
        mylist.append(list());
        
#to compute hash value of given string s        
def hashfunction(s) :
    global key ;
    key = 7;
    global mylist;
    sm = 0;
    for i in range(0, len(s)) :
        key = key * 3 + ord(s[i]);
    #print "key is :" , key;    
    key = key % 100;
    return key;
    
        
#to find left of ith element in heap which is 2*i + 1  
def left(i):
    return (2*i + 1);
#to find right of ith element in heap which is 2*i + 2    
def right(i):
    return (2*i + 2)
#to return parent of any ith element in heap which is (i-1)/2    
def parent(i):
    return ((i-1)/2)
    
#to check whether heap is empty or not    
def isEmpty(mylist):
    if len(mylist) == 0 :
        return 1;
    else:
        return 0;

#to display the heap         
def printlist(mylist):
    for item in mylist:
        print item , " ",
         
#to insert the element in MinHeap and also adjust the index of shuffeled elements in corresponding maxheap
def MinHeapInsertKey(minl, maxl, k):
    global mylist;
    loc = hashfunction(k);
    mylist[loc].append(k);
    
    minl.append([k,0]);
    i = len(minl) - 1;
    while(i != 0 and minl[parent(i)][0] > minl[i][0]):
        maxl[minl[parent(i)][1]][1] = i
        minl[parent(i)] , minl[i] = minl[i] , minl[parent(i)]
        
        i = parent(i);
    return i;
        
#to insert the element in MaxHeap and also adjust the index of shuffled elements in corresponding MinHeap
def MaxHeapInsertKey(maxl, minl, k):
    maxl.append([k,0]);
    i = len(maxl) - 1;
    while(i != 0 and maxl[parent(i)][0] < maxl[i][0]):
        minl[maxl[parent(i)][1]][1] = i
        maxl[parent(i)] , maxl[i] = maxl[i] , maxl[parent(i)]        
        i = parent(i);
    #print 'Max Insert key ' , k , ' at index i = ' , i    
    return i;

#Heapify is required to be called when the Max element from root position is removed, it is used to arrange the tree so that it satisfies
#the property of MaxHeap again
    
def MaxHeapify(maxl , minl , i):  #downwards
    while True:
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
            #MaxHeapify(maxl, minl , highest);
            i = highest;
        else:
            break;    
        
#To heapify the MinHeap after removing the element from MinHeap        
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
        #MinHeapify(minl, maxl , smallest);
        else :
            break;
#to get the Maximum element from MaxHeap, which is located at root position.
def getMax(maxl):
    if(len(maxl) <= 0):
        return None;
    else:
        x = maxl[0][0];
        return x;
#to get the minimum element from MinHeap, which is located at root position.        
def getMin(minl):
    if(len(minl) <= 0):
        return None;
    else:
        x = minl[0][0];
        return x;

#to return the size of an array        
def size(minl):
    return len(minl);

#to remove the Maximum element from DEPQ            
def ExtractMax(maxl, minl):
    if(len(maxl) <= 0):
        return None;
    if(len(maxl) == 1):
        x = maxl[0];
        maxl.pop(0);
        minl.pop(0);
        return x;
    #print mylist;
    #print "Mylist[0][0] : is " , maxl[0][0];    
    i = 0;    
    loc = hashfunction(maxl[0][0]);
    #print "Location is :" , loc;
    
    for word in mylist[loc]:
       # print "Word is :" , word;
        if word == maxl[0][0]:
            mylist[loc].pop(i);
            break;
        else :
            i = i + 1;
            
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
    
#to remove the minimum element from DEPQ                   
def ExtractMin(minl, maxl):
    global mylist;
    if(len(minl) <= 0):
        return None;
        
    i = 0;    
    loc = hashfunction(minl[0][0]);
    for word in mylist[loc]:
        if word == minl[0][0]:
            mylist[loc].pop(i);
            break;
        else :
            i = i + 1;
                    
                    
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


    
MinList = list();
MaxList = list();
init();

filename = "xyz";
flag = 0;
while True:
    print "1. IsEmpty.   2. Size       3. GetMin     4. GetMax   "
    if len(MinList) == 0 :
        print "5. BuildDEPQ",
        flag = 0;
    else :
        print "5. put(x)",
        flag = 1;    
    print " 6. RemoveMin  7. RemoveMax  8.IsContains(x) 9.Exit"
    while True:
        try:
            x = int(raw_input("Enter your choice :"));
            break;
        except ValueError:
            print "Please Enter proper no";
            
    #print "Value of x is :" , x;
    if x in range(1, 9):
        if x == 1:    #isempty
            if(isEmpty(MinList) == 1):
                print "DEPQ is empty";
            else:
                print "DEPQ is not empty";
            
        
        elif x == 2:   #size
            print "Size of DEPQ is " , size(MinList);
                            
        elif x == 3:   #GetMin
            print "Minimum of DEPQ is ", getMin(MinList);
          
        elif x == 4:    #GetMax
            print "Maximum of DEPQ is " , getMax(MaxList);
                
        elif x == 5:     
            if flag == 0 :    #BuildDEPQ
                try:
                    filename = raw_input('Enter file name :')
                    print "File name is " , filename;
                    fp = open(filename, 'r');
                except IOError:
                    print "File Error";
                    sys.exit(0);
                    
                #Handle the file not found Error here
                n = fp.readline();
                NoOfLinesInFile = int(n);
                #Handle int error here
                for line in fp:
                    while line.endswith("\n") :
                        line = line[:-1];
                    while line.endswith("\r") :
                        line = line[:-1];    
                    MinIndex = MinHeapInsertKey(MinList, MaxList , line);
                    MaxIndex = MaxHeapInsertKey(MaxList ,MinList , line);
                    MinList[MinIndex][1] = MaxIndex;
                    MaxList[MaxIndex][1] = MinIndex;

                     
            else :     #put(x)
                x = raw_input("Enter a string to insert in DEPQ : ");
                MinIndex = MinHeapInsertKey(MinList, MaxList , x);
                MaxIndex = MaxHeapInsertKey(MaxList ,MinList , x);
                MinList[MinIndex][1] = MaxIndex;
                MaxList[MaxIndex][1] = MinIndex;
            
        elif x == 6:      #remove min
            x = ExtractMin(MinList,MaxList);
            if x is not None :
                print "Minimum removed :" , x[0]
            else :
                print "Minimum removed is None";
        elif x == 7:     #remove max
            x = ExtractMax(MaxList,MinList);
            if x is not None :
                print "Maximum removed :" , x[0];
            else :
                print "Maximum removed is None ";
        elif x == 8:     #iscontains
            x = raw_input("Enter a string to search :");
            containsFlag = 0;
            loc = hashfunction(x);
            for word in mylist[loc]:
                if word == x:
                    containsFlag = 1;
                    print "Yes";
                    break;
            if containsFlag == 0:
                print "No";        
                       
        print "\t_________________________________________________________";     
    else:
        #print "Invalid choice";
        sys.exit(0);
    


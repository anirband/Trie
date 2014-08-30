#!/usr/bin/env python

def insert(trie,key,value,doc_no,flag=''):                          #Inserts values in trie
    if key is None:
        return
    if key:
        first,rest=key[0],key[1:]
        flag=flag+key[0]
        if first not in trie:
            trie[first]={}
        insert(trie[first],rest,value,doc_no,flag)
    else:
        trie['value']=[flag,value]
        trie['doc_no']=[doc_no]


def haskey(trie,key):                                #Checks if key exists and returns TRUE/FALSE
    if key is None:
        return(False)
    if key:
        first,rest=key[0],key[1:]
        if first not in trie:
            return(False)
        else:
            return(haskey(trie[first],rest))
    return(True)

def getvalue(trie,key):                              #Get stored value for the key
    if key:
        first,rest=key[0],key[1:]
        if first not in trie:
            return 0
        else:
            return(getvalue(trie[first],rest))
    return(trie['value'][1])

def increasevalue(trie,key,value,doc_no):                   #Increases the value of the key, used while inserting elemtnts
    if key:
        first,rest=key[0],key[1:]
        if first not in trie:
            return 0
        else:
            return(increasevalue(trie[first],rest,value,doc_no))
    trie['value'][1]=trie['value'][1]+value
    trie['doc_no'].append(doc_no)


def extract_value(v):                                 #Extracts the substring and its value, used by substr function
    L=[]
    for key,value in v.iteritems():
            if key=='value':
                L.append(value)
            elif key=='doc_no':
                continue
            else:
                X=extract_value(value)
                for elem in X:
                    L.append(elem)
    return L
 

def create_trie(wordl):                              #Creates the trie given a list of strings
    d={}
    L=len(wordl)
    k=0
    for word in wordl:
        if word is not None:
            keycount={}
            for i in range(len(word)):
                for j in range(i+1,len(word)+1): 
                    if word[i:j] not in keycount:
                        #print word[i:j]
                        keycount[word[i:j]]=1
                        if haskey(d,word[i:j]):
                            increasevalue(d,word[i:j],1,k)
                        else:
                            insert(d,word[i:j],1,k)
        k=k+1
    return d

def substr(trie,count_threshold=1,length_threshold=1,no_doc_threshold=1):   #Takes a trie, count threshold and length threshold and returns list of substring, its count and the documents in which they occur
    d=trie                                                
    sub_str=[]    
    for k,v in d.iteritems():
            if k=='value':
                if elem[1]>=count_threshold and len(elem[0])>=length_threshold:
                    sub_str.append(v)
            else:
                l=extract_value(v)
                for elem in l:
                    if elem[1]>=count_threshold and len(elem[0])>=length_threshold:
                        sub_str.append(elem)
    result={}
    for elem in sub_str:
            doc=get_doc_no(trie,elem[0])
            if len(doc)>=no_doc_threshold:
                result[elem[0]]={'count':elem[1],'doc_no':doc}

    return result

def get_doc_no(trie,string):                           #Gets the document number that has the substring
    if haskey(trie,string):
        n=len(string)
        X=trie[string[0]]
        for i in range(1,n):
            X=X[string[i]]
        return(X['doc_no'])
    else:
        return None



wordl=['ana  ppleop','ikno  pplens','yy  dpplsar','notoap  tple'] #List of string for the trie

d=create_trie(wordl)                        #d is the trie created

print d                                     #Prints the Trie

print get_doc_no(d,'pp')

print get_doc_no(d,'pple')

print get_doc_no(d,'hii')

print getvalue(d,'hello')

print getvalue(d,'app')

print getvalue(d,'pp')

print haskey(d,'hi')

print haskey(d,'pp')

print substr(d,3,2,4)

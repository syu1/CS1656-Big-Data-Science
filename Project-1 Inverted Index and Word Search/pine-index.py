# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 00:51:07 2019

@author: samyu
"""
import glob, os, nltk, pandas,string, json
from string import digits

from nltk.stem.porter import PorterStemmer


# For the sake not breaking the unknwown testing enviroment
# We will read file names as input\\doc1.txt instead of using
# os.chdir to take off input\, instead we will cleanup using simple slicing
files_list = glob.glob('input\*')
# hopefully none of the words have the name super_unique_total_files, if this is a problem replace with RNG names lol
my_dict= {"super_unique_total_files":len(files_list)}
porter = PorterStemmer()
remove_digits = str.maketrans('', '', digits)

# Loop over our files clean them and save all words to a list
for i,file in enumerate(files_list):
    fp = open(file,"r")
    csv_object = pandas.read_csv(fp,delimiter=" ")
    for j,word in enumerate(csv_object.columns):
        word = word.lower()
        s = word
        word = ''.join([i for i in s if not i.isdigit()])
        if word =="":
            continue
        word = word.translate(str.maketrans('','',string.punctuation))
        word = porter.stem(word)
#####################GOOOD###################        
        found = my_dict.get(word,"false")
        # Checks if WORD is in the index
        clean_file_name = file[6:]

        if found == "false":
            # Remove the /input
            # Storage of inverted index example #dictionary->[[doc1,2],[doc2,3],[doc3,4]] conceptual
            # For speed purposes double dictionary muahahahahahahhahahahha
            # #dictionary = word={
            # doc1:2,
            # doc2:3,
            # doc3:4
            # }
            my_dict.update({word:{clean_file_name:1}})
        # Checks if this WORD found in this FILE has the FILE NAME listed in the WORD's dictionary
        else:
            document_in_index = my_dict[word].get(clean_file_name,"false")
            # Did NOT find the document name listed, add it
            # For some reason this is not working correctly the second time through
            if document_in_index == "false":
                my_dict[word].update({clean_file_name:1})
            # FOUND the document name increment by 1
            else:
                increment = my_dict[word][clean_file_name]
                increment+=1
                my_dict[word].update({clean_file_name:increment})
    fp.close()
print(my_dict)                  

json_object = json.dumps(my_dict)
json_file = open("inverted-index.json","w")
json_file.write(json_object)
json_file.close()
# I should prolly refactor this... its kinda hacky
            
            
    
    
    

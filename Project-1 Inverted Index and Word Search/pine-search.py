# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 20:58:51 2019

@author: samyu
"""
import glob, os, nltk, pandas,string, json, math
from string import digits
from nltk.stem.porter import PorterStemmer
# Setup
porter = PorterStemmer()
remove_digits = str.maketrans('', '', digits)
# Clean word
def clean_words(query_list):
    for i,query in enumerate(query_list):
        
        query = query.lower()
        query = query.translate(str.maketrans('','',string.punctuation))
        query = query.translate(remove_digits)
        concatenated_query = ""
        my_keyword_list = query.split()
        for j,my_keyword in enumerate(my_keyword_list):
            my_keyword = porter.stem(my_keyword)
            
            concatenated_query= concatenated_query+my_keyword+ " "
        concatenated_query = concatenated_query.rstrip() 
        query_list[i] = concatenated_query
    return query_list

class Weighted:
    def __init__(self, document):
        self.document = document
        self.partial_weight_dict ={}
        self.total_weight = None
        
    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.document == other.document  
        
    def add_partial(self,keyword,partial_weight):
        self.partial_weight_dict[keyword] = partial_weight
        return None
    def sum_weights(self):
        sums = sum(self.partial_weight_dict.values())
        self.total_weight = sums
        return None
# Query is going to be a string
def num_words_in_query(query):
    # This is kinda hacky haha I hope you can understand it
    query_count = len(query.split())
    return query_count
def get_words_list(query):
    words_list = query.split()
    return words_list

# returns first index of first instance of weighted object
    
def check_if_weight_already_in_list(found_weighted_object,weighted_list):
    for i,weighted_object in enumerate(weighted_list):
        if found_weighted_object.document == weighted_object.document:
            return i 
    return -2

# Open Up the index
json_file = open("inverted-index.json","r")
json_file = json.load(json_file) # This returns a dictionary object
key_word_file = open("keywords.txt","r")

# Split like this so we can track multiple keywords
key_word_list = key_word_file.read().splitlines()
key_word_list = clean_words(key_word_list)
# Iterate each key(aka each line in the key-word file)
for key in key_word_list:
    weight_list = [] # Create a list of Weighted objects that store the document name, total weight and composite weights
    # Iterate of the number of words in a key(single line of text)   
    for i in range(0,num_words_in_query(key)):
        # Split those words up from their single line
        words = get_words_list(key)
        # Search the dictionary(json_file) for a single keyword
        found = json_file.get(words[i],'false')
        # If that keyword is not found continue on to the single space delimted keyword in our string(single line of text)
        if found == 'false':
            continue
        # Else calculate the weight of that single keyword from our inverted index by using our stored values
        else:
            document_list = found.keys() # A list of the documents that contain our single keyword
            # Iterate over that list of documents
            for document in document_list:
                # fetch the number of appearences of our single keyword that the document stores in its dictionary 
                num_appear = found[document]
                # Calculate the weight of that single keyword
                # (1 + log2 freq(key,doc)) * log2 (N / n(doc))
                
                partial_weight =  (1+(math.log(num_appear,2))) * math.log((json_file['super_unique_total_files']/len(document_list)),2)
                # Create a Weighted object that will store the document name and a list of partial weights of each single keyword in our string(line of text)
                found_document = Weighted(document)
                # See if our newley created document is already in the weighted list
                # This is a case for a query that has multiple words and multiple words are present in the same document
                index_found_doc = check_if_weight_already_in_list(found_document,weight_list)
                # if the index found is 0 or greater that means the document is already in our list
                if index_found_doc >=0:
                # Update the already weighted document with a new keyword and a new partial weight
                    weight_list[index_found_doc].add_partial(words[i],partial_weight)
                # Otherwise add a new weighted document to the weighted list
                else:
                    found_document.add_partial(words[i],partial_weight)
                    weight_list.append(found_document)
                
    # Sum up all the weights for our query(single line of text)
    for weight in weight_list:
        weight.sum_weights()
    
    if not weight_list:
        print("Keyword "+key+" is NOT in the index!!!\n")
    else:
        print("\nkeywords = " + key+"\n")
        words2 = get_words_list(key)
        weight_list.sort(key=lambda x: x.total_weight, reverse=True)
        for i,thing in enumerate(weight_list):
            print("file="+thing.document, end = ": ")
            rounded_total_weight = round(thing.total_weight,6)
            print("total score="+str(rounded_total_weight))
            for key,value in thing.partial_weight_dict.items():
                rounded_value = round(value,6)
                print ("weight("+str(key)+")"+"="+str(rounded_value))
            
            
    
import csv
import sys
from itertools import combinations
from itertools import permutations 
# Kinda global variables
# Create the empty candidate key dict
def create_empty_candidate_dict(my_input_csv):
    global total_transactions
    global raw_list
    count_tuple = ()
    candidate_list = []
    candidate_dict = {}
    partial_candidate_list = []
    with open(my_input_csv, 'r') as file:
      reader = csv.reader(file)
      raw_list = list(reader)
    # Probably stop doing combinations as soon as the number of verified itemsets hits zero for a combination.
    # i.e when the combinations of 4 hits 0 verified itemsets. I can't think of any corner cases where 
    # This idea would be false.
    # This is gonnna be inefficent oh boy
    total_transactions = len(raw_list)
    for i, transaction in enumerate(raw_list):
        # Rip out the first item read in from the csv
        # We don't care about what trasaction number it is
        # I hate enumerating in python. Its either a for loop or a range ugh
        raw_list[i] = transaction[1:]
    
    # Now count everything
    # Use set theory to do uniqueness
    # Make everything tuples i guess
    # Maybe I have to set it to a tuple I have no choice due to the way combinations is written
    for i, transaction in enumerate(raw_list):
        for j, item in enumerate(transaction):
                count_tuple = count_tuple + tuple(item)
    count_tuple = set(count_tuple)
    comb_list = list(count_tuple)
    comb_list.sort()
    # Also rip this N! runtime. In the future should stop making combinations when I hit the support threshold probaly

    for i in range(len(comb_list)):
        candidate_list.append(combinations(comb_list, i+1)) 
    for thing in candidate_list:
        for thing2 in thing:
            partial_candidate_list.append(tuple(thing2))
    for element in partial_candidate_list:
        candidate_dict[element] = 0
        
    return candidate_dict
# Remember that each key is a tuple!
def fill_candidate_dict(my_input_csv):
    # Basically do all possible combinations on each individul transaction record
    candidate_dict = create_empty_candidate_dict(my_input_csv)
    tuple_list = []
    
    # Convert transaction to a tuple
    for transaction in raw_list:
        for i in range(len(transaction)):
            
            tuple_list.append(combinations(transaction,i+1))
    for my_iterator in tuple_list:
        for trans_tuple in my_iterator:           
            if trans_tuple in candidate_dict:
                candidate_dict[trans_tuple] = candidate_dict[trans_tuple] + 1
    #print(candidate_dict)
    return candidate_dict 
        
def verify_candidate_dict(candidate_dict, support, output_file):
    records_list = candidate_dict.keys()
    verified_dict = {}
    the_file = open(output_file,'w+')
    for key in records_list:
        support_percent = (candidate_dict[key]/total_transactions)
        #print(len(key))
        if support_percent >= float(support):
            str_key = ','.join(key)
            str_support = format(support_percent,'.4f')
            output_str = f"S,{str_support},{str_key}"
            
            the_file.write(output_str+'\n')
            verified_dict[key] = support_percent
    the_file.close()
    return verified_dict


def calculate_confidence(final_verified_dict, confidence,output_file):
    # There should be no duplicates in my final_verfied_dict I think
    v_records_list = list(final_verified_dict.keys())
    # The max set size should be the last tuple since its in lex order I belileve
    confidence_dict = {}
    the_file = open(output_file,'a+')
    newline = ''
    for key in reversed(v_records_list):
        if len(key) == 1:
            continue
        else:
            prediction_support = final_verified_dict[key]
            #print(key)
            prediction = key
            
            prediction_set = get_conf_powerset(prediction)
            for lhs in prediction_set:
                
                #print(lhs)
                #print(prediction_set)
                # This if statement may be redundant
                # sweet this works wooooo
                rhs = tuple(set(prediction)-set(lhs))
                confidence_dict[lhs] = rhs
                calculated_confidence = round((prediction_support/final_verified_dict[lhs]),4)
                if calculated_confidence >= float(confidence):
                    str_lhs = ','.join(lhs)
                    str_rhs = ','.join(rhs)
                    formated_conf = format(calculated_confidence,'.4f')
                    formated_support = format(prediction_support,'.4f')
                    output_str = f"R,{formated_support},{formated_conf},{str_lhs},'=>',{str_rhs}"
                    
                    the_file.write(newline+output_str)
                    newline = '\n'
                    #print(output_str)
            newline = '\n'
    the_file.close()
    return confidence_dict
# nPr


def get_conf_powerset(my_set):
    powerset = ()
    true_pset = []
    for i in range(len(my_set)-1):
        powerset= powerset+tuple(combinations(my_set,i+1))
    for n_set in powerset:
        true_pset.append(tuple(n_set))
    return tuple(true_pset)

def create_out_put_filename(output_file,support,confidence):
    cut_csv_output = output_file[:-4]
    #print(cut_csv_output)
    my_output_filename = f"{cut_csv_output}.sup={support},conf={confidence}.csv"
    return my_output_filename

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    support = sys.argv[3]
    confidence = sys.argv[4]
    output_file = create_out_put_filename(output_file,support,confidence)
    # Depreciated I didn't end up needing to return some of the dicts lol
    final_candidate_dict = fill_candidate_dict(input_file)
    final_verified_dict = verify_candidate_dict(final_candidate_dict,support,output_file)
    final_confidence_dict = calculate_confidence(final_verified_dict, confidence,output_file)
    #get_powerset([1,2,3])
    #print(final_verified_dict)
    #print((final_confidence_dict))


if __name__ == "__main__": main()

import sys
import pandas as pd
# Read the ascii tree_dict from tree_dict file file
def read_tree_file(tree_file): 
    with open(tree_file) as tree_file:
        tree_lines_list = tree_file.readlines()
        # Get rid of new lines from ascii tree_dict
        for i, line in enumerate(tree_lines_list):
            tree_lines_list[i] = line.replace("\n","") 
    return tree_lines_list

def read_line_info(line):
    line_data = line.split(" ") 
    # Get rid of empty quotes ''
    line_data = [item for item in line_data if item != '']
    # Count pipes
    depth = line_data.count("|")
    # Get feature based on depth
    feature = line_data[depth]
    f_value = line_data[depth+1].strip(":")
    # Initalize these two
    category = None 
    # Skip the entries that tell you just color
    if (len(line_data) - depth) == 4: 
        category = line_data[depth+2]
    return (depth, feature, f_value, category)

def create_tree_dict(tree_list):
    # Initalize the dictionary and values
    tree_dict = {}
    level_one = (None, None) 
    level_two = (None, None) 
    branching_choices = set([]) 
    tree_dict["UNMATCHED"] = 0

    for line in tree_list:
        depth, feature, f_value, category = read_line_info(line)
        # Read first level
        if depth == 0:
            if feature not in tree_dict:
                tree_dict[feature] = {}
                tree_dict[feature][f_value] = {}
            else:
                if f_value not in tree_dict[feature]:
                    tree_dict[feature][f_value] = {}

            if  category != None:
                # Initalize a new category
                tree_dict[feature][f_value][category] = 0 
                branching_choices.add(category)

            level_one = (feature, f_value)
        # Read level two
        elif depth == 1:
            lvl1_feature = level_one[0]
            lvl1_value = level_one[1]

            if feature not in tree_dict[lvl1_feature][lvl1_value]:
                tree_dict[lvl1_feature][lvl1_value][feature] = {}
                tree_dict[lvl1_feature][lvl1_value][feature][f_value] = {}
            else:
                if f_value not in tree_dict[lvl1_feature][lvl1_value][feature]:
                    tree_dict[lvl1_feature][lvl1_value][feature][f_value] = {}

            if category != None:
                # Initalize a new category
                tree_dict[lvl1_feature][lvl1_value][feature][f_value][category] = 0
                branching_choices.add(category) 

            level_two = (feature, f_value)
        # Read level three
        else:
            lvl1_feature = level_one[0]
            lvl1_value = level_one[1]
            lvl2_feature = level_two[0]
            lvl2_value = level_two[1]

            if feature not in tree_dict[lvl1_feature][lvl1_value][lvl2_feature][lvl2_value]:
                tree_dict[lvl1_feature][lvl1_value][lvl2_feature][lvl2_value][feature] = {}
                tree_dict[lvl1_feature][lvl1_value][lvl2_feature][lvl2_value][feature][f_value] = {}
            else:
                if f_value not in tree_dict[lvl1_feature][lvl1_value][lvl2_feature][lvl2_value][feature]:
                    tree_dict[lvl1_feature][lvl1_value][lvl2_feature][lvl2_value][feature][f_value] = {}
            
            if category != None:
                # Initalize a new category
                tree_dict[lvl1_feature][lvl1_value][lvl2_feature][lvl2_value][feature][f_value][category] = 0  
                branching_choices.add(category)
   
    return (tree_dict, branching_choices)

    
# Read the test data_string and turn it into a tree based on our tree_dict
def create_test_tree(tree_dict, data_csv, branching_choices):
    
    with open(data_csv) as test_data_file: 
        data_string = pd.read_csv(test_data_file)
        # Get rid of extra quotes in the column header
        data_string.columns = [column.strip(' "') for column in data_string.columns]

    column_names = data_string.columns
    og_tree = tree_dict 
    for index, row in data_string.iterrows(): 
       
        found_choice_sentry = False

        # For tree of height three
        for i in range(3):
            for name in column_names:
                # Find the column name in the tree dict
                if name in tree_dict: 
                    data_value = row[name].strip(' \'"')
                    # if the data_value is present in the dict
                    # Use data value in dict
                    if data_value in tree_dict[name]:
                        tree_dict = tree_dict[name][data_value] 

        for choice in branching_choices: 
            if choice in tree_dict:
                found_choice_sentry = True
                tree_dict[choice] += 1

        if found_choice_sentry == False:
            og_tree["UNMATCHED"] += 1
        # Reset the tree_dict for the next row
        tree_dict = og_tree 

    return og_tree

def newly_trained_tree(parsed_tree, tree_dict, branching_choices): 
    level_one = (None, None)
    level_two = (None, None)
    no_match_sentry = tree_dict["UNMATCHED"]

    for line in parsed_tree:
        depth, feature, f_value, category = read_line_info(line)
        # Root level
        if depth == 0:
            sub_dict = tree_dict[feature][f_value]
            
            found_choice_sentry = False
            for choice in branching_choices:
                if choice in sub_dict:
                    print(f"""{feature} {f_value}: {choice} ({sub_dict[choice]})""")
                    found_choice_sentry = True
            if found_choice_sentry == False:
                print(f"""{feature} {f_value}""")

            level_one = (feature, f_value)
        # Height two
        elif depth == 1:
            lvl1_feature = level_one[0]
            lvl1_value = level_one[1]

            sub_dict = tree_dict[lvl1_feature][lvl1_value][feature][f_value]

            found_choice_sentry = False
            for choice in branching_choices:
                if choice in sub_dict:
                    print(f"""|   {feature} {f_value}: {choice} ({sub_dict[choice]})""")

                    found_choice_sentry = True
                    
            if found_choice_sentry == False:
                print(f"""|   {feature} {f_value}""")

            level_two = (feature, f_value)
        # Height three
        else: 
            lvl1_feature = level_one[0]
            lvl1_value = level_one[1]
            lvl2_feature = level_two[0]
            lvl2_value = level_two[1]

            sub_dict = tree_dict[lvl1_feature][lvl1_value][lvl2_feature][lvl2_value][feature][f_value]
            found_choice_sentry = False
            for choice in branching_choices:
                if choice in sub_dict:
                    print(f"""|    |   {feature} {f_value}: {choice} ({sub_dict[choice]})""")
                    found_choice_sentry = True
            if found_choice_sentry == False:
                print(f"""|   |   {feature} {f_value}""")    
    if no_match_sentry >= 1: 
        print("UNMATCHED: " , tree_dict["UNMATCHED"])


def main():
    tree_file = sys.argv[1]
    test_data_file = sys.argv[2]

    parsed_tree_text = read_tree_file(tree_file)
    init_tree_dict, branching_choices = create_tree_dict(parsed_tree_text)

    my_test_tree = create_test_tree(init_tree_dict, test_data_file, branching_choices)
    newly_trained_tree(parsed_tree_text, my_test_tree, branching_choices)

if __name__ == "__main__": main()



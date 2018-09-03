""""
Objective: This code is used to extract user IDs of the case and control groups based on the Phenotype file for each binary trait.
Procedures:
    1.  (Manually) Indicate the tags of values in Phenotype file for each binary trait, it means to specify whether a value of an individual is positive (Case) or negative (Control). Tag file for each trait is saved under the "Tag" folder with trait as its file name.
    2.  Generate a group file for each trait, file ({"Case":[a list of user id],"Control": [another list of user id]}) will be saved under "Group" folder. 
    3.  Create a CSV file to test the constraint (exclude the users with unreadable genetic test results): the number of case/control is greater than 10

Input: folder of the Phenotype file and ErrorUsers file
Output: 
    1.  gourp files of traits with trait name as file name
    2.  CSV file of case and control group numbers of traits
"""

import numpy as np
import pandas
import sys
import os.path
import re
import json
import config

if __name__ == "__main__":
    if len(sys.argv) <= 0:
        print "Please provide the folder of the ErrorUsers."
        exit(1)

    folder = sys.argv[1]

    if not os.path.exists(folder):
        print "The folder doesn't exist!"
        exit(1)

    filePath = os.path.join(folder, "ErrorUsers.txt")
    if not os.path.exists(filePath):
        print "The path to the ErrorUsers doesn't exist!"
        exit(1)

    with open(filePath,'r') as df:
        error_user = json.load(df)
    
    filePath = os.path.join(folder, "Categorical_Type.csv")
    if not os.path.exists(filePath):
        print "The path to the Categorical_Type doesn't exist!"
        exit(1)

    category = pandas.read_csv(filePath)


    def remove_invalid_filename(filename):
        return re.sub('[^\w\-_\. ]', '_', filename)

    def loadgroup(trait):
        traitfile = remove_invalid_filename(trait + ".txt")
        with open(os.path.join(folder, config.Folder_Attributes["group"], traitfile), 'r') as df:
            d = json.load(df)
        
        case = len(d["Case"])
        control = len(d["Control"])
        for k in d["Case"]:
            if(k in error_user):
                case = case - 1
        for k in d["Control"]:
            if(k in error_user):
                control = control -1
        return [case , control]


    headers = ["Trait", "Case", "Control", "Both groups meet requirement"]

    d = pandas.DataFrame(columns = headers)

    for i, item in category.iterrows():
        v = item["Is Categorize Trait"]
        if(v == 'Y'):
            trait = item["Traits"]
            
            case_control = loadgroup(trait)
            value = [trait]
            value.extend(case_control)
            
            if(np.any(np.array(case_control) < 10)):
                value.append('N')
            else:
                value.append('Y')
            
            d.loc[i] = value
            
    d.to_csv(os.path.join(folder, "b_remove_error_user.csv"))
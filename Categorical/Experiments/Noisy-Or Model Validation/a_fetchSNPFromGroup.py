import json
import glob
from collections import defaultdict
import pandas
import re
import util
import config
import sys
import os

#----Common variables----#
# folder = "C:\\__PQP\\RA materials\\opensnp\\"
# subfolder = "All Trait_New\\"
# tagfolder = "tags\\"
# groupfolder = "groups\\"
# rawsnpfolder = "allsnps\\"

if __name__ == "__main__":
    if len(sys.argv) <= 0:
        print "Please provide the folder of the ErrorUsers."
        exit(1)

    folder = sys.argv[1]

    if not os.path.exists(folder):
        print "The folder doesn't exist!"
        exit(1)

    ## Genetic testing files from OpenSNP should be put on folder "openSNP"
    ## In this repository, I only copy few files as examples
    filePath = os.path.join(folder, config.Folder_Attributes["raw"])
    if not os.path.exists(filePath):
        print "The raw genetic testing results from OpenSNP do not exist! Please visit OpenSNP to download before running."
        exit(1)

    ## File "Categorical_Type" lists all the variables of Phnotypes in OpenSNP
    ## Manually define these variables as categorical or numerical
    filePath = os.path.join(folder, "Categorical_Type.csv")
    if not os.path.exists(filePath):
        print "The path to the Categorical_Type doesn't exist!"
        exit(1)

    category = pandas.read_csv(filePath)

    if not os.path.exists(os.path.join(folder, config.Folder_Attributes["SNP"])):
        os.mkdir(os.path.join(folder, config.Folder_Attributes["SNP"]))

    def savetodt(dt, rsid, alleles, group):
        '''
        dt: a dict with the structure for a trait
            dt{
                <rsid>:{   
                    Alleles:{
                        <allele>:[# in control group, # in case group],
                        <allele>:[# in control group, # in case group]
                        ...
                        }
                    }
                }
        rsid: the SNP indetifier
        alleles: the alleles found from the genetic results of this rsid, usually from set {A, T, C, G}
        group: 0 -> control, 1 -> case
        '''

        # allele '-' or '0' is invalid
        exception = ['-', '0']

        if(not dt.has_key(rsid)):
            dt[rsid] = {}
        if(not dt[rsid].has_key("Alleles")):
            dt[rsid]["Alleles"] = {}

        for allele in alleles:
            if(allele in exception):
                continue
            if(not dt[rsid]["Alleles"].has_key(allele)):
                dt[rsid]["Alleles"][allele] = [0,0]
                dt[rsid]["Alleles"][allele][group] = 1
            else:
                value = dt[rsid]["Alleles"][allele][group]
                dt[rsid]["Alleles"][allele][group] = value + 1


    def save_to_error_user(userid):
        if(userid not in error_user):
            error_user.append(userid)


    def operatefile(dt, userid, group):
        '''
        processing files of each user to a dict data structure.
        * Only support the genetic results from 23andme, ftdna-illumina, and ancestry
        * if the test result is from other sources, this user id will be defined as error users
        dt: a dict with the structure for a trait
            dt{
                <rsid>:{   
                    Alleles:{
                        <allele>:[# in control group, # in case group],
                        <allele>:[# in control group, # in case group]
                        ...
                        }
                    }
                }
        userid: the id of users in OpenSNP 
        group: 0 -> control, 1 -> case           
        '''
        filename = "user" + str(userid) + "_*.txt"
        files = glob.glob(folder + filename)

        has_operated = False

        for singlefile in files:
            if(not has_operated):
                index = singlefile.index('.')
                filetype = singlefile[index+1:-4]

                if(filetype == "23andme"):
                    with open(singlefile,'r') as f:
                        try:
                            for line in f:
                                if(not line.startswith('#') and not line.lower().startswith('rsid')):
                                    items = line.strip().split('\t')
                                    rsid = unicode(items[0],errors='ignore')
                                    alleles = unicode(items[3],errors='ignore')
                                    if(rsid.strip() != ""):
                                        savetodt(dt, rsid,alleles,group)
                            has_operated = True
                        except Exception,e:
                            save_to_error_user(userid)
                            print str(userid), str(e)

                elif(filetype == "ftdna-illumina"):
                    with open(singlefile, 'r') as f:
                        try:
                            for line in f:
                                if(line.startswith('"')):
                                    items = line.replace('"','').strip().split(',')
                                    rsid = unicode(items[0], errors='ignore')
                                    alleles = unicode(items[3], errors='ignore')
                                    if (rsid.strip() != ""):
                                        savetodt(dt, rsid, alleles, group)
                            has_operated = True
                        except Exception, e:
                            save_to_error_user(userid)
                            print str(userid), str(e)
                elif (filetype == "ancestry"):
                    with open(singlefile,'r') as f:
                        try:
                            for line in f:
                                if(not line.startswith('#') and not line.lower().startswith('rsid')):
                                    items = line.strip().split('\t')
                                    rsid = unicode(items[0], errors='ignore')
                                    if(len(items) == 5):
                                        alleles = unicode(items[3] + items[4], errors='ignore')
                                    else:
                                        alleles = unicode(items[3], errors='ignore')
                                    if (rsid.strip() != ""):
                                        savetodt(dt, rsid, alleles, group)
                            has_operated = True
                        except Exception,e:
                            save_to_error_user(userid)
                            print str(userid), str(e)

        if(not has_operated):
            save_to_error_user(userid)




    def processgroup(trait):
        '''
        For each trait, extract raw SNP from each genetic test results for each user in both case and control groups  
        * for each trait, the user IDs of each group are saved as a txt file with trait name under subfolder "groups"
        * after processing, the alleles of each SNP is saved as a dict data structure with trait name under subfolder "SNP"
        '''
        filename = util.remove_invalid_filename(trait + ".txt" )

        with open(os.path.join(folder, config.Folder_Attributes["group"], filename),'r') as df:
            group = json.load(df)

        case = group["Case"]
        control = group["Control"]

        dt = defaultdict(defaultdict)

        if (case is not None):
            for i in case:
                operatefile(dt, i, 0)

        if (control is not None):
            for i in control:
                operatefile(dt, i, 1)

        with open(os.path.join(folder, config.Folder_Attributes["SNP"], filename), 'w') as outfile:
            json.dump(dt, outfile)


    # ----  for the whole traits  ----

    error_user = []
    for i, item in category.iterrows():
        v = item["Is Categorize Trait"]
        if(v == 'Y'):
            trait = item["Traits"]
            processgroup(trait)

    with open(os.path.join(folder, "ErrorUsers.txt"),'w') as df:
        json.dump(error_user, df)
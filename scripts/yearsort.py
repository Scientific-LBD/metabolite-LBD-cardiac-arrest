import gzip
import os
import re
import json

from alive_progress import alive_bar

mmo_path = "../../../data/baseline_mmo"
xml_path = "../../../data/baseline_xml"
yearsorted_path = "../../../data/baseline_yearsorted/"
json_path = "../../../data/baseline_yeardict.json"

year_dict = {}

if os.path.exists(json_path):
    with open(json_path, 'r') as j:
        year_dict = json.load(j)
else:
    print("Beginning year collection...")
    pattern = re.compile(r"<PubmedArticle>[\s\S]*?<PMID Version=\"\d\">([\d]*)</PMID>[\s\S]*?<PubDate>[\s\S]*?<Year>([\d]*)</Year>")
    with alive_bar(len(os.listdir(xml_path)), bar = 'smooth', spinner = 'classic') as bar:
        for filename in os.listdir(xml_path):
            with gzip.open(os.path.join(xml_path, filename)) as f:
                #print("Reading " + filename + "...")
                for match in  re.finditer(pattern, f.read().decode('utf-8')):
                    pmid = match.group(1)
                    year = match.group(2)
                    try:
                        year_dict[pmid] = str(year)
                    except:
                        year_dict[pmid] = "-1"
                #print("Successfuly read " + filename + ".")
                bar()
    print("Successfully completed year collection.\n")
    with open(json_path, 'w') as j:
        json.dump(year_dict, j)

print("Beginning year sort...")
pattern = re.compile(r"[\s\S]*?(utterance\('([\d]*).[\s\S]*?'EOU'.)")
with alive_bar(len(os.listdir(mmo_path)), bar = 'smooth', spinner = 'classic') as bar:
    for filename in os.listdir(mmo_path):
        #print("Sorting " + filename + "...")
        with gzip.open(os.path.join(mmo_path, filename), 'r') as f:
            for match in re.finditer(pattern, f.read().decode('utf-8')):
                pmid = match.group(2)
                try:
                    yearfilename = yearsorted_path + year_dict[pmid] + ".txt.MMO"
                except:
                    yearfilename = yearsorted_path + "-1.txt.MMO"
                if os.path.exists(yearfilename):
                    yearfile = open(yearfilename, 'a')
                    yearfile.write(match.group(1) + "\n")
                else:
                    yearfile = open(yearfilename, 'w')
                    yearfile.write(match.group(1) + "\n")
                yearfile.close()
        bar()
    #print("Successfully sorted " + filename + ".")
print("Successfully completed year sort.\n")
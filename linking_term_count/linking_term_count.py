import argparse
import os
import sys

def main():
    #parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a-terms', '-a', type=str, default="a_terms.txt", help="path to a text file containing a list of a-terms")
    parser.add_argument('-b-terms', '-b', type=str, default="b_terms.txt", help="path to a text file containing a list of b-terms")
    parser.add_argument('-co-occurrences', '-c', type=str, default="co_occurrence_counts.txt", help="path to a text file containing a list of co-occurrences")
    args = parser.parse_args()

    #gather a-terms and b-terms
    a_terms = open(args.a_terms, 'r').read().splitlines()
    b_terms = open(args.b_terms, 'r').read().splitlines()

    #gather co_occurrence_counts
    unique_cuis = set()
    abc_dict = {}
    with open(args.co_occurrences) as f:
        for line in f:
            term_1, term_2, count = line.strip().split('\t')
            count = int(count)
            unique_cuis.add(term_1)
            unique_cuis.add(term_2)
            #a b count
            if term_1 in a_terms:
                if term_2 in b_terms:
                    if term_1 not in abc_dict:
                        abc_dict[term_1] = {}
                    if term_2 not in abc_dict[term_1]:
                        abc_dict[term_1][term_2] = {}
            #b a count
            if term_1 in b_terms:
                if term_2 in a_terms:
                    if term_2 not in abc_dict:
                        abc_dict[term_2] = {}
                    if term_1 not in abc_dict[term_2]:
                        abc_dict[term_2][term_1] = {}
        #b c count
        f.seek(0)
        for line in f:
            term_1, term_2, count = line.strip().split('\t')
            count = int(count)
            if term_1 in b_terms:
                for a_term in abc_dict:
                    if term_1 in abc_dict[a_term]:
                        if term_2 in abc_dict[a_term][term_1]:
                            abc_dict[a_term][term_1][term_2] += count
                        else:
                            abc_dict[a_term][term_1][term_2] = count
        #c b count
        f.seek(0)
        for line in f:
            term_1, term_2, count = line.strip().split('\t')
            count = int(count)
            if term_2 in b_terms:
                for a_term in abc_dict:
                    if term_2 in abc_dict[a_term]:
                        if term_1 in abc_dict[a_term][term_2]:
                            abc_dict[a_term][term_2][term_1] += count
                        else:
                            abc_dict[a_term][term_2][term_1] = count

    #determine linking term count
    linking_term_counts = {}
    for c_term in unique_cuis:
        linking_term_counts[c_term] = 0
        for a_term in abc_dict:
            for b_term in abc_dict[a_term]:
                if c_term in abc_dict[a_term][b_term]:
                    linking_term_counts[c_term] += 1

    #filter by semantic type
    filtered_unique_cuis = set()
    with open("./MRSTY.RRF", "r") as f:
        for line in f:
            splitline = line.split("|")
            if splitline[0] in unique_cuis and splitline[1] == "T047":
                filtered_unique_cuis.add(splitline[0])

    #gather concept names
    concept_names = {}
    with open("./MRCONSO.RRF", "r") as f:
        for line in f:
            splitline = line.split("|")
            if splitline[0] in unique_cuis and splitline[1] == "ENG" and splitline[2] == "P":
                concept_names[splitline[0]] = splitline[14]
    for unique_cui in unique_cuis:
        if unique_cui not in concept_names:
            concept_names[unique_cui] = "Unidentified"

    #debugging
    #a_term = "C0018790"
    #b_term = "C0003765"
    #c_term = "C0018790"    
    #print(abc_dict[a_term][b_term][c_term])
    #print(linking_term_counts[c_term])



    #format output
    output = ""
    for a_term in abc_dict:
        output += a_term + " - " + concept_names[a_term] + "\n"
        for c_term, value in sorted(linking_term_counts.items(), key=lambda item: item[1], reverse=True):
            if c_term in filtered_unique_cuis:
                output += "\t" + str(value) + " - " + c_term + " - " + concept_names[c_term] + "\n"
                b_term_scores = {}
                for b_term in abc_dict[a_term]:
                    if c_term in abc_dict[a_term][b_term]:
                        b_term_scores[b_term] = abc_dict[a_term][b_term][c_term]
                for b_term, b_value in sorted(b_term_scores.items(), key=lambda item: item[1], reverse=True):
                    output += "\t\t" + str(b_value) + " - " + b_term + " - " + concept_names[b_term] + "\n"

    with open("output.txt", "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
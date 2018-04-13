import sys, os

sys.path.append('/Users/sachingb/Development/USC/CSCI_599/Assignments/HW2/UFO_ocr_image-captioning_enrichment/MITIE-master/mitielib')

from mitie import *
from collections import defaultdict

UFO_FILES_DIR = ['DEFE-24-1922','DEFE-24-1923','DEFE-24-1924', 'DEFE-24-1925', 'DEFE-31-172', 'DEFE-31-173','DEFE-31-174', 'DEFE-31-175']

OUTPUTDIR = 'MITIE_UFO/'

print("loading NER model...")
ner = named_entity_extractor('../MITIE-master/MITIE-models/english/ner_model.dat')
print("\nTags output by this NER model:", ner.get_possible_ner_tags())


for input_dir in UFO_FILES_DIR:
    for files in os.listdir(input_dir+"/outtxt/"):
        print "File name is ", files
        tokens = tokenize(load_entire_file(input_dir+"/outtxt/"+files))
        # print("Tokenized input:", tokens)
        entities = ner.extract_entities(tokens)
        # print("\nEntities found:", entities)
        # print("\nNumber of entities detected:", len(entities))
        cwd = OUTPUTDIR+input_dir+"/"
        if not os.path.exists(cwd):
            os.makedirs(cwd)
        f = open(cwd+files, 'w')
        for e in entities:
            range = e[0]
            tag = e[1]
            score = e[2]
            score_text = "{:0.3f}".format(score)
            try:
                entity_text = " ".join(tokens[i].decode() for i in range)
            except:
                entity_text = "NON Ascii text"
            f.write("   Score: " + score_text + ": " + tag + ": " + entity_text + "\n")
            # print("   Score: " + score_text + ": " + tag + ": " + entity_text)
        f.close()

# Load a text file and convert it into a list of words.
# tokens = tokenize(load_entire_file('../../sample_text.txt'))
# print("Tokenized input:", tokens)
#
# entities = ner.extract_entities(tokens)
# print("\nEntities found:", entities)
# print("\nNumber of entities detected:", len(entities))

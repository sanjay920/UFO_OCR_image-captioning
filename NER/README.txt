Requires: pip install dateparser

Download CoreNLP: https://stanfordnlp.github.io/CoreNLP/index.html#download

Start CoreNLP client: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000


1) Run cells in CoreNLP_notebook to produce pdfs_with_ner.csv -- this CSV will have each PDF page from british UFO files as a row. This notebook also saves the named entities from the text of each sighting as a dict to NER_dict.pickle and the resultant dataframe to pdfs_with_ner.pickle

2) Run reportedSighted_at notebook -- reads in {TIME_OF_CREATION}_df.pickle and goes through each row and its named entities to find a reported_at and sighted_at. Since sighted_at always is before reported_at, we look for at max 2 dates in the NEs and assign them accordingly. This will produce PDFs_reported_sighted_at.csv and a pickle that contains that DF in PDFs_reported_sighted_at.pickle

3) Run description_field notebook. This will take in PDFs_reported_sighted_at.csv and add a description field (if any found) for each UFO sighting. This notebook will output PDFs_description.csv

4) Run duration_field notebook. This will take in PDFs_description.csv and add a duration field if found in the named entities found in text. 

5) Run combine_PDF_with_images notebook. This will merge PDFs (from PDFs_description.csv) with images. Although the intermediary files contain images data, it doesnt include some important fields (location, etc.) so we read in the images from 'captions_classes_with_summary.csv'


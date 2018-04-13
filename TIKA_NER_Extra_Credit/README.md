**Exploring TIKA NER on the data set**
 Here we ran our output txt files from the ocr pipline on CoreNLP, OpenNLP and MITIE NLP packages and recorded the results.

 Input folders :
 british-ufo-files from the previous directory

Output folders :
1) CoreNLP_OUTPUT : This folder contains the results (NER Tagging) for all the ocr texts running Stanford Core NLP jar.

2) OpenNLP_OUTPUT : This folder contains the results (NER Tagging) for all ocr texts after running Stanford OPEN NLP jar.

3) MITIE_OUTPUT : This folder contains the results (NER Tagging) for all ocr texts after running MITIE.

Requirements and pre requisites

1) Make sure that we have the OpenNLP Target folder added to the path $NER_RES, details are explained in the link below.

https://wiki.apache.org/tika/TikaAndNER

2) Before running Core_NLP make sure we have the required jar ready and added to the path $CORE_NLP_JAR, details are explained in the link below

https://wiki.apache.org/tika/TikaAndNER

3) To run MITIE make sure we have the libraries are present. Follow the below link.

https://github.com/mit-nlp/MITIE

Run

Once we have this ready. Run

1) ner_extraction.sh to get Core NLP and Open NLP outputs. Details are within the script

2) ner_mitie.py to get MITIE results

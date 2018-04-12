Tika vision

1) Need python3 and pip3 to run this part

2) Create a virtual env 'hw2Vision' in this directory   
	virtualenv hw2Vision

3) Next activate the virtual environment by running the below commands:   
	source virtualenv hw2Vision/bin/activate

4) Next install the necessary packages using pip3

	pip3 install -U requirements.txt

5) In another terminal make sure that tika vision and caption dockers are running and the endpoints are accessible

Step 1: First extract the classes for each url and write it into a csv.   

Columns - Classes, URL, Case_ID   

1) To achieve this execute async_test.py in the terminal with python 3   
2) Some of the requests to the TIKA vision API may time out. In that case we make note of that and try to extract the details in the next run   
3) Once the script runs, it creates a csv named "data_set_v2_with_classes.csv"
4) Re-run async_test.py to get urls which failed in the previous run   
5) Once this is done, we will have the classes for all the urls passed   


Step 2: Secondly we need to extract captions for each url and write it into a new csv.

Columns - URL, Caption

1) Make sure Tika caption docker is up and running in a terminal window, ensure that we have access to the endpoint

2) From the previous step, we have a list of all the urls that were processed. These are stored in the file "all_url.txt"

3) For each url in this, we try to find the captions using tika caption API.

4) Once the script runs completely, we will have a csv "data_set_v2_with_caption.csv"

5) Once this is done, we will have the caption for all the urls passed

Step 3:

Once we have these files going through step1 and step2, we can merge these into single csv by running merge_data_sets.py   

merge_data_sets.py merges the two files as pandas dataframes and we merge them based on the common column "URL"

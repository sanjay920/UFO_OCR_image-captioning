import pandas as pd

#Reading the two csv files as pandas dataframes
captions_data = pd.read_csv('data_set_v2_with_caption.csv', encoding='ISO-8859-1')
classes_data = pd.read_csv('data_set_v2_with_classes.csv', encoding='ISO-8859-1')

#Removing duplicate URLs and captions
captions_url = set(captions_data['URL'].tolist())
classes_url = set(classes_data['URL'].tolist())

#Find URLs which are there in both sets
intersect = classes_url.intersection(captions_url)

print(len(intersect))

#Merge the two files based on the common column "URL"
merged_data_frame = pd.merge(captions_data, classes_data, on="URL")
merged_data_frame.to_csv("captions_and_classes.csv", encoding='ISO-8859-1')

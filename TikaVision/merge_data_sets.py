import pandas as pd

captions_data = pd.read_csv('data_set_v2_with_caption.csv', encoding='ISO-8859-1')
classes_data = pd.read_csv('data_set_v2_with_classes.csv', encoding='ISO-8859-1')

captions_url = set(captions_data['URL'].tolist())
classes_url = set(classes_data['URL'].tolist())

intersect = classes_url.intersection(captions_url)

print(len(intersect))

merged_data_frame = pd.merge(captions_data, classes_data, on="URL")
#
merged_data_frame.to_csv("captions_and_classes.csv", encoding='ISO-8859-1')

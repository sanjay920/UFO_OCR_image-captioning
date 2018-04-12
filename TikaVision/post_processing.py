import json
import os
import pandas as pd
import ast

CAPTIONS_CLASSES = "captions_and_classes.csv"

df_captions = pd.read_csv(CAPTIONS_CLASSES, encoding='ISO-8859-1')
classes = df_captions['Class'].tolist()

df_captions['Class_1'] = ""
df_captions['Class_2'] = ""
df_captions['Class_3'] = ""
df_captions['Class_4'] = ""
df_captions['Class_5'] = ""
df_captions['Class_6'] = ""
df_captions['Class_7'] = ""

for index, row in df_captions.iterrows():
    classes = ast.literal_eval(row['Class'])
    classes = classes[0].split(',')

    for i in range(1, 8):
        class_name = 'Class_'+str(i)
        # print("Class length ", len(classes[0].split(',')))
        if i <= len(classes):
            df_captions.loc[index, class_name] = classes[i-1]
        else:
            df_captions.loc[index, class_name] = "NA"

df_captions.to_csv('ufo_vision_caption_v2.csv', index=False, encoding='ISO-8859-1')

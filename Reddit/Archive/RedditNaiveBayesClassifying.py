import pandas as pd
import json

def write_file(data):
    with open(out_path,"w") as out_file:
        json.dump(data,out_file)
    print("Saved\nExiting Application")


file_paths = ["RedditJan2020_July2020.csv","Reddit2019.csv","Reddit2018to2015.csv","Reddit2015andBefore.csv"]

data_list = []

keyword = input("Enter keyword: ")

keywords = keyword.split(" ")

for path in file_paths:
    dataframe = pd.read_csv(path, index_col = False)

    title_list = dataframe["title"].tolist()

    for title in title_list:
        for keyword in keywords:
            if keyword == keywords[-1] and keyword in title.lower():
                data_list.append(title.lower())
            elif keyword not in title.lower():
                break
            
    for comment in dataframe["comments"].tolist():
        if type(comment) != float :
            comment_list = comment.split("\n\n")[:-1]
            for el in comment_list:

                for keyword in keywords:
                    if keyword == keywords[-1] and keyword in el.lower():
                        data_list.append(el.lower())
                    elif keyword not in el.lower():
                        break


print("Total Number of Posts & Comments Containing", " ".join(keywords),len(data_list))

if len(data_list) == 0:
    exit()

print("\nBegin Classifying Text ...")

data_to_classify = data_list[:int(len(data_list)*0.5)]

out_path = " ".join(keywords)+"TrainingSet.json"

classified_list = []
count = 1
try:
    for data in data_to_classify:
        print("\nClassifying {} out of {}".format(count,len(data_to_classify)))
        print("Data:",data)
        category = input("\n Enter pos or neg or skip if repeated: ")

        while category not in ["pos","neg","skip"]:
            print("Please Enter pos or neg or skip only")
            category = input("\n Enter pos or neg or skip: ")
        
        if category != "skip":
            classified_list.append({"text":data,"label":category})
        count += 1
except:
    print("Exception caught. \nSaving results to file")
    write_file(classified_list)
    exit()

write_file(classified_list)

import os
import json
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer

file_list = []
file_end = input(".txt or .json?   ")


for file in os.listdir("C:\\Users\yihao\\Google Drive\\Sem 2.5\\IS434 Social Analytics and Applications\\Project\\#blacklivesmatter"):
    if file.endswith(file_end):
        file_list.append(os.path.join("C:\\Users\\yihao\\Google Drive\\Sem 2.5\\IS434 Social Analytics and Applications\\Project\\#blacklivesmatter",file))

# print(file_list)
data_list = []
count = 1
tokenizer = RegexpTokenizer(r'\w+')
if file_end == ".txt":
    
    for element in file_list:
        with open(element, "r", encoding ="UTF-8") as in_file:
            try:
                toAppend = ""
                for line in in_file:
                    line = line.rstrip("\n")
                    toAppend += line
                
                toAppend = tokenizer.tokenize(toAppend)
                data_list.append(" ".join(toAppend))
                print("File Read: ", count)
                count += 1
            except:
                print(count, "failed")
                count += 1
    
    with open("BlackLivesMatter_InstagramPosts.json", "w", encoding = "UTF-8") as out_file:
        print("Writing to file ...")
        json.dump(data_list, out_file, indent=4)



def checkAnswers(toCheck):
    if toCheck == []:
        return ""
    else:
        print ("More Comments Found")
        toReturn = []
        for obj in toCheck:
            toAppend = tokenizer.tokenize(obj['text'])
            toAppend = " ".join(toAppend)
            if toAppend != "":
                toReturn.append(toAppend)
        return toReturn

if file_end == ".json":

    for element in file_list:
        with open(element, "r", encoding = "UTF-8") as json_file:
            data = json.load(json_file)
            for obj in data:
                print ("Reading file:",count)
                toAppend = tokenizer.tokenize(obj['text'])
                toAppend = " ".join(toAppend)
                if toAppend != "":
                    data_list.append(toAppend)
                
                moreComments = checkAnswers(obj['answers'])
                data_list += moreComments
                count += 1
        
    with open("BlackLivesMatter_InstagramComments.json", "w", encoding = "UTF-8") as out_file:
        print("Writing to file ...")
        json.dump(data_list, out_file, indent=4)
                    



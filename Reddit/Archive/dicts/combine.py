import yaml
negative_in_path = "./Reddit/dicts/negative.txt"
negative_out_path = "./Reddit/dicts/negative.yml"

positive_in_path = "./Reddit/dicts/positive.txt"
positive_out_path = "./Reddit/dicts/positive.yml"

count = 0
positive_dict = {}
with open(positive_in_path, "r") as in_file:
    for line in in_file:
        line = line.rstrip("\n")
        positive_dict[line] = ["positive"]
        count+=1
        print("Positive Lines wrote",count)

with open(positive_out_path,"w") as out_file:
    yaml.dump(positive_dict,out_file)
    print("done")


count = 0
negative_dict = {}
with open(negative_in_path, "r") as in_file:

    for line in in_file:
        line = line.rstrip("\n")
        negative_dict[line] = ["negative"]
        count+=1
        print("Negative Lines wrote",count)


    with open(negative_out_path, "w") as out_file:
        yaml.dump(negative_dict,out_file)
        print("done")
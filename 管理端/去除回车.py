
def removeSpace(string):
    for i in range(9999):
        string = string.replace("  "," ")
    return string

with open("1.txt","r",encoding="utf-8") as f:
    with open("2.txt","w",encoding="utf-8") as m:
        m.write(removeSpace(f.read().replace("\n","").replace('\t',"")))

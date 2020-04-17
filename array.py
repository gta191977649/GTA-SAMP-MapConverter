f = open("array.txt","r")
array = f.readlines()

out = []
idx = 0
for line in array:
    if line != '\n':
        if (idx == 3):
            idx = 1
        else:
            idx = idx +1
        tk = line.split("=")

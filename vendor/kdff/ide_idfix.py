path = "C:/Users/nurupo/Desktop/a.txt"

f = open(path)
ide = f.readlines()
id = 10567
for item in ide:
    tk = item.split(",")
    print("{},{},{},{},{},{},{}".format(id,tk[1],tk[2],tk[3],tk[4],tk[5],tk[6]).strip())
    id = id+1
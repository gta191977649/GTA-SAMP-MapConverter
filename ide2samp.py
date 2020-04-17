
#AddSimpleModel(-1, 19379, -3001, "vc4samp/fbi_logo_large.dff", "vc4samp/fbi_logo.txd");
#(virtualworld, baseid, newid, dffname[], txdname[])

#AddSimpleModelTimed
#(virtualworld, baseid, newid, dffname[], txdname[], timeon, timeoff)


#The new object model ID ranged from -1000 to -30000 (29000 slots) to be used later with CreateObject or CreatePlayerObject.

import math
import os
import subprocess


pathPrefix = 'vcs2samp/'
worldid = 696968
basemodel = 19379

id_start = 1000
start = id_start
VICECITY_MOVE_X = 5000
VICECITY_MOVE_Z = -5


output_modelDef = ""
output_enex = ""
ideTable = []

def findIdFromIdeTable(modelname):
    for item in ideTable:
        if item["model"] == modelname:
            return item["id"]
    return -1
def findDrawDistanceFromIdeTable(modelname):
    for item in ideTable:
        if item["model"] == modelname:
            return item["drawdistance"]
    return -1

#四元数转欧拉角
def quaternionToYawPitchRoll(modelname,quat_w,quat_x,quat_y,quat_z):
    quat_w = round(quat_w,6)
    quat_x = round(quat_x, 6)
    quat_y = round(quat_y, 6)
    quat_z = round(quat_z, 6)
    asin =  2 * ((quat_x * quat_z) + (quat_w * quat_y))
    if asin > 1:
        print("recap on model:{} asin value = {} > 1".format(modelname,2 * ((quat_x * quat_z) + (quat_w * quat_y))))
        asin = 1
    elif asin < -1:
        print("recap on model:{} asin value = {} < 1".format(modelname, 2 * ((quat_x * quat_z) + (quat_w * quat_y))))
        asin = -1

    rx = -math.asin(asin)  * 180 / math.pi;
    ry = math.atan2(2 * ((quat_y * quat_z) + (quat_w * quat_x)),(quat_w * quat_w) - (quat_x * quat_x) - (quat_y * quat_y) + (quat_z * quat_z)) * 180 / math.pi;
    rz = -math.atan2(2 * ((quat_x * quat_y) + (quat_w * quat_z)),(quat_w * quat_w) + (quat_x * quat_x) - (quat_y * quat_y) - (quat_z * quat_z)) * 180 / math.pi;
    return (rx,ry,rz)

def CompressRotation(rotation):
	return rotation - math.floor(rotation/360.0)*360.0

def quaternionToYawPitchRoll2(modelname,qw,qx,qy,qz):
    asin = 2 * qy * qz - 2 * qx * qw
    if asin > 1:
        #print("recap on model:{} asin value = {} > 1".format(modelname,asin))
        asin = 1
    elif asin < -1:
        #print("recap on model:{} asin value = {} < 1".format(modelname, asin))
        asin = -1

    rx = CompressRotation(math.asin(asin)  * 180 / math.pi );
    ry = CompressRotation(-math.atan2(qx*qz+qy*qw,0.5-qx*qx-qy*qy) * 180 / math.pi);
    rz = CompressRotation(-math.atan2(qx*qy+qz*qw,0.5-qx*qx-qz*qz)  * 180 / math.pi);
    return (round(rx,4),round(ry,4),round(rz,4))

def generateSimpleObjectCode(line):
    print(line)
    global id_start,output_modelDef
    #切分格式 ID, ModelName, TextureName, ObjectCount, DrawDist, [DrawDist2, ...], Flags
    token = line.split(',')
    modelid = token[0]
    dff = pathPrefix.strip()+"dff/"+token[1].strip().lower()
    #不要处理LOD
    if 'LOD' in dff:
        #print("Found lod on model {}, skip".format(dff))
        return
    if 'lod' in dff:
        #print("Found lod on model {}, skip".format(dff))
        return
    txd = pathPrefix.strip()+"txd/"+token[2].strip().lower()
    drawdistance = token[3]
    flags = token[4]
    ideTable.append({
        "model":token[1],
        "id":-id_start,
        "drawdistance":drawdistance
    })
    output_modelDef += "AddSimpleModel({}, {}, {}, \"{}.dff\", \"{}.txd\");".format(worldid,basemodel,-id_start,dff,txd)+"\n"
    id_start = id_start +1
    #print(id)

def generateTimedObjectCode(line):

    global id_start,output_modelDef
    #ID, ModelName, TextureName, ObjectCount, DrawDist, [DrawDist2, ...], Flags, TimeOn, TimeOff
    token = line.split(',')
    modelid = token[0].strip()
    dff = pathPrefix.strip()+"dff/"+token[1].strip().lower()
    txd = pathPrefix.strip()+"txd/"+token[2].strip().lower()
    drawdistance = token[3].strip()
    flags = token[4].strip()
    timeon = token[5].strip()
    timeoff = token[6].strip()
    #(virtualworld, baseid, newid, dffname[], txdname[], timeon, timeoff)
    ideTable.append({
        "model": token[1],
        "id": -id_start,
        "drawdistance": drawdistance
    })
    output_modelDef += "AddSimpleModelTimed({}, {}, {}, \"{}.dff\", \"{}.txd\",{},{});".format(worldid,basemodel,-id_start,dff,txd,timeon,timeoff)+"\n"
    id_start = id_start +1

def generateSAMPObjFromIpl(line,int=0):
    global output_modelDef
    token = line.split(",")
    id = token[0]
    modelName = token[1]

    if 'LOD' in modelName: return
    if 'lod' in modelName: return
    #print(modelName)
    #int = token[2]
    x = token[3]
    y = token[4]
    z = token[5]
    qx = float(token[6])
    qy = float(token[7])
    qz = float(token[8])
    qw = float(token[9])
    #转换四元数到欧拉坐标系
    #print(qx,qy,qz,qw)
    modelid = findIdFromIdeTable(modelName)
    if modelid != -1:
        rx, ry,rz = quaternionToYawPitchRoll2(modelName,qw,qx,qy,qz)
        dw = findDrawDistanceFromIdeTable(modelName)
        output_modelDef += "CreateDynamicObject({},{},{},{},{},{},{},{},{},{},{},{});\n".format(modelid,float(x)+VICECITY_MOVE_X,y,float(z)+VICECITY_MOVE_Z,rx,ry,rz,worldid,int,-1,1000,1000)
    #CreateDynamicObject(modelid, Float:x, Float:y, Float:z, Float:rx, Float:ry, Float:rz, worldid = -1, interiorid = -1, playerid = -1, Float:streamdistance = STREAMER_OBJECT_SD, Float:drawdistance = STREAMER_OBJECT_DD, areaid = -1, priority = 0)
    #output_modelDef+= "CreateDynamicObject({},{},{},{},{},{},{})".format()

def parseIde(pathIde):
    paseObjChunk = False
    f = open(pathIde, "r")
    ide = f.readlines()
    mode = ""
    print(pathIde)
    #处理IDE
    for line in ide:
        #处理普通OBJ
        if line == '\n': continue
        if "#" in line: continue
        if line == "path\n" or line == "path": continue
        if line == "end\n" or line == "end":
            paseObjChunk = False
            continue

        if line == "objs\n":
            paseObjChunk = True
            mode = "objs"
            continue
            #print("Find normal object chunk")

        #处理夜晚OBJ
        if line == "tobj\n":
            paseObjChunk = True
            mode = "tobj"
            continue
            #print("Find timed object chunk")


        if paseObjChunk:

            if mode == "objs":
                generateSimpleObjectCode(line)
            if mode == "tobj":
                generateTimedObjectCode(line)


def generateEnexObjFromIpl(line):
    global output_enex
    #enex_array[ints][enx],enex_array[ints][eny],enex_array[ints][enz],enex_array[ints][exx],enex_array[ints][exy],enex_array[ints][exz],enex_array[ints][exa],enex_array[ints][exi],enex_array[ints][lead],enex_array[ints][rname]
    tk = line.split(",")
    x1 = float(tk[0].strip())
    y1 = tk[1].strip()
    z1 = tk[2].strip()
    enter_a = tk[3].strip()
    sx = tk[4].strip()
    sy = tk[5].strip()
    sz = tk[6].strip()
    x2 = tk[7].strip()
    y2 = tk[8].strip()
    z2 = tk[9].strip()
    exit_a = tk[10].strip()
    interior = int(tk[11].strip())
    flags = tk[12].strip()
    name = tk[13].strip()
    weather = tk[14].strip()

    #round numbers
    x1 = round(float(x1),3) + VICECITY_MOVE_X
    y1 = round(float(y1),3)
    z1 = round(float(z1),2) + VICECITY_MOVE_Z + 1
    x2 = round(float(x2),3) + VICECITY_MOVE_X
    y2 = round(float(y2),3)
    z2 = round(float(z2),3) + VICECITY_MOVE_Z + 1

    #SA-MP FIX
    flags = 0
    if interior > 0:
        interior = 5
        flags = 1

    output_enex += "{} {} {} {} {} {} {} {} {} {}\n".format(x1,y1,z1,x2,y2,z2,enter_a,interior,flags,name)
#处理IPL
def parseIpl(pathIpl):
    global output_modelDef,output_enex
    paseObjChunk = False
    f = open(pathIpl, "r")
    ipl = f.readlines()
    mode = ""
    for line in ipl:
        if line == '\n': continue
        if "#" in line: continue
        if line == "end\n" or line == "end":
            paseObjChunk = False
            continue

        if "inst" in line:
            output_modelDef += "//"+pathIpl+"\n"
            paseObjChunk = True
            mode = "inst"
            continue
        if "enex" in line:
            #output_enex += "// " + pathIpl + "\n"
            paseObjChunk = True
            mode = "enex"
            continue
        if paseObjChunk:
            if mode == "inst":
                if "shops.IPL" in pathIpl or  "stadium.IPL"  in pathIpl or "int.IPL" in pathIpl:
                    generateSAMPObjFromIpl(line,5)
                else:
                    generateSAMPObjFromIpl(line, 0)
            if mode == "enex":
                generateEnexObjFromIpl(line)


def extractIMG(imgpath,modelexportPath):
    PATH_KDFF = os.path.join('./vendor/img/fastman92ImgConsole32.exe')
    subprocess.call(PATH_KDFF+" -open \"{}\" -extractall \"{}\"".format(imgpath.strip(),modelexportPath))


#parseIde(pathIde)
#parseIpl(pathIpl)

def main():
    #parseIde("D:/jmmaps/vcs2samp/vcs_map/oceandrv/oceandrv.IDE") #error on model od_clevelander_dy


    gta_dat_dir = "D:/jmmaps/vcs2samp/vcs_map/"
    modelexportPath = "D:/jmmaps/vcs2samp/img/"


    f = open(gta_dat_dir+"gta_bak.dat","r")
    gtadat = f.readlines()

    #读取SA模型定义文件
    for item in gtadat:
        if "#" in item: continue
        """
        if "IMG" in item:
            token = item.split(" ")
            imgPath = token[1]
            extractIMG(imgPath,modelexportPath)
        """
        if "IDE" in item:
            token = item.split(" ")
            idePath = token[1]
            parseIde(gta_dat_dir+idePath.strip())

        if "IPL" in item:
            token = item.split(" ")
            iplPath = token[1]
            parseIpl(gta_dat_dir+iplPath.strip())


    f = open(gta_dat_dir+"map.txt", "w")
    f.write(output_modelDef)
    f.close()

    print("Convert Finish! {} Objects in totoal use slot from {} to {}".format(id_start-start,start,id_start))
    print(output_enex)
main()

#AddSimpleModel(-1, 19379, -3001, "vc4samp/fbi_logo_large.dff", "vc4samp/fbi_logo.txd");
#(virtualworld, baseid, newid, dffname[], txdname[])

#AddSimpleModelTimed
#(virtualworld, baseid, newid, dffname[], txdname[], timeon, timeoff)


#The new object model ID ranged from -1000 to -30000 (29000 slots) to be used later with CreateObject or CreatePlayerObject.
import math

pathPrefix = 'vcs2samp/'
pathIde = "D:/jmmaps/vcs2samp/stadium/stadium.IDE"
pathIpl = "D:/jmmaps/vcs2samp/stadium/stadium.IPL"
worldid = -1
basemodel = 19379

id_start = 1000



paseObjChunk = False

output_modelDef = ""
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
        print("recap on model:{} asin value = {} > 1".format(modelname,asin))
        asin = 1
    elif asin < -1:
        print("recap on model:{} asin value = {} < 1".format(modelname, asin))
        asin = -1

    rx = CompressRotation(math.asin(asin)  * 180 / math.pi );
    ry = CompressRotation(-math.atan2(qx*qz+qy*qw,0.5-qx*qx-qy*qy) * 180 / math.pi);
    rz = CompressRotation(-math.atan2(qx*qy+qz*qw,0.5-qx*qx-qz*qz)  * 180 / math.pi);
    return (round(rx,4),round(ry,4),round(rz,4))

def generateSimpleObjectCode(line):
    global id_start,output_modelDef
    #切分格式 ID, ModelName, TextureName, ObjectCount, DrawDist, [DrawDist2, ...], Flags
    token = line.split(',')
    modelid = token[0]
    dff = pathPrefix.strip()+token[1].strip()
    #不要处理LOD
    if 'LOD' in dff:
        print("Found lod on model {}, skip".format(dff))
        return

    txd = pathPrefix.strip()+token[2].strip()
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
    modelid = token[0]
    dff = pathPrefix.strip()+token[1].strip()
    txd = pathPrefix.strip()+token[2].strip()
    drawdistance = token[3]
    flags = token[4]
    timeon = token[5]
    timeoff = token[6]
    #(virtualworld, baseid, newid, dffname[], txdname[], timeon, timeoff)
    ideTable.append({
        "model": token[1],
        "id": -id_start,
        "drawdistance": drawdistance
    })
    output_modelDef += "AddSimpleModelTimed({}, {}, {}, \"{}.dff\", \"{}.txd\",{},{});".format(worldid,basemodel,-id_start,dff,txd,timeon,timeoff)+"\n"
    id_start = id_start +1

def generateSAMPObjFromIpl(line):
    global output_modelDef
    token = line.split(",")
    id = token[0]
    modelName = token[1]

    if 'LOD' in modelName: return
    print(modelName)
    int = token[2]
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
        output_modelDef += "CreateDynamicObject({},{},{},{},{},{},{},{},{},{},{});\n".format(modelid,x,y,z,rx,ry,rz,worldid,int,-1,dw)
    #CreateDynamicObject(modelid, Float:x, Float:y, Float:z, Float:rx, Float:ry, Float:rz, worldid = -1, interiorid = -1, playerid = -1, Float:streamdistance = STREAMER_OBJECT_SD, Float:drawdistance = STREAMER_OBJECT_DD, areaid = -1, priority = 0)
    #output_modelDef+= "CreateDynamicObject({},{},{},{},{},{},{})".format()


f = open(pathIde, "r")
ide = f.readlines()
mode = ""
#处理IDE
for line in ide:
    #处理普通OBJ
    if line == "objs\n":
        paseObjChunk = True
        mode = "objs"
        print("Find normal object chunk")
        continue
    if line == "tobj\n":
        paseObjChunk = True
        mode = "tobj"
        print("Find normal object chunk")
        continue

    if paseObjChunk:
        if line != "end\n":
            if mode == "objs":
                generateSimpleObjectCode(line)
            if mode == "tobj":
                generateTimedObjectCode(line)

        else:
            paseObjChunk = False


#处理IPL

f = open(pathIpl, "r")
ipl = f.readlines()
for line in ipl:
    if line == "inst\n":
        paseObjChunk = True
        continue
    if paseObjChunk:
        if line != "end\n":
            generateSAMPObjFromIpl(line)

        else:
            break

print(output_modelDef)
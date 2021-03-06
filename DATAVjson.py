import requests
import os
import _thread as thread
exitmutexes={}

def getjson(basedir,adcode):
    exitmutexes.update({adcode:False})
    #获取当前地图轮廓
    baseurl='https://geo.datav.aliyun.com/areas/bound/'+str(adcode)+'.json'
    fullurl='https://geo.datav.aliyun.com/areas/bound/'+str(adcode)+'_full.json'
    baser=requests.get(baseurl)
    if baser.status_code==200:
        curObjName=baser.json()['features'][0]['properties']['name']
        print(curObjName)
        curFileDir = os.path.join(basedir,curObjName)
        os.mkdir(curFileDir)
        basejsonfile=os.path.join(curFileDir,str(adcode)+'.json')
        with open(basejsonfile,'w') as file:
            file.write(baser.text)
    else:
        exitmutexes.update({adcode:True})
    #获取当前地图子地图轮廓
    fullr=requests.get(fullurl)
    print(fullurl)
    if fullr.status_code==200 and 'curObjName' in vars():
        fulljsonfile=os.path.join(curFileDir,str(adcode)+'_full.json')
        with open(fulljsonfile,'w') as file:
            file.write(fullr.text)
        for item in fullr.json()['features']:
            chadcode=item['properties']['adcode']
            if chadcode==adcode:
                pass
            else:
                thread.start_new_thread(getjson,(curFileDir,chadcode))
                exitmutexes.update({chadcode:False})
        exitmutexes.update({adcode:True})
    else:
        exitmutexes.update({adcode:True})

getjson('C:\\Users\\16943\\Desktop',100000)
print(exitmutexes)
while False in exitmutexes.values():pass
print('main thread exiting')
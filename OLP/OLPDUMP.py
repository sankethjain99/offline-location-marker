import sqlite3
import json
import codecs

cc = sqlite3.connect('geodata.sqlite')
cu = cc.cusor()

cu.execute('SELECT * FROM Locations')
fhand = codecs.open('where.js','w', "utf-8")
fhand.write("myData = [\n")
c = 0
for row in cu :
    data = str(row[1])
    try: js = json.loads(str(data))
    except: continue

    if not('status' in js and js['status'] == 'OK') : continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'","")
    try :
        print (where, lat, lng)

        c = c + 1
        if c > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cu.close()
fhand.close()
print (c, "records written to where.js")
print ("Open where.html to view the data in a browser")


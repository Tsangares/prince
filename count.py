"""
Basic test file, artificially increasing the local count file
 and uploading it to the ledger. 
This is because I do not have the cirucits to test the other script.
"""

import sys,os,json,subprocess,time
from datetime import datetime

countFile = 'count.json'

def getCount():
    if not os.path.isfile(countFile):
        return 0
    else:
        try:
            data = json.load(open(countFile))
            return int(data['count'])
        except IndexError:
            print("Error, the count file is corrupt. Resetting to zero.")
            return 0
    
def setCount(myCount,threshold=20):
    dateTime = datetime.now()
    template={
        'count': myCount,
        'time': str(dateTime)
    }
    #Update local file
    json.dump(template,open(countFile,'w+'))
    #print(open(countFile).read())
    #Upload to iota ledger
    if myCount != 0 and myCount%threshold == 0:
        uploadCount()
        template['count']=0
    #Update local file
    json.dump(template,open(countFile,'w+'))

def uploadCount():
    subprocess.run(['node', 'gateway.js'])

if __name__=="__main__":
    settings = json.load(open('settings.json'))
    threshold = settings['threshold']
    print(f'threshold is {threshold}')
    count = getCount()
    print(f'Count is {count}, increasing')
    setCount(count+1)
    print("Count set")
    

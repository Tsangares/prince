"""
Basic test file, artificially increasing the local count file
 and uploading it to the ledger. 
This is because I do not have the cirucits to test the other script.
"""

import sys,os,json,subprocess,time

countFile = 'count.txt'
def getCount():
    if not os.path.isfile(countFile):
        return 0
    else:
        try:
            countStr = open(countFile).read()
            if countStr==0: return 0
            return int(countStr.split(',')[1])
        except IndexError:
            print("Error, the count file is corrupt. Resetting to zero.")
            return 0
    
def setCount(myCount,threshold=20):
    #Upload to iota ledger
    if myCount%threshold == 0:
        uploadCount()
        myCount=0

    #Update local file
    if not os.path.isfile(countFile):
        open(countFile,'w+').write(f'{time.time()},0')
    open(countFile,'w+').write(f'{time.time()},{myCount}')
    return myCount

def uploadCount():
    subprocess.run(['node', 'gateway.js'])

if __name__=="__main__":
    count = getCount()
    print(f'Count is {count}, increasing')
    setCount(count+1)
    print("Count set")
    

import json, glob
import threading, sys, traceback


recordDir = ".\\Records\\"
recordTypes = ["testName", "stepCount", "result", "runTime"]
testRecords = []
activeAnalysers = []

def clean(type, value, tb):
    traceback_details = "\n".join(traceback.extract_tb(tb).format())
    msg = f"\ncaller: {' '.join(sys.argv)}\n{type}: {value}\n{traceback_details}"
    for i in activeAnalysers:
        i.raise_exception()
        i.join()

sys.excepthook = clean

class threadedAnalyzer(threading.Thread):
    def __init__(self, recordName=None, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._target = analyzeRecord
        self._args = (recordName,)



class testObj:
    def __init__(self):
        self.recordInfo = {}


def analyzeRecord(file):
    with open(file) as trJson:
        try:
            testRecord = json.load(trJson)
        
        except Exception as err:
            print(f"WARNING: File {file} has Errors: {err}")
            return

    file = testObj()
    for recordTy in recordTypes:
        if recordTy in testRecord.keys():
            file.recordInfo[recordTy] = testRecord[recordTy].lower()

        else:
            file.recordInfo[recordTy] = "MISSING"

    testRecords.append(file)
    


def handTestRecords():
    for singleRecord in glob.glob(f"{recordDir}*.json"):
        recName = singleRecord.split(recordDir)[1]
        recName = threadedAnalyzer(recordName=singleRecord, name=recName)
        activeAnalysers.append(recName)


def workStats(typeR):
    allTypeR = []
    for tr in testRecords:
        if tr.recordInfo[typeR] != "MISSING":
            allTypeR.append(tr.recordInfo[typeR])

    # averageTypeR = sum(allTypeR)/len(allTypeR)
    # return averageTypeR


def displayStats():
    for stat in recordTypes:
        importantStat = workStats(stat)

        print(f"Average {stat} was: {importantStat}")


if __name__ == "__main__":
    handTestRecords()

    for analysingThread in activeAnalysers:
        analysingThread.start()

    for analysingThread in activeAnalysers:
        analysingThread.join()
    displayStats()
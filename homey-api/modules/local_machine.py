from genericpath import exists

# reads values written by monitorSystem.py

class local_machine:
    def __init__(self, dataFile):
        self.dataFile = dataFile    # must match monitorSystem.py `dataFile`

    def getAllInfo(self):
        with open(self.dataFile, 'r') as f:
            return f.readlines()    # send better JSON
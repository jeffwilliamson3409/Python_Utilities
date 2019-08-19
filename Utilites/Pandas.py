import pandas as pd
from collections import OrderedDict as od
from datetime import datetime as dt
import os
from datetime import datetime as dt
import os


class Ail2_File_Append_Factory(object):

    def __init__(self, fileToRun):
        self.File = fileToRun
        self.FileName = os.path.basename(fileToRun)
        self.FileNameNoExt = self.FileName.replace('.ail2', '')

    def ICOS(self, status):
        if str(status).upper() in ('E', '4', 'Q', 'Z'):
            return 'Y'
        else:
            return 'N'

    def Fv(self, ck_char8):
        if str(ck_char8) != '0':
            return 'Y'
        else:
            return 'N'

    def FReC(self, ck_char6):
        if str(ck_char6).upper() == 'B':
            return 'Y'
        else:
            return 'N'
        
    def createAil2DataFrame(self):
        dateStamp = dt.now().strftime("%Y%m%d%M%S")      
        df = pd.DataFrame.from_csv(self.File, sep='\t')
        df['ICOS'] = df.apply(lambda rowContext: self.ICOS(rowContext['status']), axis=1)
        df['Fv'] = df.apply(lambda rowContext: self.Fv(rowContext['ck_char8']), axis=1)
        df['FReC'] = df.apply(lambda rowContext: self.FReC(rowContext['ck_char6']), axis=1)
        df['Vanguard'] = 'N'
        df['FileName'] = self.FileNameNoExt
        df['RunDateTime'] = str(dateStamp)
        return df

    def returnToCsv(self, df, fileName):
        return df.to_csv(fileName, sep='\t')


if __name__ == "__main__":

    file = None # set variable to file path you wish to process
    returnFileName = None # set variable to your return file name

    a = Ail2_File_Append_Factory(file)
    dataFrame = a.createAil2DataFrame()
    a.returnToCsv(dataFrame, returnFileName)




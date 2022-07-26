import pandas as pd
import os

data = {'Data': [10, 20, 52, 11, 30]}

class excel:
    def write(excelFile, dict):
        df = pd.DataFrame(dict)
        writer = pd.ExcelWriter(os.path.join('data/',excelFile +'.xlsx'), engine='xlsxwriter')

        os.path.join('data/',excelFile,'.xlsx')
        df.to_excel(writer,sheet_name='Sheet1')
        writer.save()
        print("done_saving")

excel.write('test', data)

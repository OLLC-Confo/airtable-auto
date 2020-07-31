import pandas as pd
import os
from fpdf import FPDF


class LectureSubmission:
    
    def __init__(self, table_name, df, df_cols, path, CLASS):
        self.table_name = table_name
        self.df = df
        self.df_cols = df_cols
        self.count = len(self.df)
        self.path = path
        self.CLASS = CLASS
        self.divisions = division_map[CLASS]

    def create_empty_folders(self):
        os.chdir(self.path)
        print('PATH changed')
        
        FOLDER_NAME = self.table_name
        if not FOLDER_NAME in os.listdir():
            os.mkdir(FOLDER_NAME)
            print('Created base folder.')
        else:
            print('Base folder exists.')
        os.chdir(FOLDER_NAME)
        delete_count = 0
        for division in self.divisions:
            if division not in os.listdir():
                os.mkdir(division)
            else:
                for file in os.listdir(division):
                    os.remove(division + '/' + file)
                    delete_count += 1
        print('Deleted previous files:', delete_count, '\n')

    def create_pdf(self):
        fault_count = 0
        for row_val in self.df.itertuples():
            try:
                pdf = FPDF()
                pdf.add_font('noto', '', BASE_PATH + '/fonts/NotoSerif-Regular.ttf', uni=True)
                pdf.add_font('notoB', '', BASE_PATH + '/fonts/NotoSerif-Bold.ttf', uni=True)
                file_name = row_val['Division'] + '/' + row_val['Name'].upper().replace("'","").strip().rstrip() + '.pdf'
                print(file_name)
                pdf.add_page()
                for i in range(len(self.df_cols)):

                    pdf.set_font("notoB", "", 14)
                    pdf.set_text_color(0, 45, 90)
                    pdf.write(7, "\n\n" + str(self.df_cols[i]))
                    
                    pdf.set_font("noto", "", 14)
                    pdf.set_text_color(0, 0, 0)
                    pdf.write(7, "\n" + str(row_val[i+1]))
                

                pdf.output(file_name, 'F')
                yield True

            except Exception as e:
                print(e)
                fault_count += 1
        print("Fault count:", fault_count)

df = pd.read_csv('tabs.csv')
df = df.sort_values(by=['Division', 'Name'])
# print(len(df))

division_map = {
    'X': ['A','B','C','D','E','F','G'],
    'XI': ['A','B','C','D','E','F']
}


BASE_PATH = os.path.abspath(os.curdir)
df_cols = [x for x in df.columns]


l = LectureSubmission('Baptism XI', df, df_cols, os.curdir, 'XI')
l.create_empty_folders()
l.create_pdf()
        


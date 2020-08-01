import pandas as pd
import os
from fpdf import FPDF


class LectureSubmission:
    
    def __init__(self, table_name, path, CLASS):
        self.table_name = table_name
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

def create_pdf(df, df_cols, BASE_PATH):
    filename = ''
    for row in df.itertuples():
        pdf = FPDF()
        pdf.add_font('noto', '', 'NotoSerif-Regular.ttf', uni=True)
        pdf.add_font('notoB', '', 'NotoSerif-Bold.ttf', uni=True)
        pdf.add_page()
        for i in range(len(df_cols)):
            question = df_cols[i]
            answer = row[i+1]
            print('\n')
            filename = row.Name.upper().strip().rstrip() + '.pdf'
            try:
                pdf.set_font("notoB", "", 14)
                pdf.set_text_color(0, 45, 90)
                pdf.write(7, "\n\n" + str(question))
                        
                pdf.set_font("noto", "", 14)
                pdf.set_text_color(0, 0, 0)
                pdf.write(7, "\n" + str(answer))
            except Exception as e:
                print(e)
        os.chdir(BASE_PATH + '/' + row.Division)
        print(os.getcwd())
        yield pdf.output(filename, 'F')
        os.chdir(BASE_PATH)
        


## DATA PROCESSING
df = pd.read_csv('tabs.csv')
df = df.sort_values(by=['Division', 'Name'])
df_cols = [x for x in df.columns]


division_map = {
    'X': ['A','B','C','D','E','F','G'],
    'XI': ['A','B','C','D','E','F']
}

TABLE_NAME = 'Baptism'

CLASS = 'XI'

BASE_PATH = os.path.abspath(os.curdir)
l = LectureSubmission(TABLE_NAME, BASE_PATH, CLASS)
l.create_empty_folders()
create_pdf(df, df_cols, BASE_PATH + '/' + TABLE_NAME)





        


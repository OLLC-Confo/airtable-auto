from fpdf import FPDF
import pandas as pd
import os


class PDF(FPDF):
    def __init__(self, table_name):
        FPDF.__init__(self,orientation='P',unit='mm',format='A4')
        self.table_name = table_name

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, self.table_name + " | Page " + str(self.page_no()), 0, 0, 'C')


class LectureSubmission:
    
    def __init__(self, table_name, path, CLASS):
        self.table_name = table_name
        self.path = path
        self.CLASS = CLASS
        self.divisions = division_map[CLASS]

    def create_empty_folders(self):
        os.chdir(self.path)
        print('PATH changed', os.getcwd())
        
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
        os.chdir(BASE_PATH)

def create_pdf(df, df_cols, BASE_PATH):
    filename = ''
    for row in df.itertuples():
        pdf = PDF(TABLE_NAME)
        pdf.add_font('noto', '', 'fonts/NotoSerif-Regular.ttf', uni=True)
        pdf.add_font('notoB', '', 'fonts/NotoSerif-Bold.ttf', uni=True)
        pdf.add_page()
        
        pdf.set_font("notoB", "", 16)
        pdf.set_text_color(0, 45, 90)
        pdf.cell(w = 0, h = 0, txt = str(TABLE_NAME), align = 'C')
        
        for i in range(len(df_cols)):
            question = df_cols[i]
            answer = row[i+1]
            filename = row.Name.upper().strip().rstrip() + '.pdf'
            try:
                pdf.set_font("notoB", "", 12)
                pdf.set_text_color(0, 45, 90)
                pdf.write(7, "\n\n" + u'\u2022 ' + str(question))
                        
                pdf.set_font("noto", "", 12)
                pdf.set_text_color(0, 0, 0)
                pdf.write(7, "\n" + str(answer))
                
            except Exception as e:
                print(e)

        res = pdf.output(BASE_PATH + '/' + row.Division + "/" + filename, 'F')
    print("Done", res)
        


## DATA PROCESSING
df = pd.read_csv('16. The 7th Commandment.csv') # Change the name here to the downloaded csv file
df = df.sort_values(by=['Division', 'Name'])
df_cols = [x for x in df.columns]


division_map = {
    'X': ['A','B','C','D','E','F','G'],
    'XI': ['A','B','C','D','E','F']
}

TABLE_NAME = '16. The 7th Commandment'   # This also is the name appended to the top of the worksheet

# Name in the above manner only

CLASS = 'XI' # change class as required

BASE_PATH = os.path.abspath(os.curdir)
print(BASE_PATH)
l = LectureSubmission(TABLE_NAME, BASE_PATH, CLASS)
l.create_empty_folders()
create_pdf(df, df_cols, BASE_PATH + '/' + TABLE_NAME)
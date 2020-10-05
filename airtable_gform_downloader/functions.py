from airtable import Airtable
from fpdf import FPDF
import os

BASE_PATH = os.path.abspath(os.curdir)


division_map = {
    'X': ['A','B','C','D','E','F','G'],
    'XI': ['A','B','C','D','E','F']
}

class LectureSubmission:
    
    def __init__(self, base_key, api_key, table_name, path, CLASS):
        self.table_name = table_name
        self.airtable = Airtable(
            base_key, table_name, api_key
        ).get_all(sort = 'Division') # ,maxRecords = ?
        self.count = len(self.airtable)
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
        for test in self.airtable:
            try:
                pdf = FPDF()
                pdf.add_font('noto', '', BASE_PATH + '/NotoSerif-Regular.ttf', uni=True)
                pdf.add_font('notoB', '', BASE_PATH + '/NotoSerif-Bold.ttf', uni=True)
                file_name = test['fields']['Division'] + '/' + test['fields']['Name'].upper().replace("'","").strip().rstrip() + '.pdf'
                print(file_name)
                pdf.add_page()
                for i in test['fields']:

                    pdf.set_font("notoB", "", 14)
                    pdf.set_text_color(0, 45, 90)
                    pdf.write(7, "\n\n" + str(i))
                    
                    pdf.set_font("noto", "", 14)
                    pdf.set_text_color(0, 0, 0)
                    pdf.write(7, "\n" + str(test['fields'][i]))
                
                pdf.write(7, "\n\n" + f"{self.CLASS} {self.table_name} {test['fields']['Name']} {test['createdTime']}")
                pdf.output(file_name, 'F')
                yield True

            except Exception as e:
                print(e)
                fault_count += 1
        print("Fault count:", fault_count)
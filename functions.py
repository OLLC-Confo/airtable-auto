from airtable import Airtable
from docx2pdf import convert
from docx import Document
import os


def get_airtable_records(base_key, table_name, api_key):
    airtable = Airtable(
        base_key, table_name, api_key
    )
    return airtable.get_all(sort = 'Division', maxRecords=10)

def create_empty_folders(divisions, path):
    os.chdir(path)
    print('PATH changed')
    
    FOLDER_NAME = 'Submissions'
    if not FOLDER_NAME in os.listdir():
        os.mkdir(FOLDER_NAME)
        print('Created base folder.')
    else:
        print('Base folder exists.')
    os.chdir(FOLDER_NAME)
    delete_count = 0
    for division in divisions:
        if division not in os.listdir():
            os.mkdir(division)
        else:
            for file in os.listdir(division):
                os.remove(division + '/' + file)
                delete_count += 1
    print('Deleted previous files:', delete_count, '\n')

def create_pdf(test):
    try:
        document = Document()
        file_name = test['fields']['Division'] + '/' + test['fields']['Name'] + '.docx'
        for i in test['fields']:
            document.add_heading(str(i)).bold = True
            document.add_paragraph(test['fields'][i])
        document.add_paragraph(test['createdTime'])
        document.save(file_name)
        convert(file_name)
        os.remove(file_name)
        return True

    except Exception as e:
        print(e)
        return False
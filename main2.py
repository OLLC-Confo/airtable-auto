from airtable import Airtable
from docx import Document
from docx2pdf import convert
import os

TABLE_NAME = 'Table 1'
FOLDER_NAME = TABLE_NAME + ' Submissions'
BASE_KEY = 'appsExXNgItazXQbG'
MY_KEY = 'key1tY4mE9VGNB5uu'

airtable = Airtable(
    BASE_KEY, TABLE_NAME, MY_KEY
)

try:
    if FOLDER_NAME in os.listdir():
        os.chdir(FOLDER_NAME)
    else:
        os.mkdir(FOLDER_NAME)
        os.chdir(FOLDER_NAME)
    for i in os.listdir():
        os.remove(i)
except Exception as e:
    print(e)

submission = airtable.get_all()
print('Number of files: ' ,len(submission))

document = Document()

try:
    for i in range(65, 72):
        os.mkdir(chr(i))
except Exception as e:
    print(e)

for test in submission:
    file_name = test['fields']['Name'] + '.docx'
    for i in test['fields']:
        p = document.add_heading(str(i)).bold = True
        p = document.add_paragraph(test['fields'][i])
    p = document.add_paragraph(test['createdTime'])

    # the stuff below this doesn't seem to be the problem
    try:
        if test['fields']['Division'] in os.listdir():
            os.chdir(test['fields']['Division'])
            document.save(file_name)
            convert(file_name)
            os.remove(file_name)
            os.chdir('..')
        for i in os.listdir():
            os.remove(i)  # idk why we do this, but you did it above so I copied. Works fine without it too.
    except Exception as e:
        print(e)



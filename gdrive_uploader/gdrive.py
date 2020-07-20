from pydrive.drive import  GoogleDrive
from pydrive.auth import GoogleAuth
from pygdrive3 import service
import pandas as pd
import os


''' Class Data Retrieval '''
CLASS_MAP = pd.read_csv("class_map.csv")

''' Authentication only required for duplicate folder deletion, etc, later to be done'''
def authenticate():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("./client_secrets.json")
    drive = GoogleDrive(gauth)
    return drive


def upload_all(lecture_name, submissions_folder, CLASS):
    global CLASS_MAP
    CLASS_MAP = CLASS_MAP[CLASS_MAP.CLASS == CLASS]
    drive_service = service.DriveService('./client_secrets.json')
    drive_service.auth()

    print("Uploading...")
    for division in os.listdir(submissions_folder):
        UPLOAD_DIVISION = CLASS_MAP[CLASS_MAP.DIVISION == division]
        print("\nDivision:",division)
        lecture_folder = drive_service.create_folder(lecture_name, UPLOAD_DIVISION["PATH"].values[0])

        count = 0
        for worksheet in os.listdir(submissions_folder + "/" + division):
            file_path = submissions_folder + "/" + division + "/" + worksheet
            try:
                drive_service.upload_file(worksheet, file_path, lecture_folder)
                count += 1
            except Exception as e:
                print(e)
        print("Count:", count)
    print("Done")



#upload_all(lecture_name, submissions_folder, CLASS)

'''
lecture_name = "" #Final folder name in GDrive
CLASS = ""                                     #X or XI
submissions_folder = ""        #Path to downloaded submissions
'''

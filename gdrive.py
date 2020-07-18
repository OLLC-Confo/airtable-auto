from pydrive.drive import  GoogleDrive
from pydrive.auth import GoogleAuth
from pygdrive3 import service #found this
import pandas as pd
import os

''' Data to be entered, should GUI this '''
lecture_name = "4. Jesus' Baptism, Ministry, Manifesto" #Final folder name in GDrive
CLASS = "TestClass"                                     #X or XI
submissions_folder = "C:/Users/Keane/Desktop/L4"        #Path to downloaded submissions


''' Class Data Retrieval '''
CLASS_MAP = pd.read_csv("class_map.csv")
CLASS_MAP = CLASS_MAP[ CLASS_MAP.CLASS == CLASS]


''' Authentication only required for folder deletion, etc, later to be done'''
def authenticate():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("./client_secrets.json")
    drive = GoogleDrive(gauth)
    return drive


def upload_all(lecture_name, submissions_folder, CLASS_MAP):
    drive_service = service.DriveService('./client_secrets.json')
    drive_service.auth()
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


upload_all(lecture_name, submissions_folder, CLASS_MAP)
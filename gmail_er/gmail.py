from __future__ import print_function
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import email.encoders as encoder
from apiclient import errors
import pandas as pd
import mimetypes
import os.path
import base64
import pickle
import os
import re


# If modifying these scopes, delete the file token.pickle.
# Ideally don't touch it
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir, filename):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    path = os.path.join(file_dir, filename)
    content_type, encoding = mimetypes.guess_type(path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
        
    x = open(path, 'rb').read()
    msg = MIMEBase('application', 'pdf')
    msg.set_payload(x)

    encoder.encode_base64(msg)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_string().encode()).decode()
    
    return {'raw': raw}


def SendMessage(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    # print('Message Id: %s' % message['id'])
    return message
  except Exception as error:
    print('An error occurred: %s' % error)
    return None


def get_df(std):
    if std in ['x','X']:
        df = pd.read_csv('x_email.csv')
        return df
    elif std in ['xi','XI']:
        df = pd.read_csv('xi_email.csv')
        return df
    else:
        return None

def postman(submissions_path, std, sender_email, subject, body):
    main_class_data = get_df(std) # gets x or xi email file
    service = authenticate() # creates authencation object

    confirm = input("Do you want to send all emails? y/n:")
    if confirm not in ["y", "Y"]:
        return
    
    i = 0
    check_these_names = open("check_these_emails.txt", "w")
    for division in os.listdir(submissions_path):
        class_data = main_class_data.query(f'DIVISION == "{division}"')
        
        print('Mailing ' + division + '..')

        for file in os.listdir(submissions_path + '/' + division):
            filename = file[:-4].split()
            for k in range(len(filename)):
                filename[k] = filename[k].replace("'", "").rstrip().strip()
            #if len(filename) == 2: #name and surname
            x = class_data.query(f'NAME == "{filename[0]}" and SURNAME == "{filename[-1]}"')['EMAIL']
            #print(x)
            if len(x.index) > 0:
                try:
                    to_email = x.values[0]
                    file_path = submissions_path + "/" + division
                    msg = CreateMessageWithAttachment(sender_email, to_email, subject, body, file_path, file)
                    SendMessage(service, sender_email, msg)
                    print(str(division),"\t",str(file),"\t Whoppie",'\t',str(to_email))
                    i += 1
                except Exception as e:
                    print(e)
                    check_these_names.write(str(division) + "\t" + str(file) + "\tStudent found, Exception" + "\n")
            else:
                print(x)
                check_these_names.write(str(division) + "\t" + str(file) + " \tNot found \t" + str(filename) + "\n")
    print(i, ' mails sent successfully!')
    check_these_names.close()

    
submissions_path = ''   #path to folder
std = ''                # x or xi
sender = ''
sender_email = ''
subject = ''
body = ""   # or can create a custom body in the loop with name i.e. filename[0]


class_data = get_df(std)
postman(submissions_path, std, sender_email, subject, body)

'''
    

def get_file_name_prefix(file_path):
    basename = os.path.basename(file_path)
    file_name_prefix_match = re.compile(r"^(?P<file_name_prefix>.*)\..*$").match(basename)
    if file_name_prefix_match is None:
        return file_name_prefix_match
    else:
        return file_name_prefix_match.group("file_name_prefix")
    

'''
    
'''def get_email(df, file_name):
    file_name = [x for x in file_name]
    print(file_name)
    email = df.loc[(df['NAME'].str.strip() == file_name[0]) & (df['SURNAME'].str.strip() == file_name[1])]
    email = email['EMAIL'].to_string()[3:].strip()
    
    if '@' in email:
        return email
    else:
        # need to impute special characters in surname.
        # the register and the file name may have differing spellings
        return None
'''
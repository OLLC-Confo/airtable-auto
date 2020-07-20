from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from email.message import EmailMessage
from __future__ import print_function
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
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
    
  fp = open(path, 'rb')
  x = fp.read()
  fp.close()
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
    return None
    print('An error occurred: %s' % error)


def get_df(std):
    if std == 'x':
        df = pd.read_excel('x_email.xlsx')
        return df
    elif std == 'xi':
        df = pd.read_excel('xi_email.xlsx')
        return df
    else:
        return None
    

def get_file_name_prefix(file_path):
    basename = os.path.basename(file_path)
    file_name_prefix_match = re.compile(r"^(?P<file_name_prefix>.*)\..*$").match(basename)
    if file_name_prefix_match is None:
        return file_name_prefix_match
    else:
        return file_name_prefix_match.group("file_name_prefix")
    
    
def get_email(df, file_name):
    file_name = [x for x in file_name]
    email = df.loc[(df['NAME'].str.strip() == file_name[0]) & (df['SURNAME'].str.strip() == file_name[1])]
    email = email['EMAIL'].to_string()[3:].strip()
    
    if '@' in email:
        return email
    else:
        # need to impute special characters in surname.
        # the register and the file name may have differing spellings
        return None


def postman(submissions_path, std, subject, body):
    df = get_df(std) # gets x or xi email file
    fail_mail = open('fail_mail.txt', 'w')
    service = authenticate() # creates authencation object
    sender_email = 'orlemconfo@gmail.com'
    i = 0
    for folder in os.listdir(submissions_path):
        print('Mailing ' + folder + '..')
        file_path = submissions_path + '/' + folder

        for file in os.listdir(file_path):
            file_name_prefix = get_file_name_prefix(file_path + '/' + file).upper() # removes extension
            to_email = get_email(df, file_name_prefix.split())
            # print(to_email)
            if to_email is None:
                fail_mail.write(file_name_prefix + '\n')
            else:
                try:
                    # passing file name with extension
                    msg = CreateMessageWithAttachment(sender_email, to_email, subject, body, file_path, file)
                    SendMessage(service, sender_email, msg, fail_mail)
                    i += 1
                except Exception as e:
                    print(e)
                    fail_mail.write(file_name_prefix + '\n') 
        print('Whoppie\n')
    print(i, ' mails sent successfully!')
    fail_mail.close()          
        
    
submissions_path = ''
std = '' # x or xi
sender = ''
subject = ''
body = ''   
postman(submissions_path, std, subject, body)
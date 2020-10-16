from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
import os
import os.path



def get_service():

    SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/classroom.announcements.readonly']
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    service = build('classroom', 'v1', credentials=creds)
    return service


def download_file(file_id, file_name, course_name):

    SCOPES = ['https://www.googleapis.com/auth/drive']

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickledrive'):
        with open('token.pickledrive', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential-drive.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickledrive', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds) 

    request = service.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

    fh.seek(0)

    with open (os.path.join('./',course_name,file_name), 'wb') as f:
        f.write(fh.read())
        f.close()

def main():

    service=get_service()
    courses=service.courses().list(pageSize=11).execute()
    
    for course in courses['courses']:

        course_name=course['name']
        course_id=course['id']

        try:
            os.mkdir('./'+course_name)
        except OSError:
            print("Creation of {} directory failed".format(course_name))
        else:
            print("Created {} directory ".format(course_name))

        announcements = service.courses().announcements().list(courseId=course_id).execute()
        annonc_list=announcements.keys()


        if (len(annonc_list) == 0 ):
            continue
        else:
            for announcement in announcements['announcements']:

                try:
                    for val in announcement['materials']:
                        file_id=val['driveFile']['driveFile']['id']
                        file_name=val['driveFile']['driveFile']['title']
                        download_file(file_id, file_name, course_name)
                        print("HAHAHA")
                except KeyError as e:
                    print("this announcement doesn't have any file to download")





if __name__ == '__main__':
    main()
A script that automates downloading Google Classroom files and organizes them each in their appropriate folder.

Prerequisities:

Python

Pip

How to setup the necessary files for the script?

1- First we need to create a project in Google Cloud Platform : https://developers.google.com/workspace/guides/create-project

2- Next we need to enable Google Classroom API and Google Drive API in our project : https://developers.google.com/workspace/guides/enable-apis

3- Now we need to configure the OAuth consent screen so that we can be able to create credentials that we will later download and allows our app to access our data.

    This can be achieved by following this guide : https://developers.google.com/workspace/guides/configure-oauth-consent.

    There are 2 important steps in this part :

    1-Add our email address to test users, just add the email address (addresses) you're gonna use to access the app.

    2-Add the required scopes, the ones that our app will need to function properly ,

    For Google Classroom API we will need these scopes
    SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.announcements.readonly',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly'
    ]
    For Google Drive API we will need this one :
    SCOPES = ['https://www.googleapis.com/auth/drive']

4- After configuring the OAuth consent screen, we can now create credentials in our GCP project, we need to create OAuth Client ID for a desktop app :

https://developers.google.com/workspace/guides/create-credentials#desktop-app

If you still didn't configure the OAuth consent screen , you will get a warning and won't be able to create credentials.

5- Finally, after creating the credentials that our app needs to function, we can now download the json file that contains our credentials. The download button for that file should be easily accessible. After downloading that file we need to rename it to credentials.json and place it next to the python script ClassroomFilesDownloader.py.

ALMOST DONE!!!!!!!

Now we need to execute a command in our terminal : pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

This is mentioned here in this guide : https://developers.google.com/drive/api/quickstart/python

\*\* Now we are ready to execute our script but before that we need to tell our script the number of courses to download by editing a variable value in the script:

    - open the ClassroomFilesDownloader.py in any text editor you want

    - CTRL +F  to look for the word "pageSize"

    - change the value of that variable to how many courses you want to download, it works by the newest to oldest order.

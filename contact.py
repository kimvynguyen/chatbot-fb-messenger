from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from table import UserData
from sqlalchemy import create_engine

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1NjafDX46oOt7ThuEdTjF-ogJ3G-emNF4OlQQbDwAdDo'
SAMPLE_RANGE_NAME = 'Vmarketing!A2:F'

engine = create_engine('sqlite:///save_user.db')
conn = engine.connect()

def main(sender_id):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        s = UserData.select()
        result = conn.execute(s)
        l = 0
        for row in result:
            l = l + 1
        if l < len(values):
            delete = UserData.delete()
            conn.execute(delete)
            id = 1
            for row in values:
                ins = UserData.insert().values(id= id,fb_id = sender_id,congty=row[1],ten=row[2],sodienthoai=row[3],email=row[4])
                conn.execute(ins)
                print("{0}, {1}, {2}, {3}, {4}".format(row[0],row[1],row[2],row[3],row[4]))
                id = id + 1
                return 'ok'
    return 'khong ton tai'

'''if __name__ == '__main__':
    main('123')'''

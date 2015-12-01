from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'client_secret.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(src_cal, dest_cal): 
    credentials = get_credentials()
    dest_cal_id = 'test'
    src_cal_id = 'test'
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    page_token = None
    calendar_list = service.calendarList().list(pageToken=None).execute()
    for calendar_list_entry in calendar_list['items']:
      if (calendar_list_entry['summary'] == dest_cal):
        dest_cal_id = calendar_list_entry['id']
        print('setting dest_cal_id')
    for calendar_list_entry in calendar_list['items']:
      if (calendar_list_entry['summary'] == src_cal):
        print ('found ' + calendar_list_entry['summary'] + ' and setting src_cal_id')
        src_cal_id = calendar_list_entry['id']
        print('Getting the events from the source calendar...')
        eventsResult = service.events().list(calendarId=src_cal_id).execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No events found in source calendar.')
        for event in events:
            perma_color = event.get('colorId')
            calendar_color_id = calendar_list_entry['colorId']
            #handle coloring
            #check for manual coloring specific to this event
            if (perma_color == None): #no manual coloring
                #set colorId of event to default for source calendar
                perma_color = calendar_color_id
            service.events().move(calendarId=src_cal_id, eventId=event['id'], destination=dest_cal_id).execute()
            event = service.events().get(calendarId=dest_cal_id, eventId=event['id']).execute()
            event['colorId'] = perma_color
            updated_event = service.events().update(calendarId=dest_cal_id, eventId=event['id'], body=event).execute()
            print('Transferring an event into ' + dest_cal + '.')

if __name__ == '__main__':
    main('origin_calendar_name', 'destination_calendar_name')
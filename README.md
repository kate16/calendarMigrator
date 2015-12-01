# calendarMigrator #

This is a simple python script to migrate all events from one Google calendar to another. In order to be successful, you must be able to edit both the origin and destination calendars. 

First, it's necessary to enable OAuth 2.0 authorization for Google Calendar API access. You can find instructions for this here: https://developers.google.com/identity/protocols/OAuth2

Then rename the generated json file to 'client_secret.json' and move it to the same directory as cal_script.py. 

To run, modify cal_script.py's final line (below) to include the target origin and destination calendar names. 

<pre><code>main('origin_calendar_name', 'destination_calendar_name')</pre></code>

As a note, this script will migrate all events (unchanged) from the old to the new calendars. Color scheme will be preserved. 

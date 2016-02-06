from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build
from datetime import datetime, timedelta
import pprint,json,os,sys


client_email = 'your@email'
with open("your_cred_file") as f:
  private_key = f.read()

credentials = SignedJwtAssertionCredentials(client_email, private_key,
    'https://www.googleapis.com/auth/admin.reports.audit.readonly',sub='your@email')

DOMAIN = 'yourgoogledomain.com'

Http.debuglevel = 1
http_auth = credentials.authorize(Http())

reports = build('admin', 'reports_v1', http=http_auth)

try:

        one_day_ago = datetime.utcnow() - timedelta(days=1)
        default_start_time = one_day_ago.isoformat('T') + 'Z'

        now = datetime.utcnow() - timedelta(minutes=5)
        start_time = now.isoformat('T') + 'Z'
        end_time= now.isoformat('T') + 'Z'
        current_runtime = start_time
        eventtype = "success"
        RUN_DIR = "/opt/"

        if os.path.exists(os.path.join(RUN_DIR, eventtype + '.run')):
                LASTRUN = open(os.path.join(RUN_DIR, eventtype + '.run'), 'r').read()
                if len(LASTRUN) < 3:
                        LASTRUN = default_start_time
        else:
                open(os.path.join(RUN_DIR, eventtype + '.run'), 'w').close()
                open(os.path.join(RUN_DIR, eventtype + '.run'), 'w').write(str(default_start_time))
                LASTRUN = default_start_time

        request = reports.activities().list(userKey='all',applicationName="login",eventName="login_success",startTime=LASTRUN,endTime=end_time)

        response = request.execute()

        if response.has_key("items"):
                for value in response['items']:
                        print json.dumps(value,indent=2)
                        print "==="

        open(os.path.join(RUN_DIR, eventtype + '.run'), 'w').write(str(current_runtime))
        pass

except Exception, e:
        pprint.pprint(e)
        sys.exit(1)
else:
        pass
finally:
        pass






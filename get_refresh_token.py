"""Run ONCE on your own computer (not in chat):  pip install google-auth-oauthlib  &&  python get_refresh_token.py client_secret.json
In the browser, choose the account, then pick the channel "Rules Left Behind".
Copy the printed refresh token directly into GitHub Secrets (YT_REFRESH_TOKEN). Never paste it into a chat."""
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
f=InstalledAppFlow.from_client_secrets_file(sys.argv[1],['https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube.force-ssl'])
c=f.run_local_server(port=0,prompt='consent',access_type='offline')
print('\nYT_REFRESH_TOKEN =',c.refresh_token)

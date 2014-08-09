#https://github.com/Rentier/ReindeerIkenga/blob/master/authenticate.py
from oauth2client.client import flow_from_clientsecrets


flow = flow_from_clientsecrets('client_secrets.json',
                               scope='https://www.googleapis.com/auth/calendar',
                               redirect_uri='urn:ietf:wg:oauth:2.0:oob')

auth_uri = flow.step1_get_authorize_url()
print('Visit this site!')
print(auth_uri)
code = raw_input('Insert the given code!')
credentials = flow.step2_exchange(code)
print(credentials)
    
with open('credentials', 'wr') as f:
    f.write(credentials.to_json())

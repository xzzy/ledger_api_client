from django.conf import settings
import urllib.request, json
import urllib.parse
from confy import env

def get_ledger_user_info_by_id(userid):
    json_response = {}
    attributemap = {}
    data = urllib.parse.urlencode(attributemap)
    data = data.encode('utf-8')
    with urllib.request.urlopen(settings.LEDGERGW_URL+"ledgergw/remote/userid/"+userid+"/"+settings.LEDGER_API_KEY+"/", data) as url:
           json_response = json.loads(url.read().decode())
    return json_response


def search_ledger_users(keyword):
    print ("IN")
    json_response = {}
    attributemap = {}
    data = urllib.parse.urlencode(attributemap)
    data = data.encode('utf-8')
    with urllib.request.urlopen(settings.LEDGERGW_URL+"ledgergw/remote/user-search/"+keyword+"/"+settings.LEDGER_API_KEY+"/", data) as url:
           json_response = json.loads(url.read().decode())
    return json_response


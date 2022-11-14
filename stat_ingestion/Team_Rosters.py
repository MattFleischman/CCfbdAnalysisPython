from __future__ import print_function
import cfbd
from cfbd.rest import ApiException
from pprint import pprint

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'XbfBgZjizImMF81QPIho2e68olGYRSRCmZJzFU6DbwPPJj+BoGM1CflXMZjTQ7TS'
configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))
team = 'Wyoming' # str | Team name (optional)
year = 2022 # int | Season year (optional)

try:
    # Team rosters
    api_response = api_instance.get_roster(team=team, year=year)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->get_roster: %s\n" % e)
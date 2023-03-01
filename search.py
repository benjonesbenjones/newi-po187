from googleapiclient.discovery import build
import json as j

API_KEY = 'AIzaSyD5R-0HKVeJf3aGzBcdMKT5qKmbSvlZteA'
SEARCH_ID = '70d7331a380104754'


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


results = google_search('"winnebago county" "voter registration"', API_KEY, SEARCH_ID, num=10)
print(j.dumps(results, sort_keys=True, indent=4))
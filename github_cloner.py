from __future__ import print_function
import json
import requests
from requests.auth import HTTPBasicAuth


USERNAME = ''
PASSWORD = ''
TARGET = ''
BASE_API = 'https://api.github.com/'


def main():
    # Auth credential with basic auth.
    auth = HTTPBasicAuth(USERNAME, PASSWORD)

    # Create request to get starred repo from logged in user.
    user_response = requests.get(url=BASE_API + 'user/starred', auth=auth)

    # Create request to get starred repo from target user.
    target_response = requests.get(BASE_API + 'users/{target}/starred'.format(target=TARGET))

    # Get list of starred repo in each `user_response` & `target_response`.
    # Construct as tuple `(owner_name, repo_name)`.
    user_starred = [(u['owner']['login'], u['name']) for u in user_response.json()]
    target_starred = [(t['owner']['login'], t['name']) for t in target_response.json()]

    # Get difference starred repo to find which starred repo from target user
    # should be clone.
    difference_starred = list(set(target_starred) - set(user_starred))
    # Check if no different repo from target user.    
    if len(difference_starred) > 0:
        for param in difference_starred:
            star_url = BASE_API + 'user/starred/%s/%s' % param
            # Perform star repo from list of `diference_starred`.
            r = requests.put(url=star_url, auth=auth, headers={'Content-Length': 0})
            print(r.status_code)
        else:
            print('All repo successfully cloned.')
    else:
        print('All repo already starred.')


if  __name__ == '__main__':
    main()
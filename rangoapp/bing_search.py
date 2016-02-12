import json
import urllib 
import urllib.request as urllib2
from rangoapp import keys


BING_API_KEY = keys.bing_api_key

def run_query(search_term):
    root_url = 'https://api.datamarket.azure.com/Bing/SearchWeb/'
    source = 'Web'
    results_per_page = 10
    offset = 0

    query = "'{0}'".format(search_term)
    query = urllib.parse.quote(query)

    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(root_url, source, results_per_page, offset, query)
    username = ''
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)
    results = []

    try:
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        json_response = urllib2.urlopen(search_url).read()
        response = json.loads(json_response.decode())
        for result in response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']
                })

    except urllib2.URLError as e:
        print("Error when querying the bing api", e)

    return results


def main():
    q = input("Enter your search term here: ")
    ans = run_query(q)[:10]
    for rank, a in enumerate(ans):
        print('rank: ', rank)
        print('title: ', a['title'])
        print('url: ', a['link'])


if __name__ == '__main__':
    main()

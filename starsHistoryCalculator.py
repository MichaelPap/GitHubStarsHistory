import requests
import json
import time
import sys
from dateutil.parser import parse
from properties import GitHubAuthToken
from helpers import print_usage, write_results_to_disk

class GitHubStarsHistory:
    
    def __init__(self):
        self.token = GitHubAuthToken
    
    def download_stargazers(self, repository):
        """
        Function that downloads the stargazers information in order to calculate stars history in a monthly basis

        :param repository: the GitHub repository.
        :returns: A json object containing the number of stars for the given repository in a monthly basis
        """
        
        print('Downloading Stargazers Info for repository:', repository)
        stars_info = []
        
        self.check_limit()
        r = requests.get("https://api.github.com/repos/" + repository + '/stargazers?per_page=100', 
                         headers = {
                             'Authorization': 'token ' + self.token,
                             'Accept': 'application/vnd.github.v3.star+json'
                        })
        
        if int(r.status_code) == 200:
            for stargazer in json.loads(r.text or r.content):
                stars_info.append(stargazer)
            
            if 'Link' in r.headers:
                pages_info = r.headers["Link"].split(',')
                last_page = pages_info[1].split(';')[0].split('&page=')
                last_page = int(last_page[-1].replace('>', ''))
                
                print('Number of Info Pages:', str(last_page))
                print('Downloading Page', str(1))
                for page in range(2, last_page + 1):
                    print('Downloading Page', str(page))
                    
                    self.check_limit()
                    r = requests.get("https://api.github.com/repos/" + repository + '/stargazers?per_page=100&page=' + str(page), 
                         headers = {
                             'Authorization': 'token ' + self.token,
                             'Accept': 'application/vnd.github.v3.star+json'
                        })
                    if int(r.status_code) == 200:
                        for stargazer in json.loads(r.text or r.content):
                            stars_info.append(stargazer)
                    else:
                        print('Page ' + str(page) + ' - Query failed')
                    
        else:
            print('Page 1 - Query failed')
            
        stars = {}
        for stargazer_info in stars_info:
            timestamp = parse(stargazer_info["starred_at"])
            
            date_ref = str(timestamp.year) + '-' + str(timestamp.month).zfill(2)
            if date_ref in stars:
                stars[date_ref] += 1
            else:
                stars[date_ref] = 1
    
        sorted_keys = sorted(stars.keys())
        for i in range(1, len(sorted_keys)):
            stars[sorted_keys[i]] += stars[sorted_keys[i - 1]] 
        
        return stars
        
    def check_limit(self):
        """
        Checks the rate limit for the provided api key. In case the limit has been exceeded, then the function
        waits until it is reset
        """
        r = requests.get("https://api.github.com/rate_limit", headers = {'Authorization': 'token ' + self.token})
        if int(r.status_code) == 200:
            content = json.loads(r.text or r.content)
            self.remaining_requests = content["resources"]["core"]["remaining"]
            self.reset_time = content["resources"]["core"]["reset"]
            if(self.remaining_requests < 1):
                self.wait_for_limit_reset()
        else:
            print('Check limit query failed... Retry')
            self.check_limit()
    
    def wait_for_limit_reset(self):
        
        curr_time = time.time()
        sleep_time = int(self.reset_time - curr_time)
        print('Rate limit reached... Waiting for ' + str(sleep_time + 1) + ' seconds')

        time.sleep(sleep_time + 1)

if __name__ == "__main__":
    if ((not sys.argv) or len(sys.argv) <= 1):
        print('Invalid argument...')
        print_usage()
    elif(sys.argv[1].startswith("https://github.com/")):
        repository_name = sys.argv[1].replace('https://github.com/', '')
        starsHistory = GitHubStarsHistory()
        info = starsHistory.download_stargazers(repository_name)
        write_results_to_disk(info, repository_name.replace('/', '_') + '.json')
    else:
        print('Error in syntax...')
        print_usage()
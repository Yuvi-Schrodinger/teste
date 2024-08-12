import requests
import time
import json

class GraphAPI:
    def __init__(self, ad_acc, fb_api):
        self.base_url = "https://graph.facebook.com/v20.0/"
        self.api_fields = [
            "campaign_name","spend", "cpc", "cpm","ctr", "objective", "adset_name", 
            "adset_id", "clicks", "campaign_id", 
            "frequency", "date_start"
        ]
        self.token = "&access_token=" + fb_api
        self.ad_acc = ad_acc
        self.session = requests.Session()

    def make_request(self, endpoint, params=None):
        url = self.base_url + endpoint
        max_attempts = 5
        initial_wait_time = 1

        if params is None:
            params = {}
        params["access_token"] = self.token

        for attempt in range(max_attempts):
            response = self.session.get(url, params=params)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit error code
                print(f"Rate limit hit. Waiting {initial_wait_time} seconds before retrying.")
                time.sleep(initial_wait_time)
                initial_wait_time *= 2  # Exponential backoff
            else:
                try:
                    response.raise_for_status()
                except requests.HTTPError as e:
                    print(f"Error fetching data: {e}")
                    return None

        raise Exception("Maximum number of attempts reached. Request failed.")

    def get_insights(self, ad_acc, level="adset"):
        url = self.base_url + "act_" + str(ad_acc)
        url += "/insights?level=" + level
        url += "&fields=" + ",".join(self.api_fields)

        data = requests.get(url + self.token)
        return json.loads(data._content.decode("utf-8"))

    def get_campaigns_status(self, ad_acc):
        url = self.base_url + "act_" + str(ad_acc)
        url += "/campaigns?fields=name,status{name, id}"
        data = requests.get(url + self.token)
        return json.loads(data._content.decode("utf-8"))


    def get_adset_status(self):
        endpoint = f"act_{self.ad_acc}/adsets"
        params = {"fields": "name,status,id"}
        return self.make_request(endpoint, params)

    def get_adset_status(self, ad_acc):
        url = self.base_url + "act_" + str(ad_acc)
        url += "/adsets?fields=name,status,id"
        data = requests.get(url + self.token)
        return json.loads(data._content.decode("utf-8"))

    def get_data_over_time(self, campaign_id):
        url = self.base_url + f"{campaign_id}/insights"
        url += "?fields=" + ",".join(self.api_fields)
        url += "&time_range=("since":"2024-05-01","until":"2024-08-31)"
        url += "&time_increment=1"
        url += self.token
        
        data = requests.get(url)
        return json.loads(data._content.decode("utf-8"))

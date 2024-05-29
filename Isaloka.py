import requests
import time

class GraphAPI:
    def __init__(self, ad_acc, fb_api):
        self.base_url = "https://graph.facebook.com/v20.0/"
        self.api_fields = [
            "campaign_name","spend", "cpc", "cpm","ctr", "objective", "adset_name", 
            "adset_id", "clicks", "campaign_id", 
            "frequency", "date_start"
        ]
        self.token = fb_api
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

    def get_insights(self, level="campaign"):
        endpoint = f"act_{self.ad_acc}/insights"
        params = {"fields": ",".join(self.api_fields), "level": level}
        return self.make_request(endpoint, params)

    def get_campaigns_status(self):
        endpoint = f"act_{self.ad_acc}/campaigns"
        params = {"fields": "name,status,id"}
        return self.make_request(endpoint, params)

    def get_adset_status(self):
        endpoint = f"act_{self.ad_acc}/adsets"
        params = {"fields": "name,status,id"}
        return self.make_request(endpoint, params)

    def get_adset_insights(self):
        endpoint = f"act_{self.ad_acc}/adsets"
        params = {"fields": "name,insights"}
        return self.make_request(endpoint, params)

    def get_data_over_time(self, campaign_id):
        endpoint = f"{campaign_id}/insights"
        params = {
            "fields": ",".join(self.api_fields),
            "date_preset": "last_30d",
            "time_increment": "1"
        }
        return self.make_request(endpoint, params)

from .base import BaseCalculator
from collections import Counter

class AssetRatio(BaseCalculator):

    # TODO unique ip and sum of requests
    def total_requests(self, records: list[dict]) -> list[dict]:
        ip_minute_keys = []
        for record in records:
            if record["endpoint"]:
                ip_minute_key = f"{record["ip_address"]};{record["time"]}"
                ip_minute_keys.append(ip_minute_key)
        
        requests_per_key = []
        for key in ip_minute_keys:
            ip_address, *_ = key.split(';')
            count = ip_minute_keys.count(key)
            requests_per_key.append({"ip_address": ip_address, "total_requests": count})
        
        sum_req_per_key = Counter()
        for rk in requests_per_key:
            sum_req_per_key.update(rk)

        return sum_req_per_key

    def asset_requests(self, records: list[dict]) -> list[dict]:
        ip_minute_endpoint_end_keys = []
        for record in records:
            if record["endpoint"]:
                ip_minute_endpoint_end_key = f"{record["ip_address"]};{record["time"]};{record["endpoint"].split('.')[-1]}"
                ip_minute_endpoint_end_keys.append(ip_minute_endpoint_end_key)
        
        ip_endpoints = [] 
        assets_endings = ['css', 'js', 'png' ,'jpg' ,'jpeg' ,'gif' ,'ico' ,'woff' ,'woff2' ,'ttf']
        asset_requests = []
        for key in ip_minute_endpoint_end_keys:
            *_, endpoint_end = key.split(';')
            if endpoint_end in assets_endings:
                ip_address, _, endpoint = key.split(';')
                count = ip_minute_endpoint_end_keys.count(key)
                ip_endpoints.append({"ip_address": ip_address, "endpoint": endpoint})
        asset_requests = Counter(asset_req_ip["ip_address"] for asset_req_ip in ip_endpoints)
        return asset_requests

    def join_data_by_ip(self, total_requests: list[dict], asset_request: list[dict]) -> list[dict]:
        total_requests_indexed = {tr["ip_address"]: tr for tr in total_requests}

        for ar in asset_request:
            if ar["ip_address"] in total_requests_indexed:
                pass

    def calculate(self, records: list[dict] ) -> list[dict]:
        total_requests = self.total_requests(records)
        asset_requests = self.asset_requests(records)
        print(total_requests)

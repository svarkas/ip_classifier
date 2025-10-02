from .base import BaseCalculator
from collections import Counter

class AssetRatio(BaseCalculator):
    def calculate(self, records: list[dict] ) -> list[dict]:
        ip_minute_keys = []
        ip_minute_endpoint_end_keys = []
        for record in records:
            if record["endpoint"]:
                ip_minute_key = f"{record["ip_address"]};{record["time"]}"
                ip_minute_keys.append(ip_minute_key)
                ip_minute_endpoint_end_key = f"{ip_minute_key};{record["endpoint"].split('.')[-1]}"
                ip_minute_endpoint_end_keys.append(ip_minute_endpoint_end_key)
        
        total_requests = []
        for key in ip_minute_keys:
            ip_address, *_ = key.split(';')
            count = ip_minute_keys.count(key)
            total_requests.append({"ip_address": ip_address, "total_requests": count})
        
        ip_endpoints = [] 
        assets_endings = ['css', 'js', 'png' ,'jpg' ,'jpeg' ,'gif' ,'ico' ,'woff' ,'woff2' ,'ttf']
        for key in ip_minute_endpoint_end_keys:
            *_, endpoint_end = key.split(';')
            if endpoint_end in assets_endings:
                ip_address, _, endpoint = key.split(';')
                count = ip_minute_endpoint_end_keys.count(key)
                ip_endpoints.append({"ip_address": ip_address, "endpoint": endpoint})
        asset_requests = Counter(asset_req_ip["ip_address"] for asset_req_ip in ip_endpoints)
        print(asset_requests)

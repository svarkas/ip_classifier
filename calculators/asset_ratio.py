from .base import BaseCalculator

class AssetRatio(BaseCalculator):
    def calculate(self, records: list[dict] ) -> list[dict]:
        ip_minute_keys = []
        ip_minute_endpoint_end_keys = []
        for record in records:
            if record["endpoint"]:
                ip_minute_key = f"{record["ip_address"]};{record["time"]}"
                ip_minute_keys.append(ip_minute_key)
                ip_minute_endpoint_end_key = f"{ip_minute_key};{record["endpoint"].split('.')[-1]}"
                ip_minute_endpoint_end_keys.append(ip_minute_endpoint_end_keys)
        
        total_requests = []
        for key in ip_minute_keys:
            ip_address, *_ = key.split(';')
            count = ip_minute_keys.count(key)
            total_requests.append({"ip_address": ip_address, "total_requests": count})
        
        asset_requests = 
            for key in ip_minute_endpoint_end_keys:
            *_, endpoint_end = key.split(';')

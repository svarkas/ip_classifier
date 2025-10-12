from .base import BaseCalculator

class AssetRatio(BaseCalculator):

    # TODO unique ip and sum of requests
    def total_requests(self, records: list[dict]) -> dict:
        ip_minute_keys = []
        for record in records:
            if record["endpoint"]:
                ip_minute_key = f"{record["ip_address"]};{record["time"][0:17]}"
                ip_minute_keys.append(ip_minute_key)
        
        requests_per_key = []
        for key in ip_minute_keys:
            ip_address, *_ = key.split(';')
            count = ip_minute_keys.count(key)
            requests_per_key.append({"ip_address": ip_address, "total_requests": count})
        
        total_requests = {}
        for rk in requests_per_key:
            ip_address = rk["ip_address"]
            t_requests = rk["total_requests"]
            if ip_address in total_requests:
                total_requests[ip_address] += t_requests
            else:
                total_requests[ip_address] = t_requests

        return total_requests 

    def asset_requests(self, records: list[dict]) -> dict:
        ip_minute_endpoint_end_keys = []
        for record in records:
            if record["endpoint"]:
                ip_minute_endpoint_end_key = f"{record["ip_address"]};{record["time"][0:17]};{record["endpoint"].split('.')[-1]}"
                ip_minute_endpoint_end_keys.append(ip_minute_endpoint_end_key)
        
        ip_endpoints = [] 
        assets_endings = ['css', 'js', 'png' ,'jpg' ,'jpeg' ,'gif' ,'ico' ,'woff' ,'woff2' ,'ttf']
        for key in ip_minute_endpoint_end_keys:
            *_, endpoint_end = key.split(';')
            if endpoint_end in assets_endings:
                ip_address, _, endpoint = key.split(';')
                ip_endpoints.append({"ip_address": ip_address, "endpoint": endpoint})
        
        asset_requests = {}
        for ie in ip_endpoints:
            ip_address = ie["ip_address"]
            if ip_address in asset_requests:
                asset_requests[ip_address] += 1
            else:
                asset_requests[ip_address] = 1
        return asset_requests

    def join_data_by_ip(self, total_requests: dict, asset_request: dict)-> list[tuple[str, int, int]]:
        return [(ip, total_requests.get(ip), asset_request.get(ip)) for ip in total_requests | asset_request]

    def calculate(self, records: list[dict] ) -> list[dict]:
        '''
        TODO: the actual asset ratio calculation
        '''
        total_requests = self.total_requests(records)
        asset_requests = self.asset_requests(records)
        print(self.join_data_by_ip(total_requests, asset_requests))

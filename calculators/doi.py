from .base import BaseCalculator
import re

class Doi(BaseCalculator):
    def endpoints_to_doi(self, records: list[dict]) -> list[dict]:
        pattern = r'/10.3892/[a-z]{2,4}\.[0-9]{1,4}\.[0-9]{1,4}'
        for record in records:
            doi_match = re.match(pattern, record["endpoint"])
            if doi_match:
                record["endpoint"] = doi_match.group()
            else:
                record["endpoint"] = None
        return records

    def calculate(self, records: list[dict]) -> list[dict]:
        records = self.endpoints_to_doi(records)
        keys = []
        for record in records:
            if record["endpoint"]:
                ip_minute_endpoint_key = f"{record["ip_address"]};{record["time"]};{record["endpoint"]}"
                keys.append(ip_minute_endpoint_key)
        
        results = []
        for k in set(keys):
            ip_address, *_ = k.split(';')
            results.append({ip_address: keys.count(k)})
        results = sorted(results, key=lambda d: list(d.values())[0])
        print(results)
        return results

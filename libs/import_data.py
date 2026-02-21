from typing import Optional
import re 

class Importer:

    def is_bot(self, uagent: str) -> bool:
        pattern=r'bot|spider|crawl'
        if bool(re.search(pattern, uagent, flags=re.IGNORECASE)):
            return True
        return False

        
    def read_log(self, file:str, records_count : Optional[int] = 1000) -> list[dict]:
        records = []
        count = 0
        with open(file, 'r') as fr:
            for line in fr.readlines():
                count += 1
                if count == records_count:
                    break

                try:
                    line_splitted = line.split(' ')
                    ip, _, _, time, _, method, endpoint, protocol, result, size, referrer, uagent, *_  = line_splitted 
                    uagent = " ".join(line_splitted[11:-1])
                    time = time[0:25].strip('[]')
                    if not self.is_bot(uagent): 
                        records.append({
                            "ip_address":ip,
                            "time": time,
                            "method": method,
                            "endpoint": endpoint,
                            "protocol": protocol,
                            "http_result": result,
                            "size": size,
                            "referrer": referrer,
                            "user_agent": uagent
                        })
                except ValueError as ve:
                    print(f"not enough values ERROR: {ve}")
        return records 

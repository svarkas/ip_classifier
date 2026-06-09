import ipinfo

def get_ip_country_code(ip:str) -> str:
    access_token= "f9f2aca790d783"

    handler = ipinfo.getHandler(access_token)
    data = handler.getDetails(ip)
    return data.details.get("country")

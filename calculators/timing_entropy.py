from .base import BaseCalculator
import pandas as pd
import sys

class TimingEntropy(BaseCalculator):

    def calculate(self, records: list[dict]) -> None:
        records_df = pd.DataFrame(records)  
        records_df["time"] = pd.to_datetime(records_df["time"], format='%d/%b/%Y:%H:%M:%S' )
        records_df["unix_time"] = records_df["time"].astype('int64')
        records_df = records_df.sort_values(["ip_address", "time"])
        records_grouped = records_df.groupby("ip_address")
        ip_deltas = {}
        for ip_address, ip_data in records_grouped:
            ip_deltas[ip_address] = [ip_data["unix_time"][i] - ip_data["unix_time"][i-1] for i in range(1, len(ip_data), 1)]
        print(ip_deltas)

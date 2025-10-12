from .base import BaseCalculator
import pandas as pd

class TimingEntropy(BaseCalculator):

    def calculate(self, records: list[dict]) -> None:
        records_df = pd.DataFrame(records)  
        records_df["time"] = pd.to_datetime(records_df["time"], format='%d/%b/%Y:%H:%M:%S' )
        records_df = records_df.sort_values(["ip_address", "time"])
        records_grouped = records_df.groupby("ip_address")

        for ip_address, group in records_grouped:
            print(f"IP:{ip_address}")
            print(group, "\n")

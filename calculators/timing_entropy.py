from .base import BaseCalculator
import pandas as pd
import sys
from typing import Optional
import numpy as np
import numpy.typing as npt

class TimingEntropy(BaseCalculator):

    def calculate_deltas(self, ips_with_data: pd.DataFrame) -> dict:
        ip_deltas = {}
        for ip_address, ip_data in ips_with_data:
            utime_lst = list(ip_data["unix_time"])
            delta_lst = []
            if len(utime_lst) > 1:
                # divide by 1e9 to convert nanoseconds to seconds
                ip_deltas[ip_address] = [(utime_lst[i] - utime_lst[i-1]) / 1e9 for i in range(1, len(utime_lst), 1)]
            else:
                ip_deltas[ip_address] = []
        return ip_deltas

    def calculate_probabilities(self, deltas: dict) -> dict:
        ip_prob = {}
        for ip, deltas in deltas.items():
            deltas_count = len(deltas)
            small = 0
            medium = 0
            big = 0
            probs = []
            if deltas_count > 0:
                for d in deltas:
                    if d <= 0.3:
                        small += 1
                    elif 0.3 < d <= 0.6:
                        medium += 1
                    else:
                        big += 1
                probs.append(small/deltas_count)
                probs.append(medium/deltas_count)
                probs.append(big/deltas_count)
            ip_prob[ip] = probs
        return ip_prob

    def shannon_entropy(self, probabilities: dict) -> dict:
        shannon_entropies = {}
        for ip, probs in probabilities.items():
            probs = np.array(probs)
            probs = probs[probs >0]
            shannon_entropies[ip] = -np.sum(probs * np.log2(probs))
        #for ip, probs in probabilities.items():
        #    if probs:
        #        sums = 0
        #        for p in probs:
        #            if p > 0:
        #                sums += p*np.log2(p)
        #        shannon_entropies[ip] = -sums
        return shannon_entropies

    # when deltas very irregular probably human, when deltas very regular probably bot
    def calculate(self, records: list[dict]) -> None:
        records_df = pd.DataFrame(records) 
        records_df["time"] = pd.to_datetime(records_df["time"], format='%d/%b/%Y:%H:%M:%S.%f' )
        records_df["unix_time"] = records_df["time"].astype('int64')
        records_df = records_df.sort_values(["ip_address", "time"])
        records_grouped = records_df.groupby("ip_address")
        deltas = self.calculate_deltas(records_grouped)
        probabilities = self.calculate_probabilities(deltas)
        return self.shannon_entropy(probabilities)

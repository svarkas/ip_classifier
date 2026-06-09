import sys
import os
from libs.import_data import Importer
from calculators.doi import Doi
from calculators.asset_ratio import AssetRatio
from calculators.timing_entropy import TimingEntropy
from copy import deepcopy
import pandas as pd 
from libs.rt_tree import RTtree
from libs.ip_info import get_ip_country_code
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from random import randrange

def compine_features(doi_variance: dict, assets_ratio: dict, time_entropy: dict) -> pd.DataFrame:
    features_df = pd.DataFrame({
        "doi_variance": doi_variance,
        "assets_ratio": assets_ratio,
        "time_entropy": time_entropy
    })
    features_df = features_df.reset_index()
    features_df.rename(columns={"index": "ip"}, inplace=True)
    features_df.fillna(0, inplace = True)
    print(len(features_df)) 
    # Return only the records where all futures are > 0
    filtered = features_df[(features_df[["doi_variance", "assets_ratio", "time_entropy"]]>0).all(axis=1)]
    print(len(filtered)) 
    return filtered

def predict(node, features):
    if node.label is not None:
        return node.label

    value = features[node.feature]

    if value <= node.threshold:
        return predict(node.left, features)
    else:
        return predict(node.right, features)

def process(ip: str) -> Optional[dict]:
    country_code = get_ip_country_code(ip)
    if country_code is None:
        return None

    return {
        "ip": ip,
        "country_code": country_code
    }

def geolocate_records_out(records:list[dict]):
    with ThreadPoolExecutor(max_workers=8) as executor, open("data/ip_country.jsonl", "w", encoding="utf-8") as fw:

        futures = [executor.submit(process, r["ip_address"]) for r in records]
        
        for future in as_completed(futures):
            row = future.result()
            if row is not None:
                fw.write((json.dumps(row, ensure_ascii=False) + "\n"))

def geolocate_records_df(records: list[dict]):
    ip_df = pd.DataFrame({
        "ip": [r["ip_address"] for r in records],
        "country": [geolocate_ip(r["ip_address"]) for r in records]
    })
    print(ip_df)

def sample(records: list[dict], count: int, max: int) -> list[dict]:
    samples = []
    for i in range(0, count, 1):
        samples.append(records[randrange(len(records)-1)])
    return samples

def main(argv):
    importer = Importer()
    records = importer.read_log(argv[1], 100000)
    records = sample(deepcopy(records), 1000, 1000)
    geolocate_records_out(records)
    exit()

    dc = Doi()
    doi_variance = dc.calculate(deepcopy(records))
    arc = AssetRatio()
    assets_ratio = arc.calculate(deepcopy(records))
    tec = TimingEntropy()
    time_entropy = tec.calculate(deepcopy(records))
    features_df = compine_features(doi_variance, assets_ratio, time_entropy)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
  
    rt = RTtree()
    tree = rt.rt_tree()
    for index, feat in features_df.iterrows():
        print(feat["ip"], predict(tree, feat))

if __name__ == "__main__":
    main(sys.argv)

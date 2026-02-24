import sys
import os
from libs.import_data import Importer
from calculators.doi import Doi
from calculators.asset_ratio import AssetRatio
from calculators.timing_entropy import TimingEntropy
from copy import deepcopy
import pandas as pd 

def compine_features(doi_variance: dict, assets_ratio: dict, time_entropy) -> pd.DataFrame:
    features = {}
    all_ips = set(doi_variance) | set(assets_ratio) | set(time_entropy)
    for ip in all_ips:
        features[ip] = {
            doi_variance.get(ip, 0),
            assets_ratio.get(ip, 0),
            time_entropy.get(ip, 0)
        }
    features_df = pd.DataFrame.from_dict(features , orient="index")
    features_df.reset_index(inplace = True)
    features_df.rename(columns={"index": "ip"}, inplace = True)
    return features_df

def main(argv):
    importer = Importer()
    records = importer.read_log(argv[1], 2000)
    dc = Doi()
    doi_variance = dc.calculate(deepcopy(records))
    arc = AssetRatio()
    assets_ratio = arc.calculate(deepcopy(records))
    tec = TimingEntropy()
    time_entropy = tec.calculate(deepcopy(records))
    print(compine_features(doi_variance, assets_ratio, time_entropy))

if __name__ == "__main__":
    main(sys.argv)

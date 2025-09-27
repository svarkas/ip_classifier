import sys
import os
from libs.import_data import Importer
from calculators.doi import Doi
from calculators.asset_ratio import AssetRatio

def main(argv):
    importer = Importer()
    records = importer.read_log(argv[1], 1000)
    dc = Doi()
    dc.calculate(records)
    arc = AssetRatio()
    arc.calculate(records)

if __name__ == "__main__":
    main(sys.argv)

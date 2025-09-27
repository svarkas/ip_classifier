import sys
import os
from libs.import_data import Importer
from calculators.doi import Doi
from calculators.asset_ratio import AssetRatio
from copy import deepcopy

def main(argv):
    importer = Importer()
    records = importer.read_log(argv[1], 2000)
    dc = Doi()
    dc.calculate(deepcopy(records))
    arc = AssetRatio()
    arc.calculate(deepcopy(records))

if __name__ == "__main__":
    main(sys.argv)

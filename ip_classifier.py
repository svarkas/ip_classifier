import sys
import os
from libs.import_data import Importer

def main(argv):
    importer = Importer()
    records = importer.read_log(argv[1])
    for record in records:
        print(record["ip_address"])

if __name__ == "__main__":
    main(sys.argv)

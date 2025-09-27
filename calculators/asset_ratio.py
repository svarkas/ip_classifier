from .base import BaseCalculator

class AssetRatio(BaseCalculator):
    def calculate(self, records: list[dict] ) -> list[dict]:
        for record in records:
            print(record["endpoint"])

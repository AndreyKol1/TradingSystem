import csv
from functools import lru_cache
from typing import Set 

@lru_cache 
def load_valid_symbols() -> Set[str]:
    with open("app/data/cryptocurrency_list.csv", newline="") as f:
        reader = csv.DictReader(f)
        return {row["from_currency"].upper() for row in reader}


def validate_cryptocurr(currency: str) -> None:
    available_curr = load_valid_symbols()
    if currency not in available_curr:
        raise ValueError(f"Invalid crypto name: {currency}")


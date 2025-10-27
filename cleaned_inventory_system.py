
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(h)
logger.setLevel(logging.INFO)

# Module-level inventory mapping. Kept intentionally as a single shared
# structure to mirror the original program structure, but access is validated.
stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> None:
    """Add qty to item in stock_data; create item if not present.

    Args:
        item: non-empty string name of the item.
        qty: positive integer quantity to add.
        logs: optional list to append a human-readable operation entry.

    Raises:
        TypeError, ValueError on invalid inputs.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an int")
    if qty <= 0:
        raise ValueError("qty must be positive")

    prev = stock_data.get(item, 0)
    stock_data[item] = prev + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logger.info("Added %d of %s (was %d)", qty, item, prev)


def remove_item(item: str, qty: int) -> None:
    """Remove qty of item from stock_data. If remaining <= 0, item is removed.

    Raises KeyError if item is not present. Raises TypeError/ValueError on
    invalid inputs.
    """
    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    if not isinstance(qty, int):
        raise TypeError("qty must be an int")
    if qty <= 0:
        raise ValueError("qty must be positive")

    if item not in stock_data:
        raise KeyError(f"item '{item}' not found in inventory")

    if qty >= stock_data[item]:
        logger.info("Removing item %s from inventory (requested %d, had %d)", item, qty, stock_data[item])
        del stock_data[item]
    else:
        stock_data[item] -= qty
        logger.info("Decreased %s by %d (now %d)", item, qty, stock_data[item])


def get_qty(item: str) -> int:
    """Return quantity for item. Returns 0 if item is not present.

    Raises TypeError if item is invalid.
    """
    if not isinstance(item, str) or not item:
        raise TypeError("item must be a non-empty string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory JSON from file into module-level `stock_data`.

    If the file does not exist the function leaves `stock_data` empty. If the
    file contents are invalid JSON or the structure is not a mapping of
    str->int, a ValueError is raised.
    """
    path = Path(file)
    global stock_data
    if not path.exists():
        logger.info("Inventory file %s not found; starting with empty inventory", file)
        stock_data = {}
        return

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        logger.exception("Failed to decode JSON from %s", file)
        raise ValueError("invalid JSON in inventory file") from exc

    if not isinstance(data, dict):
        raise ValueError("inventory file must contain a JSON object mapping item->qty")

    normalized: Dict[str, int] = {}
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, int):
            raise ValueError("inventory file contains invalid types; expected str->int mapping")
        normalized[k] = v

    stock_data = normalized
    logger.info("Loaded inventory from %s (%d items)", file, len(stock_data))


def save_data(file: str = "inventory.json") -> None:
    """Save the current inventory to a JSON file using a context manager."""
    path = Path(file)
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(stock_data, f, ensure_ascii=False, indent=2)
        logger.info("Saved inventory to %s", file)
    except Exception:
        logger.exception("Failed to save inventory to %s", file)
        raise


def print_data() -> None:
    print("Items Report")
    for k in sorted(stock_data.keys()):
        print(k, "->", stock_data[k])


def check_low_items(threshold: int = 5) -> List[str]:
    if not isinstance(threshold, int):
        raise TypeError("threshold must be an int")
    return [k for k, v in stock_data.items() if v < threshold]


def main() -> None:
    # Demonstration of safe usage. The original example had invalid calls
    # (negative quantities, wrong types and eval); those are removed.
    try:
        add_item("apple", 10)
        add_item("banana", 2)
        remove_item("apple", 3)
        print("Apple stock:", get_qty("apple"))
        print("Low items:", check_low_items())
        save_data()
        # load_data()  # uncomment to reload from disk
        print_data()
    except Exception as exc:
        logger.exception("Error during example run: %s", exc)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the public product catalog before GitHub Pages deployment."""
import json
import re
import sys
from pathlib import Path

path = Path("zarrin-arman/products.json")
try:
    products = json.loads(path.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"Catalog JSON parse error: {exc}")
    sys.exit(1)

if not isinstance(products, list):
    print("Catalog must be a JSON array.")
    sys.exit(1)

required = ("name", "category", "price", "weight", "karat", "image")
seen = set()
errors = []
for i, product in enumerate(products, start=1):
    if not isinstance(product, dict):
        errors.append(f"Item {i}: expected object")
        continue
    for key in required:
        if key not in product:
            errors.append(f"Item {i}: missing {key}")
    name = product.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"Item {i}: name must be non-empty text")
    elif name in seen:
        errors.append(f"Item {i}: duplicate product name {name!r}")
    else:
        seen.add(name)
    price = product.get("price")
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        errors.append(f"Item {i}: price must be a non-negative number")
    image = product.get("image", "")
    if image and (not isinstance(image, str) or not re.match(r"^https://", image)):
        errors.append(f"Item {i}: image must be an https URL or empty")
    for field in ("category", "weight", "karat"):
        if not isinstance(product.get(field), str):
            errors.append(f"Item {i}: {field} must be text")
    if "featured" in product and not isinstance(product["featured"], bool):
        errors.append(f"Item {i}: featured must be true/false")

if errors:
    print("Catalog validation failed:")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print(f"Catalog validation passed: {len(products)} product(s).")

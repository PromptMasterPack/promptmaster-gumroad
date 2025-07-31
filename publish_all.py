import os
import json
import requests

# Variables d'environnement (GitHub Actions secrets)
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")
NICHES_FILE = "niches.json"
ASSETS_DIR = "assets"
API_BASE = "https://api.gumroad.com/v2/products"

def load_niches():
    with open(NICHES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_niches(niches):
    with open(NICHES_FILE, "w", encoding="utf-8") as f:
        json.dump(niches, f, ensure_ascii=False, indent=2)

def publish(entry):
    file_path = os.path.join(ASSETS_DIR, f"PromptMaster_{entry['niche'].replace(' ', '_')}.pdf")
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {
            "access_token": GUMROAD_TOKEN,
            "name": f"PromptMaster Pack – {entry['niche']}",
            "price": "900",  # 9 € en centimes
            "visibility": "public",
            "description": f"50 prompts ChatGPT spécialisés pour {entry['niche']}.",
            "tags": ",".join(["ChatGPT", "prompts", entry['niche'].split()[1]])
        }
        if entry.get("product_id"):
            data["product_id"] = entry["product_id"]
            url = f"{API_BASE}/update"
        else:
            url = f"{API_BASE}/create"
        resp = requests.post(url, data=data, files=files)
        resp.raise_for_status()
        product = resp.json().get("product", {})
        return product.get("id")

def main():
    niches = load_niches()
    changed = False
    for entry in niches:
        prod_id = publish(entry)
        if entry.get("product_id") != prod_id:
            entry["product_id"] = prod_id
            changed = True
            print(f"Set product_id for {entry['niche']}: {prod_id}")
    if changed:
        save_niches(niches)
        print("niches.json mis à jour.")

if __name__ == "__main__":
    main()

import requests
import pandas as pd
URL = "https://dash.alhusnainmotors.co.ke/api/chatbot/vehicles/all" 

HEADERS = {
    "Authorization": "Bearer iu6EjbJhv4iy2xTkLR0pS3HbGi309I33vBlU9A0R",
    "Accept": "application/json",
}

# ---------------------------
# FETCH DATA
# ---------------------------
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

response_json = response.json()

if isinstance(response_json, dict) and "data" in response_json:    
    vehicles = response_json["data"]
elif isinstance(response_json, list):
    vehicles = response_json
else:
    raise ValueError("Unexpected API response structure")

# ---------------------------
# NORMALIZE DATA
# ---------------------------
rows = []

for v in vehicles:
    if not isinstance(v, dict):
        continue

    # Safe nested objects
    make = v.get("make") or {}
    model = v.get("model") or {}
    make = v.get("make") or {}
    model = v.get("model") or {}
    chassis = v.get("chassis_no") or {}
    specs = v.get("specifications") or {}
    location = v.get("location") or {}

    # FEATURES
    features_list = v.get("features") or []
    features = ", ".join(
        f.get("name") for f in features_list if isinstance(f, dict)
    )

    # YEAR / MONTH
    year_month_raw = specs.get("year_with_month") or "0/0"
    year_month = int(year_month_raw.replace("/", "")) if "/" in year_month_raw else None

    # STOCK ID
    slug = v.get("slug", "")
    stock_id = slug.split("-")[-1] if slug else None

    row = {
        "MAKE": make.get("name"),
        "MODEL": model.get("name"),
        "GRADE": v.get("grade") or "N/A",
        "CHASSIS NO": str(chassis.get("last_5_digits")) if chassis.get("last_5_digits") else None,
        "STOCK_ID": stock_id,
        "COLOUR": specs.get("color"),
        "IMAGE_URL": "",
        "ENGINE CC": specs.get("engine_cc"),
        "MILEAGE": specs.get("mileage"),
        "YEAR/MONTH": year_month,
        "LOCATION": location.get("name"),
        "PRICE": 0,
        "FEATURES": features if features else None,
        "YEAR": int(specs.get("year")) if specs.get("year") else None,
        "MAKE_MODEL": f"{make.get('name')} {model.get('name')}",   
    }

    rows.append(row)

# ---------------------------
# DATAFRAME
# ---------------------------
df = pd.DataFrame(rows)

df = df[
    [
        "MAKE",
        "MODEL",
        "GRADE",
        "CHASSIS NO",
        "STOCK_ID",
        "COLOUR",
        "IMAGE_URL",
        "ENGINE CC",
        "MILEAGE",
        "YEAR/MONTH",
        "LOCATION",
        "PRICE",
        "FEATURES",
        "YEAR",
        "MAKE_MODEL",
    ]
]

# ---------------------------
# EXPORT
# ---------------------------
df.to_csv("vehicles.csv", index=False)

print(df.info())
print("\n✅ CSV saved as vehicles.csv")
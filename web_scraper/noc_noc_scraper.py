import requests
import time  # ใช้สำหรับใส่ delay ถ้าจำเป็น
import json  # Import the json module

url = "https://nocnoc.com/buyer-service/search?b-uid=1.0.1"

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,th;q=0.8",
    "authorization": "Bearer YOUR_ACCESS_TOKEN_HERE",  # เปลี่ยนตรงนี้
    "content-type": "application/json; charset=utf-8",
    "origin": "https://nocnoc.com",
    "referer": "https://nocnoc.com/th/pl/furniture-666?area=bc-navigation",
    "user-agent": "Mozilla/5.0",
    "x-nocnoc-device-id": "example-device-id",
    "x-nocnoc-platform": "web"
}


page = 1
all_items = []

while True:
    print(f"🔄 Fetching page {page}...")
    payload_text = '{"lang":"th","userType":"BUYER","locale":"th","orgIdfier":"scg","f":[{"field":"primaryCategory.o_id","type":"subcategory3","codes":["1759760"]}],"limit":2000,"page":2,"transformData":true,"searchListMetaInfo":{"nocNocChoiceLimit":8,"comingSoonLimit":8,"collapsedView":true,"totalRegularItems":1306,"totalComingSoonItems":null,"totalNocNocChoiceItems":null,"nocSort":null},"abType":"B","sort":"rel"}'
    payload = json.loads(payload_text)
    payload["page"] = page


    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code)

    data = response.json()


    items = data.get("items", [])
    print(len(items))
    with open(f"page_{page}.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)
    
    if not items:
        print("✅ No more items found. Finished.")
        break

    all_items.extend(items)
    page += 1
    time.sleep(1)  # หยุด 1 วินาที เพื่อไม่ให้ยิงเร็วเกินไป

print(f"🎉 Total items fetched: {len(all_items)}")

# Save all_items to a JSON file
output_file = "all_items.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=4)

print(f"📁 Data saved to {output_file}")

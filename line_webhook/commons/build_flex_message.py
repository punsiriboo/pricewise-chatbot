import re
from commons.vertex_ai_search import vertex_ai_search
from linebot.v3.messaging import (
    FlexContainer
)

def data_extract_and_search(gemini_reponse):
    
    pattern = r'"product":\s*"([^"]+)",\s*"price":\s*([\d.]+),\s*"quantity":\s*(\d+)'

    matches = re.findall(pattern, gemini_reponse)

    # แปลงเป็น list of dict
    extract_results = [
        {"product": m[0], "price": float(m[1]), "quantity": int(m[2])}
        for m in matches
    ]
    print(extract_results)

    all_search_item_list = []
    for item_no,item in enumerate(extract_results):
        print("="*40)
        search_product = item['product']
        original_price = item['price']
        gemini_summary_text, search_results = vertex_ai_search(search_product)
        print(gemini_summary_text)
        print(search_results)


        all_items_list = []
        price_all = []
        for item in search_results:
            structData = item["document"]["structData"]
            product_name = structData["title"]
            product_image_url = structData["image"]
            price = structData["price"]["price"]
            price_all.append(price)

            with open("templates/product_item.json") as file:
                product_item = file.read()
                
            price_diff = original_price - price
            price_diff_text = f"{price_diff:+,.2f}"

            product_item_with_data = (
                product_item
                .replace("<PRODUCT_IMG>", product_image_url)
                .replace("<PRODUCT_NAME>", product_name)
                .replace("<PRICE>", str(price))
                .replace("<PRICE_DIFF>", price_diff_text)
            )
            all_items_list.append(product_item_with_data)


        all_items_list_text = ",".join(all_items_list)

        with open("templates/product_bubble.json") as file:
            product_bubble = file.read()
        
        average_price = sum(price_all) / len(price_all)
        analyse_color = "#ff0000" if original_price > average_price else "#00ff00"
        percent_diff = ((original_price - average_price) / average_price) * 100
        analysis_text = (
            f"overpriced (+{percent_diff:.2f}%)"
            if original_price > average_price
            else f"underpriced ({percent_diff:.2f}%)"
        )
        product_search_bubble = (
            product_bubble
            .replace("<ITEM_NO>", str(item_no+1))
            .replace("<PRODUCT_ITEMS>", all_items_list_text)
            .replace("<ORIGINAL_PRODUCT>", search_product)
            .replace("<ORIGINAL_PRICE>", str(original_price))
            .replace("<AVG_PRICE>", str(average_price))
            .replace("<ANALYSE>", analysis_text)
            .replace("<ANALYSE_COLOR>", analyse_color)
        )
        print("*"*100)
        print(product_search_bubble)
        all_search_item_list.append(FlexContainer.from_json(product_search_bubble))

    return all_search_item_list
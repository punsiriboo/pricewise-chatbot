import json

def filter_columns(item):
    """
    กรองเฉพาะคอลัมน์ที่ต้องการ (title, image, price)
    
    Args:
        item (dict): ข้อมูลแต่ละรายการ
    
    Returns:
        dict: ข้อมูลที่กรองแล้ว
    """
    return {
        'title': item.get('title', ''),
        'image':  'https://cdn.nocnoc.com/assets-static/assets' + item.get('image', ''),
        'price': item.get('price', '')
    }
def convert_to_ndjson(data_list, output_file):
    """
    แปลงข้อมูลเป็นรูปแบบ NDJSON และบันทึกลงไฟล์
    
    Args:
        data_list (list): รายการข้อมูลที่จะแปลง
        output_file (str): ชื่อไฟล์ที่ต้องการบันทึก
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data_list:
            # กรองคอลัมน์ที่ต้องการ
            filtered_item = filter_columns(item)
            # เขียนแต่ละรายการในรูปแบบ JSON และเพิ่ม newline
            f.write(json.dumps(filtered_item, ensure_ascii=False) + '\n')

def read_ndjson(input_file):
    """
    อ่านข้อมูลจากไฟล์ NDJSON
    
    Args:
        input_file (str): ชื่อไฟล์ NDJSON ที่ต้องการอ่าน
    
    Returns:
        list: รายการข้อมูลที่อ่านได้
    """
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # ตรวจสอบว่าไม่ใช่บรรทัดว่าง
                data.append(json.loads(line))
    return data

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    # โหลดข้อมูลจากไฟล์ page_1.json
    with open('page_1.json', 'r', encoding='utf-8') as f:
        sample_data = json.load(f)
    
    # แปลงและบันทึกเป็นไฟล์ NDJSON
    output_file = "output.ndjson"
    convert_to_ndjson(sample_data, output_file)
    print("แปลงข้อมูลเป็น NDJSON เรียบร้อยแล้ว!")
    
    # อ่านข้อมูลจากไฟล์ NDJSON
    print("\nอ่านข้อมูลจากไฟล์ NDJSON:")
    read_data = read_ndjson(output_file)
    for item in read_data:
        print(json.dumps(item, ensure_ascii=False, indent=2)) 
# การใช้ uv เป็น Package Manager

uv เป็น package manager ที่เร็วและทันสมัยสำหรับ Python โดยมีประสิทธิภาพสูงกว่า pip มาตรฐาน

## การติดตั้ง uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## การใช้งานพื้นฐาน

### การติดตั้ง package
```bash
uv pip install package_name
```

### การติดตั้ง package จาก requirements.txt
```bash
uv pip install -r requirements.txt
```

### การสร้าง virtual environment
```bash
uv venv
```

### การใช้งาน virtual environment
```bash
source .venv/bin/activate  # บน Unix/macOS
.venv\Scripts\activate     # บน Windows
```

### การอัปเดต package
```bash
uv pip install --upgrade package_name
```

### การลบ package
```bash
uv pip uninstall package_name
```

## ข้อดีของ uv
- ความเร็วในการติดตั้ง package ที่สูงกว่า pip มาตรฐาน
- การจัดการ dependencies ที่มีประสิทธิภาพ
- การรองรับการทำงานแบบ parallel
- การใช้ disk space ที่มีประสิทธิภาพ

## การใช้งานร่วมกับ requirements.txt
uv สามารถทำงานร่วมกับไฟล์ requirements.txt ได้เหมือนกับ pip ทุกประการ

```bash
uv pip install -r requirements.txt
```

## การใช้งานร่วมกับ virtual environment
uv มีคำสั่งสำหรับการจัดการ virtual environment ที่ใช้งานง่าย

```bash
# สร้าง virtual environment
uv venv

# เปิดใช้งาน virtual environment
source .venv/bin/activate  # บน Unix/macOS
.venv\Scripts\activate     # บน Windows

# ติดตั้ง package ใน virtual environment
uv pip install package_name
```

## การอัปเดต uv
```bash
uv pip install --upgrade uv
```

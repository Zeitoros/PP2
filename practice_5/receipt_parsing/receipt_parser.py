import re
import json

def parse_receipt_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        parsed_data = {
            "merchant": "EUROPHARMA",
            "date_time": None,
            "payment_method": None,
            "total_amount": 0.0,
            "items": []
        }

        date_match = re.search(r'(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})', content)
        if date_match:
            parsed_data["date_time"] = date_match.group(1)

        if "Банковская карта" in content:
            parsed_data["payment_method"] = "Bank Card"
 
        total_match = re.search(r'ИТОГО:\s*([\d\s,.]+)', content)
        if total_match:
            total_str = total_match.group(1).replace("\xa0", "").replace(" ", "").replace(",", ".")
            parsed_data["total_amount"] = float(total_str)

        item_pattern = re.compile(
            r'\d+\.\s*\n(.*?)\n(?:\\s*)?([\d,]+)\s*x\s*([\d\s,.]+)\n([\d\s,.]+)', 
            re.DOTALL
        )

        matches = item_pattern.findall(content)
        
        for match in matches:
            name = match[0].strip().replace('\n', ' ')
            qty = float(match[1].replace(',', '.'))
            unit_price = float(match[2].replace('\xa0', '').replace(' ', '').replace(',', '.'))
            subtotal = float(match[3].replace('\xa0', '').replace(' ', '').replace(',', '.'))

            parsed_data["items"].append({
                "product_name": name,
                "quantity": qty,
                "unit_price": unit_price,
                "subtotal": subtotal
            })

        return parsed_data

    except FileNotFoundError:
        return {"Error": "Файл raw.txt не найден."}

file_name = 'practice_5/receipt_parsing/raw.txt'
result = parse_receipt_from_file(file_name)

print(json.dumps(result, indent=4, ensure_ascii=False))
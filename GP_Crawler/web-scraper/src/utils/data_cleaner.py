def clean_data(raw_data):
    cleaned_data = []
    for item in raw_data:
        # Assuming item is a dictionary with keys 'title', 'price', and 'description'
        cleaned_item = {
            'title': item.get('title', '').strip(),
            'price': item.get('price', '').strip(),
            'description': item.get('description', '').strip()
        }
        cleaned_data.append(cleaned_item)
    return cleaned_data
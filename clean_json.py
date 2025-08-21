import json

# Replace with your JSON file
input_file = 'sneakers_fixed.json'
output_file = 'sneakers_clean.json'

# Models to keep
allowed_models = [
    'store.sneaker',
    'store.sneakersize',
    'store.sneakerimage'
]

with open(input_file, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

cleaned_data = [entry for entry in data if entry['model'] in allowed_models]

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, indent=4)

print(f"Cleaned fixture saved as {output_file}")

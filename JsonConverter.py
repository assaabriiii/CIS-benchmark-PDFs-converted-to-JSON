import os
import json
from bs4 import BeautifulSoup
import re

def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        custom_items = {}
        item_counter = 1
        
        for custom_item in soup.find_all('item'):
            item_dict = {}
            tag_value = custom_item.get_text(strip=True)
            
            # Extract key-value pairs within the tag value, allowing values to contain double quotes
            matches = re.findall(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"', tag_value)
            for key, value in matches:
                item_dict[key] = value.replace('\\"', '"')  # Handle escaped quotes within the value
            
            custom_items[f'custom_item_{item_counter}'] = item_dict
            item_counter += 1
        
        for custom_item in soup.find_all('custom_item'):
            item_dict = {}
            tag_value = custom_item.get_text(strip=True)
            
            # Extract key-value pairs within the tag value, allowing values to contain double quotes
            matches = re.findall(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"', tag_value)
            for key, value in matches:
                item_dict[key] = value.replace('\\"', '"')  # Handle escaped quotes within the value
            
            custom_items[f'custom_item_{item_counter}'] = item_dict
            item_counter += 1
        
        return custom_items

def process_audit_files(base_directory):
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.audit'):
                file_path = os.path.join(root, file)
                custom_items_dict = parse_html_file(file_path)
                
                # Create corresponding JSON file path
                json_file_path = os.path.splitext(file_path)[0] + '.json'
                
                # Write the dictionary to a JSON file
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(custom_items_dict, json_file, ensure_ascii=False, indent=4)
                
                print(f"Processed {file_path} and saved to {json_file_path}")

# Base directory containing the 'portal_audits' folder
base_directory = 'portal_audits_main'
process_audit_files(base_directory)

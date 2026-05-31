import json
import xml.etree.ElementTree as ET
import os
import glob

def parse_svg(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    pieces = {}
    for polygon in root.findall('{http://www.w3.org/2000/svg}polygon'):
        pid = polygon.get('id')
        points = polygon.get('points')
        pieces[pid] = points
    return pieces

def prepare_dataset(json_path, svg_dir, limit=20):
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    dataset = []
    count = 0
    for key, value in data.items():
        if count >= limit:
            break
        
        svg_path = os.path.join(svg_dir, f"{key}.svg")
        if not os.path.exists(svg_path):
            continue
            
        pieces_coords = parse_svg(svg_path)
        
        # Take the first annotation
        if not value['annotations']:
            continue
            
        annotation = value['annotations'][0]
        whole_name = annotation['whole']['wholeAnnotation']
        part_mapping = annotation['part']
        
        # Group pieces by part name
        parts = {}
        for pid, part_name in part_mapping.items():
            if part_name not in parts:
                parts[part_name] = []
            if pid in pieces_coords:
                parts[part_name].append(pieces_coords[pid])
        
        dataset.append({
            'id': key,
            'whole_name': whole_name,
            'parts': parts
        })
        count += 1
        
    return dataset

if __name__ == "__main__":
    JSON_PATH = "code/kilogram/dataset/full.json"
    SVG_DIR = "code/kilogram/dataset/tangrams-svg"
    
    dataset = prepare_dataset(JSON_PATH, SVG_DIR, limit=50)
    
    with open("results/processed_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Processed {len(dataset)} shapes.")

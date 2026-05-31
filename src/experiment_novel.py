import json
import os
import random
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt, model="gpt-4o"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling API: {e}")
        return None

def format_shape_novel(shape, novel_name):
    res = f"Object: {novel_name}\n"
    for part_name, coords_list in shape['parts'].items():
        coords_str = " | ".join(coords_list)
        res += f"{part_name}: {coords_str}\n"
    return res

def get_min_y(coords_list):
    ys = []
    for s in coords_list:
        points = s.split()
        for p in points:
            try: ys.append(float(p.split(',')[1]))
            except: pass
    return min(ys) if ys else 0

def run_novel_name_test(dataset, n_shots=1):
    results = []
    test_shapes = random.sample(dataset, 20)
    novel_names = ["Zark", "Gribble", "Bloop", "Xylo", "Quirk", "Vorm", "Jinx", "Plonk"] * 3
    
    for i, shape in enumerate(test_shapes):
        novel_name = novel_names[i]
        parts = list(shape['parts'].keys())
        if len(parts) < 2: continue
        
        p1, p2 = random.sample(parts, 2)
        relation = random.choice(["above", "below", "left", "right"])
        
        if relation == "above":
            gt = "Yes" if get_min_y(shape['parts'][p1]) < get_min_y(shape['parts'][p2]) else "No"
        elif relation == "below":
            gt = "Yes" if get_min_y(shape['parts'][p1]) > get_min_y(shape['parts'][p2]) else "No"
        # Skip left/right for brevity or keep them
        else: continue 
        
        shape_def = format_shape_novel(shape, novel_name)
        prompt = f"Here is a definition of a novel geometric object '{novel_name}':\n\n{shape_def}\n\nTask: In the object '{novel_name}', is the '{p1}' {relation} the '{p2}'? Answer only with 'Yes' or 'No'."
        
        response = get_completion(prompt)
        success = gt.lower() in response.lower() if response else False
        
        results.append({
            'shape_id': shape['id'],
            'novel_name': novel_name,
            'gt': gt,
            'response': response,
            'success': success
        })
    return results

if __name__ == "__main__":
    with open("results/processed_dataset.json", "r") as f:
        dataset = json.load(f)
    
    novel_results = run_novel_name_test(dataset)
    with open("results/novel_name_results.json", "w") as f:
        json.dump(novel_results, f, indent=2)
    
    acc = sum(1 for r in novel_results if r['success']) / len(novel_results) if novel_results else 0
    print(f"Novel Name Reasoning Accuracy: {acc}")

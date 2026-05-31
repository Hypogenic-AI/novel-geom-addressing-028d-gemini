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

def format_shape(shape):
    res = f"Object: {shape['whole_name']}\n"
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

def run_cot_test(dataset):
    results = []
    test_shapes = random.sample(dataset, 20)
    
    for shape in test_shapes:
        parts = list(shape['parts'].keys())
        if len(parts) < 2: continue
        
        p1, p2 = random.sample(parts, 2)
        relation = "above"
        gt = "Yes" if get_min_y(shape['parts'][p1]) < get_min_y(shape['parts'][p2]) else "No"
        
        shape_def = format_shape(shape)
        
        prompt = f"Here is a definition of a geometric object:\n\n{shape_def}\n\nTask: In this object, is the '{p1}' {relation} the '{p2}'? Think step by step. First, extract the y-coordinates for both parts. Then compare them. Finally, answer with 'Final Answer: Yes' or 'Final Answer: No'."
        
        response = get_completion(prompt)
        success = gt.lower() in response.lower() if response else False
        
        results.append({
            'shape_id': shape['id'],
            'gt': gt,
            'response': response,
            'success': success
        })
    return results

if __name__ == "__main__":
    with open("results/processed_dataset.json", "r") as f:
        dataset = json.load(f)
    
    cot_results = run_cot_test(dataset)
    with open("results/cot_results.json", "w") as f:
        json.dump(cot_results, f, indent=2)
    
    acc = sum(1 for r in cot_results if r['success']) / len(cot_results) if cot_results else 0
    print(f"CoT Reasoning Accuracy: {acc}")

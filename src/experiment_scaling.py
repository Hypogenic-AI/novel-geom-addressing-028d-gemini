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

def run_scaling_test(dataset, n_shots_list=[1, 5, 10, 20]):
    results = []
    # Use 10 shapes per N to keep it manageable
    test_shapes = random.sample(dataset, 10)
    
    for n in n_shots_list:
        print(f"Running Scaling Test with N={n}...")
        for shape in test_shapes:
            parts = list(shape['parts'].keys())
            if len(parts) < 2: continue
            
            p1, p2 = random.sample(parts, 2)
            relation = "above" # Keep it simple to see the trend
            gt = "Yes" if get_min_y(shape['parts'][p1]) < get_min_y(shape['parts'][p2]) else "No"
            
            shape_def = format_shape(shape)
            context = ""
            for i in range(n):
                context += f"Definition {i+1}:\n{shape_def}\n\n"
            
            prompt = f"Here are some definitions of geometric objects:\n\n{context}Task: In the object '{shape['whole_name']}', is the '{p1}' {relation} the '{p2}'? Answer only with 'Yes' or 'No'."
            
            response = get_completion(prompt)
            success = gt.lower() in response.lower() if response else False
            
            results.append({
                'n_shots': n,
                'shape_id': shape['id'],
                'gt': gt,
                'response': response,
                'success': success
            })
    return results

if __name__ == "__main__":
    with open("results/processed_dataset.json", "r") as f:
        dataset = json.load(f)
    
    n_shots_list = [1, 5, 10, 20]
    scaling_results = run_scaling_test(dataset, n_shots_list)
    with open("results/scaling_results.json", "w") as f:
        json.dump(scaling_results, f, indent=2)
    
    for n in n_shots_list:
        n_results = [r for r in scaling_results if r['n_shots'] == n]
        acc = sum(1 for r in n_results if r['success']) / len(n_results) if n_results else 0
        print(f"N={n} Accuracy: {acc}")

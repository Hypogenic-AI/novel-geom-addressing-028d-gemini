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
            try:
                ys.append(float(p.split(',')[1]))
            except: pass
    return min(ys) if ys else 0

def get_min_x(coords_list):
    xs = []
    for s in coords_list:
        points = s.split()
        for p in points:
            try:
                xs.append(float(p.split(',')[0]))
            except: pass
    return min(xs) if xs else 0

def run_reasoning_suite(dataset, n_shots_list=[1, 5]):
    results = []
    test_shapes = random.sample(dataset, 15)
    
    for n in n_shots_list:
        print(f"Running Reasoning Suite with N={n}...")
        for shape in test_shapes:
            parts = list(shape['parts'].keys())
            if len(parts) < 2: continue
            
            # Pick 2 random parts
            p1, p2 = random.sample(parts, 2)
            
            # Test 4 directions
            for relation in ["above", "below", "left", "right"]:
                if relation == "above":
                    gt = "Yes" if get_min_y(shape['parts'][p1]) < get_min_y(shape['parts'][p2]) else "No"
                elif relation == "below":
                    gt = "Yes" if get_min_y(shape['parts'][p1]) > get_min_y(shape['parts'][p2]) else "No"
                elif relation == "left":
                    gt = "Yes" if get_min_x(shape['parts'][p1]) < get_min_x(shape['parts'][p2]) else "No"
                elif relation == "right":
                    gt = "Yes" if get_min_x(shape['parts'][p1]) > get_min_x(shape['parts'][p2]) else "No"
                
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
                    'relation': relation,
                    'p1': p1,
                    'p2': p2,
                    'gt': gt,
                    'response': response,
                    'success': success
                })
    return results

if __name__ == "__main__":
    with open("results/processed_dataset.json", "r") as f:
        dataset = json.load(f)
    
    reasoning_results = run_reasoning_suite(dataset)
    with open("results/reasoning_suite_results.json", "w") as f:
        json.dump(reasoning_results, f, indent=2)
    
    print("Reasoning suite completed.")

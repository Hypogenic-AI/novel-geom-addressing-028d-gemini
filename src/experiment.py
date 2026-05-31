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

def run_experiment_1(dataset, n_shots_list=[0, 1, 3, 5]):
    results = []
    
    # Select a few shapes for testing
    test_shapes = random.sample(dataset, 5)
    
    for n in n_shots_list:
        print(f"Running Experiment 1 with N={n}...")
        for shape in test_shapes:
            shape_def = format_shape(shape)
            
            # Construct prompt
            if n == 0:
                prompt = f"Here is a definition of a geometric object:\n\n{shape_def}\n\nTask: Return the exact coordinates of the '{list(shape['parts'].keys())[0]}' in this object. Return only the coordinates, nothing else."
            else:
                context = ""
                for i in range(n):
                    context += f"Definition {i+1}:\n{shape_def}\n\n"
                prompt = f"Here are some definitions of geometric objects:\n\n{context}Task: Return the exact coordinates of the '{list(shape['parts'].keys())[0]}' in this object. Return only the coordinates, nothing else."
            
            start_time = time.time()
            response = get_completion(prompt)
            latency = time.time() - start_time
            
            # Evaluate
            target_part = list(shape['parts'].keys())[0]
            target_coords = " | ".join(shape['parts'][target_part])
            
            # Simplified evaluation: exact match or substring
            success = target_coords in response if response else False
            
            results.append({
                'n_shots': n,
                'shape_id': shape['id'],
                'target_part': target_part,
                'target_coords': target_coords,
                'response': response,
                'success': success,
                'latency': latency
            })
            
    return results

def run_experiment_2(dataset, n_shots_list=[1, 3, 5]):
    results = []
    
    # Select a few shapes for testing
    test_shapes = random.sample(dataset, 5)
    
    for n in n_shots_list:
        print(f"Running Experiment 2 with N={n}...")
        for shape in test_shapes:
            # We need at least 2 parts for reasoning
            parts = list(shape['parts'].keys())
            if len(parts) < 2:
                continue
            
            p1, p2 = parts[0], parts[1]
            
            # Ground truth for spatial reasoning (simplified: check y-coords)
            def get_min_y(coords_list):
                ys = []
                for s in coords_list:
                    points = s.split()
                    for p in points:
                        ys.append(float(p.split(',')[1]))
                return min(ys)
            
            min_y1 = get_min_y(shape['parts'][p1])
            min_y2 = get_min_y(shape['parts'][p2])
            
            gt_above = "Yes" if min_y1 < min_y2 else "No"
            
            shape_def = format_shape(shape)
            
            context = ""
            for i in range(n):
                context += f"Definition {i+1}:\n{shape_def}\n\n"
            
            prompt = f"Here are some definitions of geometric objects:\n\n{context}Task: In the object '{shape['whole_name']}', is the '{p1}' above the '{p2}'? Answer only with 'Yes' or 'No'."
            
            start_time = time.time()
            response = get_completion(prompt)
            latency = time.time() - start_time
            
            success = gt_above.lower() in response.lower() if response else False
            
            results.append({
                'n_shots': n,
                'shape_id': shape['id'],
                'p1': p1,
                'p2': p2,
                'gt_above': gt_above,
                'response': response,
                'success': success,
                'latency': latency
            })
            
    return results

if __name__ == "__main__":
    with open("results/processed_dataset.json", "r") as f:
        dataset = json.load(f)
    
    exp1_results = run_experiment_1(dataset)
    with open("results/exp1_results.json", "w") as f:
        json.dump(exp1_results, f, indent=2)
        
    exp2_results = run_experiment_2(dataset)
    with open("results/exp2_results.json", "w") as f:
        json.dump(exp2_results, f, indent=2)
    
    print("Experiments completed.")

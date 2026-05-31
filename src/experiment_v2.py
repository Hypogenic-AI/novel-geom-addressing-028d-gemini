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

def run_experiment_3(dataset, n_shots_list=[1, 2, 3, 5, 8]):
    """Tests memory/association: definition is in shots, but not in the final question block."""
    results = []
    
    # Select a few shapes for testing
    test_shapes = random.sample(dataset, 10)
    
    for n in n_shots_list:
        print(f"Running Experiment 3 (Memory) with N={n}...")
        for shape in test_shapes:
            shape_def = format_shape(shape)
            
            context = "Below are some definitions for you to remember.\n\n"
            for i in range(n):
                context += f"Definition {i+1}:\n{shape_def}\n\n"
            
            target_part = list(shape['parts'].keys())[0]
            target_coords = " | ".join(shape['parts'][target_part])
            
            prompt = context + f"Now, without looking back at the definitions if possible, what are the coordinates of the '{target_part}' in the object '{shape['whole_name']}'? Return only the coordinates, nothing else."
            
            start_time = time.time()
            response = get_completion(prompt)
            latency = time.time() - start_time
            
            results.append({
                'n_shots': n,
                'shape_id': shape['id'],
                'target_part': target_part,
                'target_coords': target_coords,
                'response': response,
                'latency': latency
            })
            
    return results

if __name__ == "__main__":
    with open("results/processed_dataset.json", "r") as f:
        dataset = json.load(f)
    
    exp3_results = run_experiment_3(dataset)
    with open("results/exp3_results.json", "w") as f:
        json.dump(exp3_results, f, indent=2)
    
    print("Experiment 3 completed.")

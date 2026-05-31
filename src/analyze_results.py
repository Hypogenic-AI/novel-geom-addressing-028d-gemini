import json
import pandas as pd
import matplotlib.pyplot as plt
import re

def clean_coords(s):
    # Extract all numbers/floats from a string
    return set(re.findall(r"[-+]?\d*\.\d+|\d+", s))

def analyze_results():
    with open("results/exp1_results.json", "r") as f:
        exp1 = json.load(f)
    with open("results/exp2_results.json", "r") as f:
        exp2 = json.load(f)
        
    # Robust success check for Exp 1
    for item in exp1:
        if not item['response']:
            item['success_robust'] = False
            continue
        expected_nums = clean_coords(item['target_coords'])
        got_nums = clean_coords(item['response'])
        # If all expected numbers are in got numbers, it's a success
        item['success_robust'] = expected_nums.issubset(got_nums)
    
    df1 = pd.DataFrame(exp1)
    df2 = pd.DataFrame(exp2)
    
    acc1 = df1.groupby('n_shots')['success_robust'].mean()
    acc2 = df2.groupby('n_shots')['success'].mean()
    
    print("Experiment 1 (Addressing) Robust Accuracy:")
    print(acc1)
    print("\nExperiment 2 (Reasoning) Accuracy:")
    print(acc2)
    
    # Plotting
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    acc1.plot(kind='bar', color='skyblue')
    plt.title('Exp 1: Addressing Accuracy (Robust)')
    plt.xlabel('N Shots')
    plt.ylabel('Accuracy')
    
    plt.subplot(1, 2, 2)
    acc2.plot(kind='bar', color='salmon')
    plt.title('Exp 2: Reasoning Accuracy')
    plt.xlabel('N Shots')
    plt.ylabel('Accuracy')
    plt.axhline(y=0.5, color='gray', linestyle='--')
    
    plt.tight_layout()
    plt.savefig('results/accuracy_plot_robust.png')
    
    # Save robust results
    df1.to_json("results/exp1_results_robust.json", orient='records', indent=2)

if __name__ == "__main__":
    analyze_results()

import json
import pandas as pd

def analyze_reasoning():
    with open("results/reasoning_suite_results.json", "r") as f:
        res = json.load(f)
    
    df = pd.DataFrame(res)
    acc = df.groupby(['n_shots', 'relation'])['success'].mean()
    print("Reasoning Accuracy by N-shot and Relation:")
    print(acc)
    
    acc_overall = df.groupby('n_shots')['success'].mean()
    print("\nOverall Reasoning Accuracy:")
    print(acc_overall)

if __name__ == "__main__":
    analyze_reasoning()

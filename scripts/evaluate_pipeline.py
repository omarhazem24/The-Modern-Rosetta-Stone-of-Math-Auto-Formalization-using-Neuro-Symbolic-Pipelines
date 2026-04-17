import os
import time
from llm_translator import multi_agent_consensus_and_repair
PROMPTS = [
    "The intersection of sets A and B contains elements that are in both A and B.",
    "A function f from A to B is injective if and only if for all x and y in A, if f(x) equals f(y), then x equals y.",
    "The symmetric difference of two sets A and B is the set containing those elements in either A or B, but not in both.",
    "An integer n is even if there exists an integer k such that n is equal to 2 times k.",
    "A relation R on a set A is an equivalence relation if it is reflexive, symmetric, and transitive.",
    "The power set of a set S is the set of all subsets of S, including the empty set and S itself.",
    "An integer p greater than 1 is prime if the only positive factors of p are 1 and p.",
    "The union of a collection of sets is the set that contains those elements that are members of at least one set in the collection.",
    "For any two real numbers x and y, the absolute value of their sum is less than or equal to the sum of their absolute values.",
    "If n is a positive integer, then n factorial is the product of the first n positive integers."
]

def run_evaluation():
    print("==================================================")
    print("Starting Pipeline Evaluation on 10 Rosen Prompts")
    print("==================================================")
    
    results = []
    total_prompts = len(PROMPTS)
    
    for idx, prompt_text in enumerate(PROMPTS, 1):
        print(f"\n[{idx}/{total_prompts}] Testing Prompt: '{prompt_text}'")
        output_file = f"Output_{idx}.lean"
        
        try:
            start_time = time.time()
            success, iterations = multi_agent_consensus_and_repair(prompt_text, output_file, max_retries=10)
            elapsed_time = time.time() - start_time
            
            results.append({
                "prompt": prompt_text,
                "success": success,
                "iterations": iterations,
                "time": elapsed_time
            })
            
            status = "PASSED" if success else "FAILED"
            print(f">>> Result: {status} in {iterations} iterations ({elapsed_time:.1f}s)")
            
        except Exception as e:
            print(f">>> Error evaluating prompt {idx}: {e}")
            results.append({
                "prompt": prompt_text,
                "success": False,
                "iterations": 0,
                "time": 0.0
            })
    print("\n" + "="*50)
    print("FINAL EVALUATION REPORT")
    print("="*50)
    
    successful_runs = [r for r in results if r["success"]]
    failed_runs = [r for r in results if not r["success"]]
    
    success_rate = (len(successful_runs) / total_prompts) * 100
    avg_iterations_success = sum(r["iterations"] for r in successful_runs) / len(successful_runs) if successful_runs else 0
    avg_time = sum(r["time"] for r in results) / len(results) if results else 0
    
    print(f"Total Prompts Tested: {total_prompts}")
    print(f"Overall Success Rate: {success_rate:.1f}%")
    print(f"Average Execution Time per Prompt: {avg_time:.1f}s")
    
    print("\n
    print(f"Average Fix Iterations (successful runs): {avg_iterations_success:.1f}")
    if avg_iterations_success == 1:
        print("Effectiveness: Excellent. Most prompts were translated correctly on the first try or required no cyclic repairs.")
    elif 1 < avg_iterations_success <= 5:
        print("Effectiveness: High. The Critic successfully diagnosed and repaired errors efficiently within the first half of the retry budget.")
    elif 5 < avg_iterations_success <= 9:
        print("Effectiveness: Moderate. The Loop repaired complex errors, but struggled with repetitive hallucination before converging.")
    else:
        print("Effectiveness: Poor. The Actor-Critic loop consistently hit maximum iterations without finding a formally verified translation.")

    print("\n
    for idx, r in enumerate(results, 1):
        mark = "✓" if r["success"] else "✗"
        print(f"[{mark}] Prompt {idx}: {r['iterations']} iterations | {r['time']:.1f}s")
        print(f"     \"{r['prompt'][:60]}...\"")

if __name__ == "__main__":
    run_evaluation()

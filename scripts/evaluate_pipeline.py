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
    "If n is a positive integer, then n factorial is the product of the first n positive integers.",
    "The intersection of two disjoint non-empty sets contains exactly one element.",
    "A bipartite graph is a graph whose vertices can be divided into two disjoint sets such that every edge connects a vertex in one to a vertex in the other.",
    "The sum of any two odd integers is an odd integer.",
    "A rational number is any number that can be expressed as the quotient or fraction p/q of two integers.",
    "The square of any real number is non-negative.",
    "A set A is a subset of a set B if every element of A is also an element of B.",
    "The number of vertices of odd degree in any finite graph is even.",
    "For any set A, the intersection of A with the empty set is the empty set.",
    "For any set A, the union of A with the empty set is A.",
    "A relation is symmetric if for all x, y, x related to y implies y related to x.",
    "A relation is transitive if for all x, y, z, x related to y and y related to z implies x related to z.",
    "Two sets are equal if and only if they have the exact same elements.",
    "The absolute value of x is x if x is non-negative, and -x if x is negative.",
    "The greatest common divisor of a and b divides both a and b.",
    "If a divides b and b divides c, then a divides c.",
    "If a is a divisor of b and b is a divisor of a, then a equals b or a equals -b.",
    "The sum of an even integer and an odd integer is an odd integer.",
    "The product of an even integer and any integer is an even integer.",
    "A finite set with n elements has 2^n subsets.",
    "The cartesian product of two sets A and B is the set of all ordered pairs (a,b) where a is in A and b is in B.",
    "If a function is strictly increasing, then it is injective.",
    "The composition of two injective functions is injective.",
    "The composition of two surjective functions is surjective.",
    "A bijective function has an inverse.",
    "The inverse of a bijective function is also bijective.",
    "A tree is a connected acyclic undirected graph.",
    "A natural number is divisible by 3 if the sum of its digits is divisible by 3.",
    "If a divides bc and a is coprime to b, then a divides c.",
    "Every natural number greater than 1 can be uniquely factored into prime numbers.",
    "The set of rational numbers is dense in the real numbers.",
    "There is no largest prime number.",
    "The square root of 2 is irrational.",
    "Between any two distinct real numbers there is a rational number.",
    "The limit of 1/n as n approaches infinity is 0.",
    "A continuous function on a closed interval achieves its maximum and minimum bounds.",
    "Every differentiable function is continuous.",
    "A polynomial of degree n over the complex numbers has exactly n roots counting multiplicities.",
    "The derivative of a constant function is zero.",
    "A cycle in a graph is a path that starts and ends at the same vertex.",
    "The sum of the first n odd non-negative integers is n squared."
]

def run_evaluation():
    print("==================================================")
    print("Starting Pipeline Evaluation on " + str(len(PROMPTS)) + " Prompts")
    print("==================================================")
    
    results = []
    total_prompts = len(PROMPTS)
    
    for idx, prompt_text in enumerate(PROMPTS, 1):
        print("\n[" + str(idx) + "/" + str(total_prompts) + "] Testing Prompt: '" + prompt_text + "'")
        output_file = "Output_" + str(idx) + ".lean"
        
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
            print(">>> Result: " + status + " in " + str(iterations) + " iterations (" + str(round(elapsed_time, 1)) + "s)")
            
        except Exception as e:
            print(">>> Error evaluating prompt " + str(idx) + ": " + str(e))
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
    
    print("Total Prompts Tested: " + str(total_prompts))
    print("Overall Success Rate: " + str(round(success_rate, 1)) + "%")
    print("Average Execution Time per Prompt: " + str(round(avg_time, 1)) + "s")
    
    print("\n--- Repair Loop Effectiveness ---")
    print("Average Fix Iterations (successful runs): " + str(round(avg_iterations_success, 1)))
    if avg_iterations_success == 1:
        print("Effectiveness: Excellent. Most prompts were translated correctly on the first try or required no cyclic repairs.")
    elif 1 < avg_iterations_success <= 5:
        print("Effectiveness: High. The Critic successfully diagnosed and repaired errors efficiently within the first half of the retry budget.")
    elif 5 < avg_iterations_success <= 9:
        print("Effectiveness: Moderate. The Loop repaired complex errors, but struggled with repetitive hallucination before converging.")
    else:
        print("Effectiveness: Poor. The Actor-Critic loop consistently hit maximum iterations without finding a formally verified translation.")

    print("\n--- Benchmark Detail ---")
    for idx, r in enumerate(results, 1):
        mark = "[OK]" if r["success"] else "[X]"
        print(mark + " Prompt " + str(idx) + ": " + str(r['iterations']) + " iterations | " + str(round(r['time'], 1)) + "s")
        print("     '" + r['prompt'][:60] + "...'")

if __name__ == "__main__":
    run_evaluation()

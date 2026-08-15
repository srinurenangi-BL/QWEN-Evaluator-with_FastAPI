"""
test_data.py — 18 Controlled Variants for "Second Largest Distinct Element"
Each variant has a ground truth label, expected score ranges, and the exact code.
"""

QUESTION_TEXT = (
    "Write a Java program that reads an array of integers and prints the second "
    "largest distinct value in the array (i.e. duplicates of the largest value don't "
    "count as a separate \"second largest\")."
)

# ---------------------------------------------------------------------------
# Each test case dict:
#   id              — short label (V1 … V18)
#   category        — human-readable category
#   ground_truth    — what the answer actually is
#   code            — the student submission
#   target_language — expected language (always Java except V15)
#   expected_overall_min / max — the score range we consider a PASS
#   key_checks      — list of strings we expect to find (or NOT find) in feedback
#   notes           — why we expect what we expect
# ---------------------------------------------------------------------------

TEST_CASES = [
    # ===================================================================
    # V1 — Fully Correct
    # ===================================================================
    {
        "id": "V1",
        "category": "Fully Correct",
        "ground_truth": "Fully Correct. No issues.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = Integer.MIN_VALUE;
        int secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            if (arr[i] > largest) {
                secondLargest = largest;
                largest = arr[i];
            } else if (arr[i] > secondLargest && arr[i] != largest) {
                secondLargest = arr[i];
            }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 8.0,
        "expected_overall_max": 10.0,
        "notes": "Reference solution — should score near-perfect.",
    },

    # ===================================================================
    # V2 — Missing public class wrapper
    # ===================================================================
    {
        "id": "V2",
        "category": "Does Not Compile",
        "ground_truth": "Does Not Compile — no class declaration, main is floating. Also missing import.",
        "code": """public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int n = sc.nextInt();
    int[] arr = new int[n];
    for (int i = 0; i < n; i++) arr[i] = sc.nextInt();
    int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
        else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
    }
    System.out.println(secondLargest);
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "No class, no import. Should be flagged as non-compilable.",
    },

    # ===================================================================
    # V3 — Class present, main method missing entirely
    # ===================================================================
    {
        "id": "V3",
        "category": "Compiles But Unrunnable",
        "ground_truth": "Compiles but no main method — cannot execute. Logic inside helper is correct.",
        "code": """import java.util.Scanner;

public class Main {
    public static int findSecondLargest(int[] arr) {
        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        return secondLargest;
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 5.0,
        "notes": "No main method. Logic is correct but unreachable/untestable.",
    },

    # ===================================================================
    # V4 — Method defined but never called (dead code)
    # ===================================================================
    {
        "id": "V4",
        "category": "Runs But No Output",
        "ground_truth": "Compiles and runs, but produces no output. Correct helper is dead code — never invoked.",
        "code": """import java.util.Scanner;

public class Main {
    public static int findSecondLargest(int[] arr) {
        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        return secondLargest;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();
        // forgot to call findSecondLargest(arr) and print the result
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 4.0,
        "notes": "Dead code trap — grader must notice method is never called, not just that it exists.",
    },

    # ===================================================================
    # V5 — Off-by-one loop bound (skips last element)
    # ===================================================================
    {
        "id": "V5",
        "category": "Partially Correct (Logic Bug)",
        "ground_truth": "i < n - 1 skips last element. Wrong output on most inputs.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < n - 1; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 6.0,
        "notes": "Known blind spot territory — 'right shape' bug. Watch if model catches i < n-1.",
    },

    # ===================================================================
    # V6 — Duplicates not handled (missing != largest guard)
    # ===================================================================
    {
        "id": "V6",
        "category": "Partially Correct (Logic Bug)",
        "ground_truth": "Missing arr[i] != largest guard. Fails on arrays with duplicate max values.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 6.5,
        "notes": "Known blind spot territory — missing duplicate guard is a 'shape-correct' bug.",
    },

    # ===================================================================
    # V7 — Crashes on single-element array
    # ===================================================================
    {
        "id": "V7",
        "category": "Partially Correct (Edge Case Crash)",
        "ground_truth": "ArrayIndexOutOfBoundsException when n <= 1. No bounds guard.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = arr[0], secondLargest = arr[1];
        for (int i = 2; i < n; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 6.5,
        "notes": "Known blind spot territory — crashes only on edge-case input (n<=1).",
    },

    # ===================================================================
    # V8 — Solves a different problem (prints largest, not second-largest)
    # ===================================================================
    {
        "id": "V8",
        "category": "Mismatched (Wrong Problem)",
        "ground_truth": "Prints the largest element, not the second-largest. Different question answered.",
        "code": """import java.util.Scanner;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();
        Arrays.sort(arr);
        System.out.println(arr[n - 1]);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 3.0,
        "notes": "Model should detect it answers a different question. Known strength area.",
    },

    # ===================================================================
    # V9 — Syntax error (missing closing brace)
    # ===================================================================
    {
        "id": "V9",
        "category": "Does Not Compile (Syntax Error)",
        "ground_truth": "Missing final closing brace for Main class.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Missing closing brace — straightforward syntax error.",
    },

    # ===================================================================
    # V10 — Syntax error (missing semicolon)
    # ===================================================================
    {
        "id": "V10",
        "category": "Does Not Compile (Syntax Error)",
        "ground_truth": "Missing semicolon after sc.nextInt() on the n assignment line.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt()
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Missing semicolon — straightforward syntax error.",
    },

    # ===================================================================
    # V11 — Wrong return type causes compile error
    # ===================================================================
    {
        "id": "V11",
        "category": "Does Not Compile (Type Error)",
        "ground_truth": "void method has return secondLargest — cannot return a value from void.",
        "code": """import java.util.Scanner;

public class Main {
    public static void findSecondLargest(int[] arr) {
        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        return secondLargest;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();
        System.out.println(findSecondLargest(arr));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "void + return value — should be caught as compile error.",
    },

    # ===================================================================
    # V12 — Infinite loop (missing increment)
    # ===================================================================
    {
        "id": "V12",
        "category": "Runs But Hangs",
        "ground_truth": "i is never incremented inside while loop — infinite loop. Logic body is correct.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        int i = 0;
        while (i < n) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Blind spot territory — 'correct shape' but hangs forever. Body logic is fine.",
    },

    # ===================================================================
    # V13 — Undeclared/misspelled variable (compile error)
    # ===================================================================
    {
        "id": "V13",
        "category": "Does Not Compile (Typo)",
        "ground_truth": "secondlargest (lowercase l) != secondLargest (uppercase L). Case-sensitive error.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondlargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Case-sensitive typo — easy for humans to miss, fatal for compiler.",
    },

    # ===================================================================
    # V14 — Correct logic, poor readability/style
    # ===================================================================
    {
        "id": "V14",
        "category": "Fully Correct (Poor Style)",
        "ground_truth": "Functionally correct — identical logic, crushed formatting. Style ding only.",
        "code": """import java.util.*;
public class Main{public static void main(String[]a){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]r=new int[n];for(int i=0;i<n;i++)r[i]=s.nextInt();int l=Integer.MIN_VALUE,sl=Integer.MIN_VALUE;for(int i=0;i<n;i++){if(r[i]>l){sl=l;l=r[i];}else if(r[i]>sl&&r[i]!=l){sl=r[i];}}System.out.println(sl);}}""",
        "target_language": "Java",
        "expected_overall_min": 5.0,
        "expected_overall_max": 9.0,
        "notes": "Completeness should be high, code_quality should be low. Tests style vs correctness separation.",
    },

    # ===================================================================
    # V15 — Wrong language (Python)
    # ===================================================================
    {
        "id": "V15",
        "category": "Wrong Language",
        "ground_truth": "Python code. Logic is correct but language gate should reject before grading.",
        "code": """n = int(input())
arr = list(map(int, input().split()))
unique_sorted = sorted(set(arr), reverse=True)
print(unique_sorted[1] if len(unique_sorted) > 1 else None)""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 0.0,
        "notes": "Language mismatch — known strength. All scores should be 0.0.",
    },

    # ===================================================================
    # V16 — Empty/unattempted stub
    # ===================================================================
    {
        "id": "V16",
        "category": "Unattempted",
        "ground_truth": "Compiles, runs, no output, no logic. Completely unattempted.",
        "code": """public class Main {
    public static void main(String[] args) {
        // TODO: figure this out later
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 2.0,
        "notes": "Empty stub — should get near-zero across all scores.",
    },

    # ===================================================================
    # V17 — Right idea, wrong initial values (fails on negative arrays)
    # ===================================================================
    {
        "id": "V17",
        "category": "Partially Correct (Subtle Init Bug)",
        "ground_truth": "Initialized to 0 instead of Integer.MIN_VALUE. Fails on all-negative arrays.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        int largest = 0, secondLargest = 0;
        for (int i = 0; i < n; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 7.0,
        "notes": "KNOWN BLIND SPOT — model missed Kadane's 0-init bug before. Key test case.",
    },

    # ===================================================================
    # V18 — Correct logic, extra unused import and dead variable
    # ===================================================================
    {
        "id": "V18",
        "category": "Fully Correct (Minor Dead Code)",
        "ground_truth": "Functionally correct. Unused import and dead variable — minor code quality issue.",
        "code": """import java.util.Scanner;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        int unusedCounter = 0;
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
            unusedCounter++;
        }

        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for (int i = 0; i < n; i++) {
            if (arr[i] > largest) { secondLargest = largest; largest = arr[i]; }
            else if (arr[i] > secondLargest && arr[i] != largest) { secondLargest = arr[i]; }
        }
        System.out.println(secondLargest);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 7.0,
        "expected_overall_max": 10.0,
        "notes": "Correct with minor dead code. Completeness high, code_quality slightly dinged.",
    },
]

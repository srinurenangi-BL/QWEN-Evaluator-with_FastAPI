"""
test_data.py — Unified Master Test Suite for QWEN Code Evaluator (48 Test Cases)

Consolidated test cases spanning:
- V1 – V18: 18 Variants of "Second Largest Distinct Element" (Structural & Boundary Checks)
- V19 – V38: 20 Variants across 5 Problem Domains (Reverse String, Prime, Vowel Count, GCD, Array Sorted)
- V39 – V48: 10 Classic DS&A Algorithm Problems (Two Sum, LinkedList, Stacks, Kadane's, Intervals, DP, Window, Trees, Cycle, Anagrams)
"""

TEST_CASES = [
    # ===================================================================
    # PROBLEM 1: Second Largest Distinct Element (V1 – V18)
    # ===================================================================
    {
        "id": "V1",
        "category": "Fully Correct",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
    {
        "id": "V2",
        "category": "Does Not Compile (Missing Class)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
    {
        "id": "V3",
        "category": "Compiles But Unrunnable",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
    {
        "id": "V4",
        "category": "Runs But No Output",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Dead code trap — grader must notice method is never called.",
    },
    {
        "id": "V5",
        "category": "Partially Correct (Logic Bug)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Off-by-one loop bound (skips last element).",
    },
    {
        "id": "V6",
        "category": "Partially Correct (Logic Bug)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Missing duplicate guard is a shape-correct bug.",
    },
    {
        "id": "V7",
        "category": "Partially Correct (Edge Case Crash)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Crashes on edge-case input (n<=1).",
    },
    {
        "id": "V8",
        "category": "Mismatched (Wrong Problem)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Prints largest instead of second largest.",
    },
    {
        "id": "V9",
        "category": "Does Not Compile (Syntax Error)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
    {
        "id": "V10",
        "category": "Does Not Compile (Syntax Error)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
    {
        "id": "V11",
        "category": "Does Not Compile (Type Error)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "void + return value — compile error.",
    },
    {
        "id": "V12",
        "category": "Runs But Hangs",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Infinite loop — missing i++.",
    },
    {
        "id": "V13",
        "category": "Does Not Compile (Typo)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Case-sensitive typo in variable name.",
    },
    {
        "id": "V14",
        "category": "Fully Correct (Poor Style)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
        "ground_truth": "Functionally correct — identical logic, crushed formatting. Style ding only.",
        "code": """import java.util.*;
public class Main{public static void main(String[]a){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]r=new int[n];for(int i=0;i<n;i++)r[i]=s.nextInt();int l=Integer.MIN_VALUE,sl=Integer.MIN_VALUE;for(int i=0;i<n;i++){if(r[i]>l){sl=l;l=r[i];}else if(r[i]>sl&&r[i]!=l){sl=r[i];}}System.out.println(sl);}}""",
        "target_language": "Java",
        "expected_overall_min": 5.0,
        "expected_overall_max": 9.0,
        "notes": "Minified single-line code. Correct logic with poor readability.",
    },
    {
        "id": "V15",
        "category": "Wrong Language",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
        "ground_truth": "Python code. Logic is correct but language gate should reject before grading.",
        "code": """n = int(input())
arr = list(map(int, input().split()))
unique_sorted = sorted(set(arr), reverse=True)
print(unique_sorted[1] if len(unique_sorted) > 1 else None)""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 0.0,
        "notes": "Language mismatch — should score 0.0 across the board.",
    },
    {
        "id": "V16",
        "category": "Unattempted",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
        "ground_truth": "Compiles, runs, no output, no logic. Completely unattempted.",
        "code": """public class Main {
    public static void main(String[] args) {
        // TODO: figure this out later
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 2.0,
        "notes": "Empty stub — should get near-zero.",
    },
    {
        "id": "V17",
        "category": "Partially Correct (Subtle Init Bug)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Bad init value (0 instead of Integer.MIN_VALUE).",
    },
    {
        "id": "V18",
        "category": "Fully Correct (Minor Dead Code)",
        "question_text": "Write a Java program that reads an array of integers and prints the second largest distinct value in the array (i.e. duplicates of the largest value don't count as a separate \"second largest\").",
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
        "notes": "Correct with minor dead code.",
    },

    # ===================================================================
    # PROBLEM 2: Reverse a String (V19 – V22)
    # ===================================================================
    {
        "id": "V19",
        "category": "Fully Correct",
        "question_text": "Write a Java program that reads a string from the user and prints it reversed, without using StringBuilder.reverse() or any built-in reverse method. Use a character-level approach (e.g., loop from end to start, or swap in a char array).",
        "ground_truth": "Correct. Loops from end to start building reversed string.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.nextLine();
        char[] chars = input.toCharArray();
        int left = 0, right = chars.length - 1;
        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }
        System.out.println(new String(chars));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 8.0,
        "expected_overall_max": 10.0,
        "notes": "Clean char-array swap approach.",
    },
    {
        "id": "V20",
        "category": "Does Not Compile (Syntax Error)",
        "question_text": "Write a Java program that reads a string from the user and prints it reversed, without using StringBuilder.reverse() or any built-in reverse method. Use a character-level approach (e.g., loop from end to start, or swap in a char array).",
        "ground_truth": "Won't compile — missing semicolons after sc.nextLine() and after temp declaration.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.nextLine()
        char[] chars = input.toCharArray();
        int left = 0, right = chars.length - 1;
        while (left < right) {
            char temp = chars[left]
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }
        System.out.println(new String(chars));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Missing semicolons.",
    },
    {
        "id": "V21",
        "category": "Partially Correct (Runtime Crash)",
        "question_text": "Write a Java program that reads a string from the user and prints it reversed, without using StringBuilder.reverse() or any built-in reverse method. Use a character-level approach (e.g., loop from end to start, or swap in a char array).",
        "ground_truth": "Crashes with ArrayIndexOutOfBoundsException — right starts at chars.length instead of chars.length - 1.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.nextLine();
        char[] chars = input.toCharArray();
        int left = 0, right = chars.length;
        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }
        System.out.println(new String(chars));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 2.0,
        "expected_overall_max": 6.0,
        "notes": "Off-by-one causing ArrayIndexOutOfBounds.",
    },
    {
        "id": "V22",
        "category": "Runs But Hangs",
        "question_text": "Write a Java program that reads a string from the user and prints it reversed, without using StringBuilder.reverse() or any built-in reverse method. Use a character-level approach (e.g., loop from end to start, or swap in a char array).",
        "ground_truth": "Infinite loop — left++ and right-- are commented out. While body swaps forever.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.nextLine();
        char[] chars = input.toCharArray();
        int left = 0, right = chars.length - 1;
        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            // left++;
            // right--;
        }
        System.out.println(new String(chars));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Infinite loop in string reversal.",
    },

    # ===================================================================
    # PROBLEM 3: Prime Number Check (V23 – V26)
    # ===================================================================
    {
        "id": "V23",
        "category": "Fully Correct",
        "question_text": "Write a Java program that reads an integer from the user and prints whether it is a prime number or not. Handle edge cases: numbers less than 2 are not prime. Use an efficient approach (check divisibility up to sqrt(n)).",
        "ground_truth": "Correct. Handles edge cases, uses sqrt optimization.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        if (n < 2) {
            System.out.println("Not Prime");
            return;
        }

        boolean isPrime = true;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) {
                isPrime = false;
                break;
            }
        }
        System.out.println(isPrime ? "Prime" : "Not Prime");
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 8.0,
        "expected_overall_max": 10.0,
        "notes": "Clean prime check.",
    },
    {
        "id": "V24",
        "category": "Partially Correct (Edge Case Bug)",
        "question_text": "Write a Java program that reads an integer from the user and prints whether it is a prime number or not. Handle edge cases: numbers less than 2 are not prime. Use an efficient approach (check divisibility up to sqrt(n)).",
        "ground_truth": "Bug: considers 1 as prime (guard is n < 1 instead of n < 2). Also considers 0 and negative numbers incorrectly.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        if (n < 1) {
            System.out.println("Not Prime");
            return;
        }

        boolean isPrime = true;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) {
                isPrime = false;
                break;
            }
        }
        System.out.println(isPrime ? "Prime" : "Not Prime");
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 4.0,
        "expected_overall_max": 7.0,
        "notes": "Subtle edge case: n < 1 instead of n < 2.",
    },
    {
        "id": "V25",
        "category": "Does Not Compile (Type Error)",
        "question_text": "Write a Java program that reads an integer from the user and prints whether it is a prime number or not. Handle edge cases: numbers less than 2 are not prime. Use an efficient approach (check divisibility up to sqrt(n)).",
        "ground_truth": "Won't compile — isPrime() declared void but returns boolean.",
        "code": """import java.util.Scanner;

public class Main {
    public static void isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(isPrime(n) ? "Prime" : "Not Prime");
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "void method returning boolean.",
    },
    {
        "id": "V26",
        "category": "Fully Correct (Poor Style)",
        "question_text": "Write a Java program that reads an integer from the user and prints whether it is a prime number or not. Handle edge cases: numbers less than 2 are not prime. Use an efficient approach (check divisibility up to sqrt(n)).",
        "ground_truth": "Functionally correct. Crushed formatting, single-letter vars, no whitespace.",
        "code": """import java.util.*;public class Main{public static void main(String[]a){int n=new Scanner(System.in).nextInt();if(n<2){System.out.println("Not Prime");return;}boolean p=true;for(int i=2;i<=Math.sqrt(n);i++){if(n%i==0){p=false;break;}}System.out.println(p?"Prime":"Not Prime");}}""",
        "target_language": "Java",
        "expected_overall_min": 5.0,
        "expected_overall_max": 9.0,
        "notes": "Minified prime check.",
    },

    # ===================================================================
    # PROBLEM 4: Count Vowels and Consonants (V27 – V30)
    # ===================================================================
    {
        "id": "V27",
        "category": "Fully Correct",
        "question_text": "Write a Java program that reads a string and counts the number of vowels and consonants in it. Ignore spaces, digits, and special characters — only count alphabetic characters. Print the counts in the format: 'Vowels: X, Consonants: Y'.",
        "ground_truth": "Correct. Properly filters non-alpha chars and counts vowels/consonants.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.nextLine().toLowerCase();
        int vowels = 0, consonants = 0;

        for (int i = 0; i < input.length(); i++) {
            char ch = input.charAt(i);
            if (Character.isLetter(ch)) {
                if ("aeiou".indexOf(ch) != -1) {
                    vowels++;
                } else {
                    consonants++;
                }
            }
        }
        System.out.println("Vowels: " + vowels + ", Consonants: " + consonants);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 8.0,
        "expected_overall_max": 10.0,
        "notes": "Clean vowel/consonant counter.",
    },
    {
        "id": "V28",
        "category": "Partially Correct (Logic Bug)",
        "question_text": "Write a Java program that reads a string and counts the number of vowels and consonants in it. Ignore spaces, digits, and special characters — only count alphabetic characters. Print the counts in the format: 'Vowels: X, Consonants: Y'.",
        "ground_truth": "Bug: no isLetter check, so spaces/digits/special chars count as consonants.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.nextLine().toLowerCase();
        int vowels = 0, consonants = 0;

        for (int i = 0; i < input.length(); i++) {
            char ch = input.charAt(i);
            if ("aeiou".indexOf(ch) != -1) {
                vowels++;
            } else {
                consonants++;
            }
        }
        System.out.println("Vowels: " + vowels + ", Consonants: " + consonants);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 6.5,
        "notes": "Missing isLetter guard — spaces count as consonants.",
    },
    {
        "id": "V29",
        "category": "Does Not Compile (Syntax Error)",
        "question_text": "Write a Java program that reads a string and counts the number of vowels and consonants in it. Ignore spaces, digits, and special characters — only count alphabetic characters. Print the counts in the format: 'Vowels: X, Consonants: Y'.",
        "ground_truth": "Won't compile — missing final closing brace for Main class.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String input = sc.nextLine().toLowerCase();
        int vowels = 0, consonants = 0;

        for (int i = 0; i < input.length(); i++) {
            char ch = input.charAt(i);
            if (Character.isLetter(ch)) {
                if ("aeiou".indexOf(ch) != -1) {
                    vowels++;
                } else {
                    consonants++;
                }
            }
        }
        System.out.println("Vowels: " + vowels + ", Consonants: " + consonants);
    }""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Missing closing brace.",
    },
    {
        "id": "V30",
        "category": "Wrong Language",
        "question_text": "Write a Java program that reads a string and counts the number of vowels and consonants in it. Ignore spaces, digits, and special characters — only count alphabetic characters. Print the counts in the format: 'Vowels: X, Consonants: Y'.",
        "ground_truth": "Python code. Logic is correct but wrong language.",
        "code": """s = input().lower()
vowels = sum(1 for c in s if c in 'aeiou')
consonants = sum(1 for c in s if c.isalpha() and c not in 'aeiou')
print(f"Vowels: {vowels}, Consonants: {consonants}")""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 0.0,
        "notes": "Python code submitted as Java.",
    },

    # ===================================================================
    # PROBLEM 5: GCD using Euclidean Algorithm (V31 – V34)
    # ===================================================================
    {
        "id": "V31",
        "category": "Fully Correct",
        "question_text": "Write a Java program that reads two positive integers and prints their Greatest Common Divisor (GCD) using the Euclidean algorithm. The Euclidean algorithm repeatedly replaces the larger number with the remainder of dividing the larger by the smaller until one becomes zero.",
        "ground_truth": "Correct Euclidean algorithm implementation.",
        "code": """import java.util.Scanner;

public class Main {
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        System.out.println("GCD: " + gcd(a, b));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 8.0,
        "expected_overall_max": 10.0,
        "notes": "Clean Euclidean algorithm.",
    },
    {
        "id": "V32",
        "category": "Runs But No Output",
        "question_text": "Write a Java program that reads two positive integers and prints their Greatest Common Divisor (GCD) using the Euclidean algorithm. The Euclidean algorithm repeatedly replaces the larger number with the remainder of dividing the larger by the smaller until one becomes zero.",
        "ground_truth": "Compiles and runs, but gcd() is never called. Main just reads input and exits.",
        "code": """import java.util.Scanner;

public class Main {
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        // should call gcd(a, b) and print result
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 4.0,
        "notes": "gcd() never called from main.",
    },
    {
        "id": "V33",
        "category": "Mismatched (Wrong Problem)",
        "question_text": "Write a Java program that reads two positive integers and prints their Greatest Common Divisor (GCD) using the Euclidean algorithm. The Euclidean algorithm repeatedly replaces the larger number with the remainder of dividing the larger by the smaller until one becomes zero.",
        "ground_truth": "Calculates and prints LCM, not GCD. Different computation entirely.",
        "code": """import java.util.Scanner;

public class Main {
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        int lcm = (a * b) / gcd(a, b);
        System.out.println("GCD: " + lcm);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 4.0,
        "notes": "Prints LCM labeled as GCD.",
    },
    {
        "id": "V34",
        "category": "Runs But Crashes (Stack Overflow)",
        "question_text": "Write a Java program that reads two positive integers and prints their Greatest Common Divisor (GCD) using the Euclidean algorithm. The Euclidean algorithm repeatedly replaces the larger number with the remainder of dividing the larger by the smaller until one becomes zero.",
        "ground_truth": "Infinite recursion — recursive call uses gcd(a, b) instead of gcd(b, a % b). StackOverflowError.",
        "code": """import java.util.Scanner;

public class Main {
    public static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(a, b);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        System.out.println("GCD: " + gcd(a, b));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Infinite recursion in gcd.",
    },

    # ===================================================================
    # PROBLEM 6: Check If Array Is Sorted (V35 – V38)
    # ===================================================================
    {
        "id": "V35",
        "category": "Fully Correct",
        "question_text": "Write a Java program that reads an array of integers and checks whether the array is sorted in strictly ascending order (each element must be strictly greater than the previous one). Print 'Sorted' or 'Not Sorted'.",
        "ground_truth": "Correct. Uses strict < comparison between consecutive elements.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        boolean sorted = true;
        for (int i = 1; i < n; i++) {
            if (arr[i] <= arr[i - 1]) {
                sorted = false;
                break;
            }
        }
        System.out.println(sorted ? "Sorted" : "Not Sorted");
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 8.0,
        "expected_overall_max": 10.0,
        "notes": "Clean ascending-order check.",
    },
    {
        "id": "V36",
        "category": "Partially Correct (Wrong Condition)",
        "question_text": "Write a Java program that reads an array of integers and checks whether the array is sorted in strictly ascending order (each element must be strictly greater than the previous one). Print 'Sorted' or 'Not Sorted'.",
        "ground_truth": "Bug: checks arr[i] >= arr[i-1] which checks for NON-DESCENDING (wrong direction). On descending arrays it says 'Sorted', on ascending it says 'Not Sorted'.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        boolean sorted = true;
        for (int i = 1; i < n; i++) {
            if (arr[i] >= arr[i - 1]) {
                sorted = false;
                break;
            }
        }
        System.out.println(sorted ? "Sorted" : "Not Sorted");
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 4.0,
        "notes": "Inverted condition checks descending order.",
    },
    {
        "id": "V37",
        "category": "Does Not Compile (Typo)",
        "question_text": "Write a Java program that reads an array of integers and checks whether the array is sorted in strictly ascending order (each element must be strictly greater than the previous one). Print 'Sorted' or 'Not Sorted'.",
        "ground_truth": "Won't compile — 'sorte' is used in println but only 'sorted' is declared.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        boolean sorted = true;
        for (int i = 1; i < n; i++) {
            if (arr[i] <= arr[i - 1]) {
                sorted = false;
                break;
            }
        }
        System.out.println(sorte ? "Sorted" : "Not Sorted");
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 4.0,
        "notes": "Typo 'sorte' instead of 'sorted'.",
    },
    {
        "id": "V38",
        "category": "Unattempted",
        "question_text": "Write a Java program that reads an array of integers and checks whether the array is sorted in strictly ascending order (each element must be strictly greater than the previous one). Print 'Sorted' or 'Not Sorted'.",
        "ground_truth": "Compiles, runs, no output, no logic. Completely unattempted.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        // I'll do this tomorrow
        Scanner sc = new Scanner(System.in);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 2.0,
        "notes": "Empty stub with scanner only.",
    },

    # ===================================================================
    # PROBLEM 7 – 16: Diverse Classic DS&A Algorithm Questions (V39 – V48)
    # ===================================================================
    {
        "id": "V39",
        "category": "Fully Correct (Suboptimal)",
        "question_text": "Given an array of integers nums and a target, return indices of the two numbers that add up to target. Assume exactly one solution exists.",
        "ground_truth": "Language = Java ✅ | Verdict = Fully Correct (functionally) | Note = O(n²) brute force instead of the expected O(n) HashMap approach — correct output, suboptimal complexity, not a bug.",
        "code": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();
        int target = sc.nextInt();

        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    System.out.println(i + " " + j);
                }
            }
        }
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 6.0,
        "expected_overall_max": 9.5,
        "notes": "Two Sum brute force.",
    },
    {
        "id": "V40",
        "category": "Fully Incorrect (Logic Bug)",
        "question_text": "Reverse a singly linked list in place and return the new head.",
        "ground_truth": "Language = Java ✅ | Verdict = Fully Incorrect (infinite/broken traversal) | Bug = curr.next = prev overwrites curr.next before advancing curr = curr.next, so curr immediately becomes prev — loop terminates after one iteration and only the head node gets processed. Missing the next = curr.next temp-storage step before reassignment.",
        "code": """class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public class Main {
    public static ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            curr.next = prev;
            prev = curr;
            curr = curr.next;
        }
        return prev;
    }

    public static void main(String[] args) {
        ListNode a = new ListNode(1);
        a.next = new ListNode(2);
        a.next.next = new ListNode(3);
        ListNode reversed = reverseList(a);
        while (reversed != null) {
            System.out.print(reversed.val + " ");
            reversed = reversed.next;
        }
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 5.0,
        "notes": "Reverse Linked List pointer overwriting bug.",
    },
    {
        "id": "V41",
        "category": "Fully Incorrect (Wrong Algorithm)",
        "question_text": "Given a string of ()[]{}, determine if the brackets are validly matched/nested.",
        "ground_truth": "Language = Java ✅ | Verdict = Fully Incorrect | Bug = counts brackets instead of checking nesting order/type-matching with a stack. Passes trivial cases like '()' but wrongly accepts '([)]' and '}{' as valid since counts match.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();
        int open = 0, close = 0;
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') open++;
            if (c == ')' || c == ']' || c == '}') close++;
        }
        System.out.println(open == close ? "Valid" : "Invalid");
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 4.5,
        "notes": "Valid brackets count-only instead of stack.",
    },
    {
        "id": "V42",
        "category": "Partially Correct (Init Bug)",
        "question_text": "Given an integer array (may contain negatives), find the contiguous subarray with the largest sum and return that sum.",
        "ground_truth": "Language = Java ✅ | Verdict = Partially Correct | Bug = maxSum initialized to 0 instead of Integer.MIN_VALUE (or nums[0]). Fails on all-negative arrays — e.g. [-3, -1, -7] should return -1, but this prints 0 since 0 never gets beaten by any negative running sum.",
        "code": """import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) nums[i] = sc.nextInt();

        int maxSum = 0;
        int currSum = 0;
        for (int i = 0; i < n; i++) {
            currSum = Math.max(nums[i], currSum + nums[i]);
            maxSum = Math.max(maxSum, currSum);
        }
        System.out.println(maxSum);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 7.0,
        "notes": "Kadane's 0-init bug on negative arrays.",
    },
    {
        "id": "V43",
        "category": "Partially Correct (Missing Prerequisite)",
        "question_text": "Given a list of intervals, merge all overlapping intervals and return the result.",
        "ground_truth": "Language = Java ✅ | Verdict = Partially Correct | Bug = never sorts intervals by start time before merging, so the merge-adjacent-if-overlapping logic (which is itself correct) operates on unsorted data. On this exact input it outputs [1,3] [8,10] [2,6] [15,18] unmerged/wrong instead of the correct [1,6] [8,10] [15,18].",
        "code": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        int[][] intervals = { {1, 3}, {8, 10}, {2, 6}, {15, 18} };
        List<int[]> merged = new ArrayList<>();

        for (int[] interval : intervals) {
            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {
                merged.add(interval);
            } else {
                merged.get(merged.size() - 1)[1] =
                    Math.max(merged.get(merged.size() - 1)[1], interval[1]);
            }
        }

        for (int[] iv : merged) {
            System.out.println(Arrays.toString(iv));
        }
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 6.5,
        "notes": "Merge intervals without Arrays.sort.",
    },
    {
        "id": "V44",
        "category": "Wrong Language",
        "question_text": "Given coin denominations and a target amount, return the fewest coins needed to make that amount using dynamic programming, or -1 if impossible.",
        "ground_truth": "Language = Python ❌ | Verdict = Invalid Submission — wrong language. Note: the DP logic itself is actually correct and would return 3.",
        "code": """def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1, 2, 5]
amount = 11
print(coinChange(coins, amount))""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 0.0,
        "notes": "Python coin change DP submitted as Java.",
    },
    {
        "id": "V45",
        "category": "Partially Correct (Logic Bug)",
        "question_text": "Given a string, find the length of the longest substring without repeating characters.",
        "ground_truth": "Language = Java ✅ | Verdict = Partially Correct | Bug = when a duplicate is found, only removes/advances left by one position instead of shrinking the window until the duplicate character is actually gone — should be a while (seen.contains(c)) loop, not a single if. Fails on inputs like 'abba': at the second 'b', only one character is evicted instead of shrinking past both 'a' and the first 'b', producing an inflated/wrong window size in some traces.",
        "code": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();
        Set<Character> seen = new HashSet<>();
        int maxLen = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (seen.contains(c)) {
                seen.remove(s.charAt(left));
                left++;
            }
            seen.add(c);
            maxLen = Math.max(maxLen, right - left + 1);
        }
        System.out.println(maxLen);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 3.0,
        "expected_overall_max": 6.5,
        "notes": "Sliding window single-if duplicate shrink bug.",
    },
    {
        "id": "V46",
        "category": "Mismatched (Wrong Traversal)",
        "question_text": "Given the root of a binary tree, return its level-order traversal as a list of lists (one list per level), using BFS with a queue.",
        "ground_truth": "Language = Java ✅ | Verdict = Mismatched — submission implements a recursive in-order DFS traversal that prints a flat string, not BFS level-order traversal returning a list of lists per level. Solves a related-but-different tree problem.",
        "code": """class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}

public class Main {
    public static void main(String[] args) {
        TreeNode root = new TreeNode(5);
        root.left = new TreeNode(3);
        root.right = new TreeNode(8);
        System.out.println(inorder(root));
    }

    public static String inorder(TreeNode node) {
        if (node == null) return "";
        return inorder(node.left) + node.val + " " + inorder(node.right);
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 3.5,
        "notes": "Binary tree in-order DFS instead of BFS level-order.",
    },
    {
        "id": "V47",
        "category": "Fully Correct (Alternative Approach)",
        "question_text": "Given the head of a linked list, determine if it has a cycle.",
        "ground_truth": "Language = Java ✅ | Verdict = Fully Correct | Note = uses HashSet (O(n) space) instead of the 'expected' Floyd's cycle detection / two-pointer (O(1) space), but this is a completely valid, commonly-taught alternative solution — not a lesser or buggy one.",
        "code": """import java.util.*;

class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public class Main {
    public static boolean hasCycle(ListNode head) {
        Set<ListNode> seen = new HashSet<>();
        ListNode curr = head;
        while (curr != null) {
            if (seen.contains(curr)) return true;
            seen.add(curr);
            curr = curr.next;
        }
        return false;
    }

    public static void main(String[] args) {
        ListNode a = new ListNode(1);
        ListNode b = new ListNode(2);
        a.next = b;
        b.next = a; // cycle
        System.out.println(hasCycle(a));
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 7.0,
        "expected_overall_max": 10.0,
        "notes": "Cycle detection using HashSet O(n) space.",
    },
    {
        "id": "V48",
        "category": "Fully Incorrect (Missing Key Step)",
        "question_text": "Given an array of strings, group the anagrams together and print each group.",
        "ground_truth": "Language = Java ✅ | Verdict = Fully Incorrect | Bug = builds the grouping key from the unsorted characters (new String(chars) without Arrays.sort(chars) first), so anagrams like 'eat'/'tea'/'ate' get different keys and end up in separate groups instead of one. Output is 6 groups of 1 instead of the correct 3 groups: {eat,tea,ate}, {tan,nat}, {bat}.",
        "code": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        String[] words = {"eat", "tea", "tan", "ate", "nat", "bat"};
        Map<String, List<String>> groups = new HashMap<>();

        for (String w : words) {
            char[] chars = w.toCharArray();
            String key = new String(chars);
            groups.computeIfAbsent(key, k -> new ArrayList<>()).add(w);
        }

        for (List<String> group : groups.values()) {
            System.out.println(group);
        }
    }
}""",
        "target_language": "Java",
        "expected_overall_min": 1.0,
        "expected_overall_max": 4.5,
        "notes": "Group anagrams missing sort step.",
    },
]

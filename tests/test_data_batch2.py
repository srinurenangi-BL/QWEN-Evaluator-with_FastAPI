"""
test_data_batch2.py — Batch 2: Multiple Questions, Targeted Variants

5 different Java questions, each with 4 variants specifically designed to
re-test confirmed blind spots on fresh code the model hasn't seen before.

Purpose: Determine if blind spots (syntax errors, infinite loops, shape-correct
bugs, ugly-code penalty) are universal or question-specific.
"""

# ---------------------------------------------------------------------------
# Question bank — 5 questions × 4 variants = 20 test cases
# ---------------------------------------------------------------------------

# ===================================================================
# QUESTION 1: Reverse a string without using StringBuilder.reverse()
# ===================================================================
Q1_TEXT = (
    "Write a Java program that reads a string from the user and prints it reversed, "
    "without using StringBuilder.reverse() or any built-in reverse method. "
    "Use a character-level approach (e.g., loop from end to start, or swap in a char array)."
)

Q1_VARIANTS = [
    # V19 — Fully Correct
    {
        "id": "V19",
        "category": "Fully Correct",
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
        "notes": "Clean char-array swap approach. Should score near-perfect.",
    },

    # V20 — Missing semicolons (2 of them)
    {
        "id": "V20",
        "category": "Does Not Compile (Syntax Error)",
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
        "notes": "Re-testing syntax error blind spot on different code.",
    },

    # V21 — Off-by-one: left <= right causes double-swap on odd-length strings (still correct output, but inefficient)
    # Actually let's make it a real bug: starts right at chars.length (ArrayIndexOutOfBounds)
    {
        "id": "V21",
        "category": "Partially Correct (Runtime Crash)",
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
        "notes": "Off-by-one causing ArrayIndexOutOfBounds. Shape-correct bug territory.",
    },

    # V22 — Infinite loop: left and right never move
    {
        "id": "V22",
        "category": "Runs But Hangs",
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
        "notes": "Re-testing infinite loop blind spot on different code.",
    },
]

# ===================================================================
# QUESTION 2: Check if a number is prime
# ===================================================================
Q2_TEXT = (
    "Write a Java program that reads an integer from the user and prints whether it is "
    "a prime number or not. Handle edge cases: numbers less than 2 are not prime. "
    "Use an efficient approach (check divisibility up to sqrt(n))."
)

Q2_VARIANTS = [
    # V23 — Fully Correct
    {
        "id": "V23",
        "category": "Fully Correct",
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
        "notes": "Clean prime check with sqrt optimization.",
    },

    # V24 — Returns true for 1 (edge case bug)
    {
        "id": "V24",
        "category": "Partially Correct (Edge Case Bug)",
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
        "notes": "Subtle edge case: n < 1 instead of n < 2. Shape-correct bug.",
    },

    # V25 — void method returning boolean (compile error)
    {
        "id": "V25",
        "category": "Does Not Compile (Type Error)",
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
        "notes": "Re-testing void+return blind spot on different code.",
    },

    # V26 — Correct but horrifically formatted (one-liner)
    {
        "id": "V26",
        "category": "Fully Correct (Poor Style)",
        "ground_truth": "Functionally correct. Crushed formatting, single-letter vars, no whitespace.",
        "code": """import java.util.*;public class Main{public static void main(String[]a){int n=new Scanner(System.in).nextInt();if(n<2){System.out.println("Not Prime");return;}boolean p=true;for(int i=2;i<=Math.sqrt(n);i++){if(n%i==0){p=false;break;}}System.out.println(p?"Prime":"Not Prime");}}""",
        "target_language": "Java",
        "expected_overall_min": 5.0,
        "expected_overall_max": 9.0,
        "notes": "Re-testing ugly-code penalty on different code. Should be high completeness, low code_quality.",
    },
]

# ===================================================================
# QUESTION 3: Count vowels and consonants in a string
# ===================================================================
Q3_TEXT = (
    "Write a Java program that reads a string and counts the number of vowels and "
    "consonants in it. Ignore spaces, digits, and special characters — only count "
    "alphabetic characters. Print the counts in the format: 'Vowels: X, Consonants: Y'."
)

Q3_VARIANTS = [
    # V27 — Fully Correct
    {
        "id": "V27",
        "category": "Fully Correct",
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
        "notes": "Clean solution with proper Character.isLetter() guard.",
    },

    # V28 — Space counted as consonant (missing isLetter guard)
    {
        "id": "V28",
        "category": "Partially Correct (Logic Bug)",
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
        "notes": "Known blind spot from vowel/consonant test in prior profile. Re-testing.",
    },

    # V29 — Missing closing brace for class
    {
        "id": "V29",
        "category": "Does Not Compile (Syntax Error)",
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
        "notes": "Re-testing missing-brace syntax error on different code.",
    },

    # V30 — Wrong language (Python)
    {
        "id": "V30",
        "category": "Wrong Language",
        "ground_truth": "Python code. Logic is correct but wrong language.",
        "code": """s = input().lower()
vowels = sum(1 for c in s if c in 'aeiou')
consonants = sum(1 for c in s if c.isalpha() and c not in 'aeiou')
print(f"Vowels: {vowels}, Consonants: {consonants}")""",
        "target_language": "Java",
        "expected_overall_min": 0.0,
        "expected_overall_max": 0.0,
        "notes": "Re-testing wrong-language detection on different code.",
    },
]

# ===================================================================
# QUESTION 4: Find GCD of two numbers using Euclidean Algorithm
# ===================================================================
Q4_TEXT = (
    "Write a Java program that reads two positive integers and prints their Greatest "
    "Common Divisor (GCD) using the Euclidean algorithm. The Euclidean algorithm "
    "repeatedly replaces the larger number with the remainder of dividing the larger "
    "by the smaller until one becomes zero."
)

Q4_VARIANTS = [
    # V31 — Fully Correct
    {
        "id": "V31",
        "category": "Fully Correct",
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

    # V32 — Method exists but never called from main (dead code)
    {
        "id": "V32",
        "category": "Runs But No Output",
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
        "notes": "Re-testing dead code detection on different code.",
    },

    # V33 — Prints LCM instead of GCD (wrong problem)
    {
        "id": "V33",
        "category": "Mismatched (Wrong Problem)",
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
        "notes": "Prints LCM labeled as GCD. Tests mismatched-output detection.",
    },

    # V34 — Infinite recursion (stack overflow)
    {
        "id": "V34",
        "category": "Runs But Crashes (Stack Overflow)",
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
        "notes": "Infinite recursion — gcd(a, b) calls gcd(a, b) unchanged. StackOverflow.",
    },
]

# ===================================================================
# QUESTION 5: Check if an array is sorted in ascending order
# ===================================================================
Q5_TEXT = (
    "Write a Java program that reads an array of integers and checks whether the array "
    "is sorted in strictly ascending order (each element must be strictly greater than "
    "the previous one). Print 'Sorted' or 'Not Sorted'."
)

Q5_VARIANTS = [
    # V35 — Fully Correct
    {
        "id": "V35",
        "category": "Fully Correct",
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

    # V36 — Uses >= instead of <= (checks descending instead of ascending)
    {
        "id": "V36",
        "category": "Partially Correct (Wrong Condition)",
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
        "notes": "Inverted comparison — checks descending order not ascending. Should be obvious.",
    },

    # V37 — Variable typo: 'sorte' instead of 'sorted'
    {
        "id": "V37",
        "category": "Does Not Compile (Typo)",
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
        "notes": "Re-testing variable typo compile error on different code.",
    },

    # V38 — Empty stub
    {
        "id": "V38",
        "category": "Unattempted",
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
        "notes": "Empty stub with just a scanner. No logic at all.",
    },
]

# ===================================================================
# Combined list for the runner
# ===================================================================
QUESTIONS = {
    "Q1": Q1_TEXT,
    "Q2": Q2_TEXT,
    "Q3": Q3_TEXT,
    "Q4": Q4_TEXT,
    "Q5": Q5_TEXT,
}

# Map variant IDs to their question
VARIANT_QUESTION_MAP = {}
for v in Q1_VARIANTS:
    VARIANT_QUESTION_MAP[v["id"]] = "Q1"
for v in Q2_VARIANTS:
    VARIANT_QUESTION_MAP[v["id"]] = "Q2"
for v in Q3_VARIANTS:
    VARIANT_QUESTION_MAP[v["id"]] = "Q3"
for v in Q4_VARIANTS:
    VARIANT_QUESTION_MAP[v["id"]] = "Q4"
for v in Q5_VARIANTS:
    VARIANT_QUESTION_MAP[v["id"]] = "Q5"

# All test cases combined
TEST_CASES_BATCH2 = Q1_VARIANTS + Q2_VARIANTS + Q3_VARIANTS + Q4_VARIANTS + Q5_VARIANTS

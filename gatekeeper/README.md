# CTF Write-Up: `gatekeeper`

![Category](https://img.shields.io/badge/Category-Reverse%20Engineering-blue)
![Platform](https://img.shields.io/badge/Platform-x86__64%20ELF-lightgrey)
![Tools](https://img.shields.io/badge/Tools-Ghidra%20%7C%20GDB%20%7C%20Python-orange)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy%2FMedium-green)

## Executive Summary

During reverse engineering analysis of the `gatekeeper` ELF binary using **Ghidra**, a logic flow paradox was identified in the input validation routine. The program attempted to enforce a numerical range requirement alongside a strict string length check. The vulnerability stems from an improper base parameter in the standard library function `strtol()`, which allowed for a complete control flow bypass using hexadecimal payload formatting.

---

## Technical Analysis

### 1. Disassembly & Decompilation

Analysis of the `main` control function in Ghidra revealed the core control flow and input processing logic:

```c
// Decompiled representation of the main validation logic
int main(int argc, char **argv) {
    char user_input[16];
    
    printf("Enter PIN: ");
    fgets(user_input, sizeof(user_input), stdin);
    
    // Stripping newline
    user_input[strcspn(user_input, "\n")] = 0;

    long val = strtol(user_input, NULL, 16); // Input converted using Base-16 (Hex)
    size_t len = strlen(user_input);

    // Validation checks
    if (val >= 1000 && val < 10000) {
        if (len == 3) {
            reveal_flag();
            return 0;
        }
    }

    puts("Access Denied!");
    return 1;
}
```

### 2. Identifying the Logic Paradox

The application imposes two distinct conditions before executing `reveal_flag()`:

1. **Numerical Range Condition:** `val >= 1000 && val < 10000` (Decimal bounds: $[1000, 9999]$).
2. **Length Condition:** `strlen(user_input) == 3`.

In base-10 decimal representation, any string satisfying $val \ge 1000$ requires **at least 4 characters** (`"1000"` to `"9999"`). Conversely, the maximum 3-character decimal string is `"999"`, creating a standard logic deadlock.

### 3. Exploitation via Hex Loophole

The flaw exists in `strtol(user_input, NULL, 16)` using **base 16** instead of base 10. 

Because input characters are parsed as hexadecimal digits, 3-character strings map to significantly higher integer values:

* **Lower Bound:** `"3E8"` (Base 16) $\rightarrow 3(16^2) + 14(16^1) + 8(16^0) = 1000_{10}$
* **Upper Bound:** `"FFF"` (Base 16) $\rightarrow 15(16^2) + 15(16^1) + 15(16^0) = 4095_{10}$

Since $1000 \le 4095 < 10000$, any 3-character hex string between `3E8` and `FFF` satisfies both conditions simultaneously.

---

## Proof of Concept

Executing the binary with the 3-character hex payload `FFF`:

```bash
$ ./gatekeeper
Enter PIN: FFF
[+] Access Granted! Unlocking flag...
[+] Flag: FLAG{REDACTED_FOR_PORTFOLIO}
```

---

## Remediation & Best Practices

1. **Explicit Base Handling:** If the application expects decimal user input, explicitly specify base `10` in `strtol()` calls:
   ```c
   long val = strtol(user_input, NULL, 10);
   ```
2. **Canonical Length Checks:** Validate string length and input characters prior to conversion, or unify integer boundary checks with input constraints to avoid representation mismatches.

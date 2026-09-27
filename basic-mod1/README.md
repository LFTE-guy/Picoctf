# basic-mod1 - picoCTF

**Difficulty:** Medium  
**Category:** Cryptography  
**Platform:** picoCTF / CyLab Security Academy

## Challenge

A list of numbers was intercepted. To decode the message:

- Take each number mod 37.
- Map the result to a character set:
  - 0–25 → A–Z (uppercase)
  - 26–35 → 0–9
  - 36 → underscore (`_`)

## Solution

I wrote a Python script (`decrypt.py`) that:

1. Reads the list of numbers from `message.txt`.
2. Computes `num % 37` for each number.
3. Maps the remainder to the correct character using a string index.
4. Prints each step (remainder and character) to verify the logic.

The script output the decoded message: `R0UND_N_R0UND_65371195`.

## Code

See [`decrypt.py`](./decrypt.py).

Key logic:
```python
set = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
r = int(num) % 37
print(set[r], end='')

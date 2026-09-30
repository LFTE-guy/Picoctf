# Transformation — CTF Writeup

## Overview
This writeup documents the solution for the Transformation challenge. The challenge provided an encrypted source file (`enc`) containing Unicode characters. Each character in the file was a 16-bit container packing two distinct 8-bit ASCII characters together.

## Technical Breakdown

### The Packing Mechanism
The encryption formula compressed two 8-bit characters (char1 and char2) into a single 16-bit integer Z:

Z = (char1 << 8) + char2

- High Byte (First Character): Shifted 8 bits to the left, occupying the top 8 bits.
- Low Byte (Second Character): Placed directly into the bottom 8 bits.

## What Was Learned & Implemented

1. Bitwise Right-Shift (`>> 8`):
   Extracted the high byte (first character) by sliding the upper 8 bits down into the lower position while discarding the bottom 8 bits.

2. Bitwise AND Masking (`& 0x00FF`):
   Isolated the low byte (second character) by zeroing out the upper 8 bits while preserving the bottom 8 bits untouched.

3. Register Mutation vs. Static Inspection:
   Realized that bitwise operations alter the value being evaluated rather than merely looking at it. Both operations must be performed independently on the original untouched character integer value.

4. Type Safety in Scripting:
   Fixed handling of integer-to-character conversions using `chr()`, ensuring type consistency when concatenating high-byte and low-byte string outputs.

## How to Run
Ensure your Python script and the `enc` file are in the same directory:

```bash
python3 bitwise.py

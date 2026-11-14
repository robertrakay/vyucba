---
layout: custom_default
title: Week 1
permalink: /Logické_riadiace_systémy/Weeks/week1/
show_sidebar: false
---
# Week 1
Siemens programming Style Guide 
[PDF link - official Siemens](https://support.industry.siemens.com/cs/attachments/109478084/81318674_Programming_Styleguide_DOC_V2_1_0_en.pdf?download=true/)

Here is the Siemens Style Guide summary 

***

# Siemens S7-1200/S7-1500 Programming Style Guide
### A Student Summary for Professional Code Engineering

> **Instructor Note:**
> "Hello class! As a mechatronics instructor, I often see students write code that 'works' but is impossible to fix or read a month later. This document from Siemens is the gold standard for avoiding that mess. It moves you from 'making it work' to 'engineering a solution.'"

---

## 1. Environment & General Settings
Setting up your workspace correctly is the first step toward professional code.

### Standardize the Engineering Environment
Set your TIA Portal environment to use **English (US)** for the interface and **"International"** for mnemonics. This ensures system constants and syntax are consistent regardless of the developer's location, allowing for seamless global collaboration.



> **Example:** In TIA Portal settings, change the "Mnemonic" dropdown to **International**. You will see `%I0.0` (International) instead of `%E0.0` (German).

### Enforce Strict Code Checks
Enable the **"IEC check"** for all new blocks to ensure type safety. This forces the compiler to flag data type mismatches (like mixing Integers and Words without conversion) that usually cause silent runtime errors.

> **Example:** If you try to move a value of `-1` into a `USInt` (0-255) variable, the IEC check will flag this as an error during compilation rather than letting it crash the PLC during operation.

---

## 2. Naming Conventions (Nomenclature)
Clear naming prevents confusion between local variables and global objects.

### Use Consistent Casing Styles
* **UpperCamelCase (PascalCase):** Use for structural objects like Blocks, Data Types, and Tag Tables.
* **lowerCamelCase:** Use for code elements like variables and parameters.

> **Example:** Name your Function Block `MotorControl` (UpperCamelCase) but name the variable inside it `currentSpeed` (lowerCamelCase).

### Apply Variable Prefixes
Use specific prefixes to identify the scope of a variable. This prevents bugs caused by confusing a local temporary value with a value retained across cycles.

| Scope | Prefix | Description |
| :--- | :--- | :--- |
| **Temporary** | `temp` | Variables that reset every cycle. |
| **Static** | `stat` | Variables that retain memory. |
| **Instance** | `inst` | Multi-instance calls. |

> **Example:** Rename a temporary integer used for looping from `index` to `#tempIndex`, and a static state variable from `state` to `#statState`.

### Use Symbolic Constants
Avoid "magic numbers" (hard-coded numeric values). Define them as symbolic constants in `UPPER_CASE`.

> **Example:** instead of writing `IF #speed > 1500`, define a constant named `MAX_RPM` with a value of 1500:
>
> `IF #speed > #MAX_RPM`

---

## 3. Reusability & Library Design
Write code that can be dragged and dropped into any future project without breaking.

### Create Hardware-Independent Logic
Write Function Blocks (FBs) and Functions (FCs) that rely **only** on their interface parameters. Avoid direct references to global DBs or physical hardware addresses inside the logic.

> **Example:** Instead of referencing global tag `"Conveyor_DB".RunCmd`, create an **Input parameter** named `runCommand` and pass the global tag to it when calling the block.

### Use Multi-Instances
When calling a sub-block (like a timer or another FB) inside a Function Block, use **multi-instances** instead of generating a separate Instance DB for every call. This reduces data block clutter.



> **Example:** When using an `IEC_Timer` inside your `MotorControl` FB, declare it as `#instTimer` in the **Static variables** section rather than creating a new `IEC_Timer_DB`.

---

## 4. Architecture & Logic Design
Structure your program flow for predictability and readability.

### Implement Standardized Control Behaviors
Follow PLCopen standards for asynchronous blocks:
* **Enable (Level-triggered):** Keeps a process running while high (e.g., PID Loop).
* **Execute (Edge-triggered):** Triggers a one-time job (e.g., Sending a message).

> **Example:** For a communication block, use an `execute` input to send a message once. For a PID controller, use an `enable` input to keep the control loop active.

### Use CASE Statements for State Machines
Prefer `CASE` instructions over complex `IF...ELSIF` chains when programming sequencers. Always include an `ELSE` branch to catch undefined states.



> **Example:** Use `CASE #statState OF` to switch between `#IDLE`, `#RUNNING`, and `#ERROR` states. This is much cleaner than deeply nested `IF` statements.

---

## 5. Performance & Stability
Write efficient code that protects the CPU memory.

### Optimize Data Access
Pass large structured data (like Arrays or UDTs) as **InOut** parameters. This utilizes "Call by Reference" (passing a pointer) rather than copying the data, saving memory and time.

> **Example:** If processing an array of 1000 tracking records, pass the array via `InOut` so the CPU doesn't have to duplicate the entire array every time the block is called.

### Initialize Temporary Variables
Always write a value to a temporary variable (`temp`) before reading it. Temp memory is reused by other blocks, so uninitialized variables may contain "garbage" data.

> **Example:** At the very top of your FC, add the line `#tempCalculatedResult := 0;` to ensure the variable starts clean every cycle.

---

## 6. Error Handling
Make your code diagnostic-friendly for the maintenance technicians.

### Report Status and Errors
Blocks should provide a status word output.
* **Bit 15 (Most Significant Bit):** Indicates an Error.
* **Remaining Bits:** Provide a specific error code.

> **Example:** Instead of just an output `Error = TRUE`, provide a Status word where `16#8201` indicates "Error: Invalid Parameter Configuration."

### Handle ENO (Enable Output)
Ensure your blocks assign a value to `ENO` (usually `TRUE`). If a runtime error occurs (like division by zero), the system sets `ENO` to `FALSE`, allowing you to catch crashes.

> **Example:** In SCL, ensure your code ends with `ENO := TRUE;` unless a specific error condition requires you to report a failure.


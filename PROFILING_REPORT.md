## 1. FishComplete.format_completion() benchmark

```bash
python profiling_benchmark.py
```

**Výsledky:**
```
Iterations: 10,000
Total time: 0.0158 s
Average time per iteration: 0.0016 ms
Average time per item: 0.3956 μs
```

## 2. String replace - PRED optimalizáciou

**Testované s 1,000,000 iterácií**

| Metrika              | Hodnota    |
|----------------------|------------|
| Total time           | 0.8163 s   |
| Avg per operation    | 0.8163 μs  |
| Replace calls        | 200,000    |

**Bottleneck:** `str.replace()` sa volá aj keď string neobsahuje `\n`

## 3. Implementovaná optimalizácia

### Zmena v `src/click/shell_completion.py`

**PRED:**
```python
value = item.value.replace("\n", r"\n")
help_escaped = help_.replace("\n", r"\n")
```

**PO:**
```python
# Check-before-replace pattern
value = item.value.replace("\n", r"\n") if "\n" in item.value else item.value
help_escaped = help_.replace("\n", r"\n") if "\n" in help_ else help_
```

**Princíp:** Skontroluj či string obsahuje `\n` pred volaním `replace()`

## 4. String replace - PO optimalizácii

**Testované s 1,000,000 iterácií**

| Metrika              | Hodnota    |
|----------------------|------------|
| Total time           | 0.4529 s   |
| Avg per operation    | 0.4529 μs  |
| Replace calls        | 50,000     |

## 5. Porovnanie PRED vs. PO

| Metrika              | PRED       | PO         | Zlepšenie   |
|----------------------|------------|------------|-------------|
| **Total time**       | 0.8163 s   | 0.4529 s   | **-44.52%** |
| **Avg per operation**| 0.8163 μs  | 0.4529 μs  | **-44.52%** |
| **Replace calls**    | 200,000    | 50,000     | **-75%**    |
| **Time saved**       | -          | 0.3634 s   | -           |

**Hlavné zlepšenia:**
- Čas: -44.52%
- Function calls: -75%

## 6. cProfile analýza

**Top funkcie (zoradené podľa cumulative time):**

```
         9598 function calls (9597 primitive calls) in 0.007 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    0.007    0.007 profiling_benchmark.py:43(benchmark_fish_format_completion)
     4000    0.003    0.000    0.003    0.000 src/click/shell_completion.py:423(format_completion)
     2000    0.000    0.000    0.000    0.000 {method 'replace' of 'str' objects}
     2000    0.000    0.000    0.000    0.000 {built-in method time.perf_counter}
     1000    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
```

**Nástroj:** Python cProfile (Time profiling)

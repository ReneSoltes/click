## 1. Výsledky PRED optimalizáciou

### Benchmark

```bash
python profiling_benchmark.py
```

**cProfile výstup:**
```
ncalls  tottime  cumtime  function
100000  0.071   0.092    format_completion()
200000  0.021   0.021    str.replace()
```

| Metrika | Hodnota |
|---------|---------|
| Total time | 0.0735 s |
| Avg per operation | 0.7345 μs |
| Replace calls | 200,000 |

**Bottleneck:** `str.replace()` sa volá aj keď string neobsahuje `\n`

## 2. Implementovaná optimalizácia

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

## 3. Výsledky PO optimalizácii

```bash
python profiling_benchmark.py
```

**cProfile výstup:**
```
ncalls  tottime  cumtime  function
100000  0.044   0.055    format_completion()
50000   0.006   0.006    str.replace()
```

| Metrika | Hodnota |
|---------|---------|
| Total time | 0.0442 s |
| Avg per operation | 0.4418 μs |
| Replace calls | 50,000 |

## 4. Porovnanie PRED vs. PO

| Metrika | PRED | PO | Zlepšenie |
|---------|------|-----|-----------|
| **Total time** | 0.0735 s | 0.0442 s | **-40.05%** |
| **Avg per operation** | 0.7345 μs | 0.4418 μs | **-40.05%** |
| **Replace calls** | 200,000 | 50,000 | **-75%** |
| **Time saved** | - | 0.0293 s | - |

**Hlavné zlepšenia:**
- Čas: -40.05%
- Function calls: -75%

## 5. Overenie

Všetky testy prejdú:
```bash
pytest tests/test_shell_completion.py -v
# Result: 53 passed ✅
```

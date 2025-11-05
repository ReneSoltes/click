# Code Coverage Report - Click Project

**Študent:** René Solteš
**Projekt:** Click (Python CLI framework)
**Vetva:** coverage-testing
**Dátum:** 4. November 2025

---

## 📊 Meranie pokrytia kódu testami

### 1. Počiatočné meranie (PRED pridaním testov)

**Nástroj:** pytest-cov (Coverage.py)
**Príkaz:** `pytest tests/ --cov=src/click --cov-report=term`

#### Metriky celkového pokrytia:

| Metrika | Hodnota |
|---------|---------|
| **Total Statements** | 4354 |
| **Covered Lines (absolute)** | 3574 riadkov |
| **Covered Lines (relative)** | **80%** |
| **Missing Lines** | 780 riadkov |
| **Branch Coverage** | 89% (1377/1546) |
| **Tests Passed** | 1314 |

#### Pokrytie jednotlivých modulov (PRED):

| Modul | Statements | Miss | Branch | BrPart | Cover |
|-------|-----------|------|--------|--------|-------|
| `shell_completion.py` | 219 | **19** | 60 | 6 | **89%** |
| `decorators.py` | 179 | **54** | 60 | 1 | **66%** |
| `core.py` | 1192 | 86 | 554 | 43 | 91% |
| `types.py` | 426 | 30 | 116 | 7 | 93% |
| `utils.py` | 234 | 47 | 96 | 13 | 76% |

**Identifikované oblasti s nízkym pokrytím:**
- ❌ `decorators.py` - 66% (najnižšie)
- ❌ `shell_completion.py` - 89% (edge cases)
- ❌ `utils.py` - 76%

---

### 2. Vytvorenie nových testov

**Súbor:** `tests/test_coverage_improvement.py`
**Počet testovacích metód:** 11

#### Testované oblasti:

##### A) Shell Completion (8 testov):
1. ✅ **test_completion_item_with_none_help** - Test handling None help text
2. ✅ **test_fish_complete_format_with_empty_help** - Test empty help string
3. ✅ **test_fish_complete_format_with_newlines_in_value** - Test newline escaping in values
4. ✅ **test_bash_complete_format_with_special_chars** - Test special characters
5. ✅ **test_zsh_complete_format_with_colon_in_help** - Test colon handling in Zsh
6. ✅ **test_add_completion_class_custom** - Test custom completion class registration
7. ✅ **test_shell_complete_get_completion_args_abstract** - Test abstract method implementation
8. ✅ **test_completion_item_equality** - Test CompletionItem attributes

##### B) Decorators (3 testy):
9. ✅ **test_version_option_with_custom_message** - Test custom version message template
10. ✅ **test_version_option_with_package_name** - Test version from package metadata (with mock)
11. ✅ **test_help_option_custom_names** - Test custom help option names

#### Použité techniky test doubles:

**1. Mocks:**
```python
from unittest.mock import Mock, MagicMock, patch

# Mock objekty pre CLI context
fish = FishComplete(cli=Mock(), ctx_args={}, prog_name="test", complete_var="TEST")

# Mock importlib.metadata.version
with patch('importlib.metadata.version', return_value="2.0.0"):
    # Test code
```

**2. Fakes:**
```python
# Fake completion class pre testovanie registrácie
class CustomComplete(ShellComplete):
    name = "custom"
    source_template = "# custom template"

    def format_completion(self, item):
        return f"custom:{item.value}"
```

**3. Test Data Objects:**
```python
# CompletionItem objekty s rôznymi kombináciami hodnôt
item = CompletionItem(type="plain", value="--option", help=None)
```

---

### 3. Finálne meranie (PO pridaní testov)

**Príkaz:** `pytest tests/ --cov=src/click --cov-report=term --cov-report=html`

#### Metriky celkového pokrytia:

| Metrika | Hodnota | Zmena |
|---------|---------|-------|
| **Total Statements** | 4354 | - |
| **Covered Lines (absolute)** | 3599 riadkov | **+25** ✅ |
| **Covered Lines (relative)** | **81%** | **+1%** ✅ |
| **Missing Lines** | 755 riadkov | **-25** ✅ |
| **Branch Coverage** | 89% (1372/1546) | - |
| **Tests Passed** | 1325 | **+11** ✅ |

#### Pokrytie jednotlivých modulov (PO):

| Modul | Statements | Miss | Branch | BrPart | Cover | Zmena |
|-------|-----------|------|--------|--------|-------|-------|
| `shell_completion.py` | 219 | **19** | 60 | 6 | **89%** | - |
| `decorators.py` | 179 | **32** | 60 | 5 | **79%** | **+13%** ✅ |
| `core.py` | 1192 | 83 | 554 | 44 | 91% | - |

**Najväčšie zlepšenia:**
- ✅ `decorators.py`: **66% → 79%** (+13 percentage points, -22 missed lines)
- ✅ `core.py`: **91% → 91%** (-3 missed lines)

---

### 4. Porovnanie výsledkov

#### Absolútne hodnoty:

| Metrika | PRED | PO | Rozdiel |
|---------|------|-----|---------|
| Covered Lines | 3574 | 3599 | **+25** ✅ |
| Missing Lines | 780 | 755 | **-25** ✅ |
| Total Coverage | 80% | 81% | **+1%** ✅ |

#### Relatívne zlepšenie:

```
Pôvodné pokrytie:  ████████████████████░░░░░░░░  80%
Nové pokrytie:     ████████████████████▓░░░░░░░  81%
                                        ↑ +1%
```

#### Graf zlepšenia v decorators.py:

```
Pôvodné pokrytie:  █████████████░░░░░░░  66%
Nové pokrytie:     ███████████████▓░░░░  79%
                                  ↑ +13%
```

---

### 5. HTML Report

**Lokácia:** `htmlcov/index.html`

HTML report obsahuje:
- ✅ Detailný prehľad pokrytia každého súboru
- ✅ Zvýraznenie pokrytých/nepokrytých riadkov (zelená/červená)
- ✅ Branch coverage analysis
- ✅ Interaktívne zobrazenie zdrojového kódu

**Otvorenie reportu:**
```bash
# Linux/WSL
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

---

## 📝 Záver

### Dosiahnuté ciele:

✅ **Zmerané počiatočné pokrytie:** 80% (3574/4354 riadkov)
✅ **Vytvorené nové testy:** 11 testovacích metód
✅ **Použité test doubles:** Mocks, Fakes, Test Data Objects
✅ **Zlepšené pokrytie:** 81% (3599/4354 riadkov)
✅ **Absolútne zlepšenie:** +25 pokrytých riadkov
✅ **Najväčší posun:** decorators.py (+13%)

### Metriky code coverage:

| Typ metriky | Hodnota |
|-------------|---------|
| **Line Coverage** | 81% |
| **Branch Coverage** | 89% |
| **Function Coverage** | ~85% (odhadované) |
| **Statement Coverage** | 81% |

### Oblasti pre ďalšie zlepšenie:

1. `_winconsole.py` - 0% (Windows-specific, nevykonateľné na Linux)
2. `_termui_impl.py` - 56% (terminál-specific funkcie)
3. `_compat.py` - 67% (compatibility layer)
4. `utils.py` - 76% (utility funkcie)

---

## 🔗 Odkazy

- **Testovací súbor:** `tests/test_coverage_improvement.py`
- **Coverage report:** `htmlcov/index.html`
- **Projekto vetva:** `coverage-testing`
- **Click dokumentácia:** https://click.palletsprojects.com/

---

**Poznámka:** Testy súvisiace s opravou issue #3043 (Fish shell completion) sa nenachádzajú v tomto súbore - tie sú v `tests/test_shell_completion.py` a boli vytvorené v predchádzajúcej fáze projektu.

# OverlapCalculator - Complete Documentation

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Mathematical Background](#mathematical-background)
4. [Installation Requirements](#installation-requirements)
5. [Quick Start](#quick-start)
6. [Class: OverlapCalculator](#class-overlapcalculator)
7. [Methods Reference](#methods-reference)
8. [Usage Examples](#usage-examples)
9. [Understanding Output](#understanding-output)
10. [Performance Considerations](#performance-considerations)
11. [Best Practices](#best-practices)
12. [Visualization Guide](#visualization-guide)
13. [Common Use Cases](#common-use-cases)
14. [Troubleshooting](#troubleshooting)
15. [FAQ](#faq)
16. [Method Reference Table](#method-reference-table)
17. [Version History](#version-history)
18. [License](#license)
19. [Support](#support)

---

## Overview

**OverlapCalculator** is a Python class for comprehensive analysis of overlaps between multiple sets. It provides tools to compute intersections, exclusive elements, pairwise relationships, and detailed statistics for any number of sets.

### Design Philosophy

The OverlapCalculator is designed with these core principles:

1. **Simplicity**: Intuitive API that works out of the box
2. **Flexibility**: Multiple input formats and query options
3. **Performance**: Optimized algorithms with result caching
4. **Completeness**: Handles all 2^n - 1 possible combinations
5. **Reproducibility**: Deterministic results with sorted outputs

### Key Concepts

- **Set Overlap**: Elements common to two or more sets
- **Exclusive Elements**: Elements unique to a single set
- **Jaccard Similarity**: Measure of set similarity (0.0 to 1.0)
- **Combinations**: All possible subsets (2^n - 1 for n sets)
- **Intersection**: Common elements between sets (∩ operator)
- **Union**: All elements across sets (∪ operator)

## Features

| Feature | Description | Use Case |
|----------|-------------|-----------|
| ✅ Compute all combinations | All 2^n - 1 possible intersections | Complete analysis |
| ✅ Exclusive elements | Elements unique to each set | Venn diagrams, feature selection |
| ✅ Pairwise matrices | Overlap and Jaccard similarity | Set comparison |
| ✅ Multiple input formats | Dict, list, or tuples | Flexibility |
| ✅ Size filtering | min_size and max_size parameters | Focus on significant overlaps |
| ✅ Flexible querying | Specific combinations or all combinations | Interactive analysis |
| ✅ Summary statistics | Comprehensive overview | Quick insights |
| ✅ Pandas DataFrame | Easy analysis and export | Data science workflows |
| ✅ Dictionary output | Programmatic access | Custom processing |
| ✅ Result caching | Avoid recomputation | Performance |
| ✅ Sorted outputs | Deterministic, reproducible | Consistency |
| ✅ Plot-ready data | Optimized for Venn diagrams | Visualization |

---

## Mathemal Background

### Set Theory Fundamentals

OverlapCalculator is based on fundamental set theory operations:

#### Intersection (∩)

The **intersection** of sets A and B contains elements present in **both** sets:

```
A ∩ B = {x | x ∈ A and x ∈ B}
```

**Example:**
```
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
A ∩ B = {3, 4}
```

#### Union (∪)

The **union** of sets A and B contains elements present in **either** set:

```
A ∪ B = {x | x ∈ A or x ∈ B}
```

**Example:**
```
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
A ∪ B = {1, 2, 3, 4, 5, 6}
```

#### Difference (-)

The **difference** A - B contains elements in A but **not** in B:

```
A - B = {x | x ∈ A and x ∉ B}
```

**Example:**
```
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
A - B = {1, 2}
```

### Power Set and Combinations

For n sets, the **power set** contains 2^n possible subsets (including the empty set).

Excluding the empty set, we have **2^n - 1** non-empty combinations.

**Example for n=3:**
```
Total combinations: 2^3 - 1 = 7

1. {Set1}                 → Single sets (3 combinations)
2. {Set2}
3. {Set3}

4. {Set1, Set2}           → Pairwise overlaps (3 combinations)
5. {Set1, Set3}
6. {Set2, Set3}

7. {Set1, Set2, Set3}      → Triple overlap (1 combination)
```

**Growth:**
```
n=3:  2^3 - 1 = 7    combinations
n=5:  2^5 - 1 = 31   combinations
n=10: 2^10 - 1 = 1,023 combinations
n=15: 2^15 - 1 = 32,767 combinations
n=20: 2^20 - 1 = 1,048,575 combinations
```

### Exclusive Elements

**Exclusive elements** are those that belong to **exactly one set**:

```
Exclusive(A) = A - (B ∪ C ∪ D ∪ ...)
```

**Visualization in Venn Diagram:**
```
For sets A, B, C:

    A-only region = Exclusive(A)
    B-only region = Exclusive(B)
    C-only region = Exclusive(C)
    A∩B region = Intersection(A, B) - C
    A∩C region = Intersection(A, C) - B
    B∩C region = Intersection(B, C) - A
    A∩B∩C region = Intersection(A, B, C)
```

### Jaccard Similarity Coefficient

**Jaccard similarity** measures similarity between two sets:

```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|

Where:
- |A ∩ B| = size of intersection
- |A ∪ B| = size of union
```

**Properties:**
- Range: 0.0 to 1.0
- 0.0 = No overlap (disjoint sets)
- 1.0 = Identical sets
- Values between indicate partial similarity

**Examples:**
```
A = {1, 2, 3, 4, 5}
B = {3, 4, 5, 6, 7}
C = {1, 2, 3, 4, 5}  (same as A)

Jaccard(A, B) = |{3,4,5}| / |{1,2,3,4,5,6,7}| = 3/7 ≈ 0.43
Jaccard(A, C) = |{1,2,3,4,5}| / |{1,2,3,4,5}| = 5/5 = 1.0
Jaccard(A, D) where D = {6,7,8,9} = 0.0 (no overlap)
```

### Inclusion-Exclusion Principle

For calculating union size of n sets:

```
|A ∪ B ∪ C| = |A| + |B| + |C|
                - |A ∩ B| - |A ∩ C| - |B ∩ C|
                + |A ∩ B ∩ C|
```

OverlapCalculator uses this implicitly through Python's `set.union()`.

---

## Installation Requirements

```python
import pandas as pd
from typing import List, Set, Dict, Tuple, Any, Optional, Union
from itertools import combinations
```

**Dependencies:**
- pandas ≥ 1.0.0
- Python ≥ 3.7 (for type hints)

**Installation:**
```bash
pip install pandas
```

No additional packages required - uses only Python standard library and pandas.

---

## Quick Start

### Basic Usage

```python
from caculated import OverlapCalculator

# Create calculator with dictionary input
data = {
    'SetA': {1, 2, 3, 4, 5},
    'SetB': {2, 3, 4, 6, 7},
    'SetC': {3, 4, 5, 7, 8}
}

calc = OverlapCalculator(data)

# Compute all overlaps (including empty)
df = calc.compute(min_size=0)
print(f"Total combinations (2^n - 1): {len(df)}")
print(df[['set_names', 'size', 'elements']])

# Get only non-empty overlaps
df_nonempty = calc.compute(min_size=1)
print(f"Non-empty combinations: {len(df_nonempty)}")

# Get summary
summary = calc.get_summary()
print(f"Total combinations: {len(summary['all_overlaps'])}")
```

---

## Class: OverlapCalculator

### Constructor

#### `__init__(data)`

Initializes the calculator with input data.

**Parameters:**
- `data`: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]
  - Dictionary: `{'name': {elements}, ...}`
  - List of sets: `[{elements1}, {elements2}, ...]` (auto-named Set1, Set2, etc.)
  - List of tuples: `[('name', {elements}), ...]`

**Raises:**
- `ValueError`: If data is empty or validation fails
- `TypeError`: If data format is not supported

**Example:**
```python
# Dictionary format
calc = OverlapCalculator({'A': {1,2,3}, 'B': {2,3,4}})

# List format (auto-named)
calc = OverlapCalculator([{1,2,3}, {2,3,4}])

# Tuple format
calc = OverlapCalculator([('A', {1,2,3}), ('B', {2,3,4})])
```

---

## Instance Variables

### Core Data Storage

| Variable | Type | Description |
|----------|------|-------------|
| `sets_names` | `List[str]` | List of set names in order |
| `sets_list` | `List[Set]` | List of actual set objects |
| `_results_df` | `Optional[pd.DataFrame]` | Cached overlap computation results |
| `_exclusive_results` | `Optional[pd.DataFrame]` | Cached exclusive element results |

### Access Pattern

These variables are primarily for internal use. Use the provided methods to access data:

```python
# Don't do this:
# print(calc.sets_names)
# print(calc._results_df)

# Do this instead:
summary = calc.get_summary()
print(summary['set_names'])
df = calc.get_dataframe()
print(df)
```

---

## Methods

### compute(min_size=0, max_size=None)

**Computes all possible overlaps between sets and returns all 2^n - 1 combinations.**

This is the core method that calculates all intersections for every possible combination of sets. It generates all 2^n - 1 non-empty subsets of the n input sets.

**Parameters:**
- `min_size`: int, default 0
  - Minimum overlap size threshold (inclusive)
  - Only returns combinations with intersection size ≥ min_size
  - Set to 0 to include empty intersections (all 2^n - 1 combinations)
  - Set to 1 to exclude empty intersections
- `max_size`: int, optional
  - Maximum overlap size threshold (inclusive)
  - Only returns combinations with intersection size ≤ max_size

**Returns:**
- `pd.DataFrame` with columns:
  - `sets`: tuple of set names
  - `set_names`: string representation (e.g., "A & B & C")
  - `n_sets`: number of sets in combination
  - `size`: size of intersection (0 for empty intersections)
  - `elements`: sorted list of intersecting elements ([] for empty)
  - `exclusive_size`: elements only in this combination
  - `exclusive_elements`: sorted list of exclusive elements

**Example:**
```python
# Get ALL combinations including empty (2^n - 1 rows)
df = calc.compute(min_size=0)
print(f"Total combinations: {len(df)}")  # Should be 2^n - 1

# Get only non-empty overlaps
df = calc.compute(min_size=1)

# Find overlaps with exactly 3 elements
df = calc.compute(min_size=3, max_size=3)
```

**Notes:**
- Results are cached in `_results_df`
- Sorted by `n_sets` (descending) then `size` (descending)
- With `min_size=0`, returns all 2^n - 1 possible combinations
- Empty intersections have `size=0` and `elements=[]`
- Use `min_size=1` to exclude empty intersections

---

### compute_exclusive()

**Computes exclusive elements for each individual set.**

Exclusive elements belong to only ONE set, not shared with any other sets.

**Returns:**
- `pd.DataFrame` with columns:
  - `set`: set name
  - `total_size`: total elements in the set
  - `exclusive_size`: elements only in this set
  - `exclusive_elements`: sorted list of exclusive elements
  - `overlap_size`: elements shared with other sets

**Formula:**
- `exclusive_elements = current_set - union(all_other_sets)`
- `overlap_size = total_size - exclusive_size`

**Example:**
```python
exclusive_df = calc.compute_exclusive()
print(exclusive_df[['set', 'exclusive_size', 'exclusive_elements']])
```

**Notes:**
- Results are cached in `_exclusive_results`

---

### get_pairwise_overlap()

**Generates pairwise overlap and Jaccard similarity matrices.**

Creates two symmetric matrices showing relationships between all pairs of sets.

**Returns:**
- `dict` with keys:
  - `overlap_matrix`: DataFrame with intersection counts
  - `jaccard_matrix`: DataFrame with Jaccard coefficients (0.0 to 1.0)

**Jaccard Similarity:**
```
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

**Example:**
```python
matrices = calc.get_pairwise_overlap()

# View overlap counts
print("Overlap Matrix:")
print(matrices['overlap_matrix'])

# View Jaccard similarities
print("\nJaccard Similarity Matrix:")
print(matrices['jaccard_matrix'].round(3))
```

**Notes:**
- Matrices are symmetric (M[i,j] = M[j,i])
- Diagonal shows set size (overlap with itself)
- Jaccard range: 0.0 (no overlap) to 1.0 (identical sets)

---

### get_summary()

**Generates comprehensive summary statistics from the most recent compute() call.**

Provides a high-level overview of overlaps based on cached results. Does NOT recompute or modify data.

**Returns:**
- `dict` with keys:
  - `n_sets`: number of input sets
  - `set_names`: list of all set names
  - `set_sizes`: dictionary mapping names to sizes
  - `total_unique_elements`: size of union of all sets
  - `all_common_size`: elements in all sets (if any)
  - `max_overlap_size`: size of largest overlap
  - `max_overlap_sets`: which sets have max overlap
  - `all_overlaps`: list of overlap dictionaries from last compute()
  - `n_combinations`: number of combinations from last compute()
  - `empty_combinations`: number of empty intersections
  - `non_empty_combinations`: number of non-empty intersections

**Example:**
```python
# First compute with min_size=0 to get all combinations
calc.compute(min_size=0)
summary = calc.get_summary()

print(f"Number of sets: {summary['n_sets']}")
print(f"Total combinations: {summary['n_combinations']}")
print(f"Empty intersections: {summary['empty_combinations']}")
print(f"Non-empty intersections: {summary['non_empty_combinations']}")
print(f"Total unique elements: {summary['total_unique_elements']}")
print(f"Elements common to all sets: {summary['all_common_size']}")
print(f"Maximum overlap: {summary['max_overlap_size']} elements in {summary['max_overlap_sets']}")

# Access all overlaps
for overlap in summary['all_overlaps']:
    print(f"{overlap['set_names']}: {overlap['elements']}")
```

**Notes:**
- Automatically triggers `compute()` if not already done
- `all_overlaps` contains whatever the last compute() produced
- Simple getter - does NOT recompute or ignore previous filters
- Call `compute(min_size=0)` explicitly before get_summary() if you need all 2^n - 1 combinations

---

### get_dataframe()

**Returns the computed overlap DataFrame from the most recent compute() call.**

Simple getter method that returns cached results. Does NOT recompute or modify data.

**Returns:**
- `pd.DataFrame`: DataFrame from the most recent compute() call

**Example:**
```python
# First compute with min_size=0 to get all combinations
calc.compute(min_size=0)
df = calc.get_dataframe()
print(f"Total rows: {len(df)}")  # Should be 2^n - 1

# Export to CSV
df.to_csv("overlaps.csv", index=False)

# If you call compute() with different parameters, get_dataframe() reflects that
calc.compute(min_size=2)  # Only large overlaps
df_large = calc.get_dataframe()
print(f"Large overlaps only: {len(df_large)} rows")
```

**Notes:**
- Automatically triggers `compute()` with default parameters if no computation done yet
- Returns whatever the last compute() produced (including filters)
- Simple getter - does NOT recompute or ignore previous filters
- Call `compute(min_size=0)` explicitly before get_dataframe() if you need all 2^n - 1 combinations

---

### get_plot_data()

**Get DataFrame formatted for Venn diagram plotting.**

Returns a DataFrame with selected columns suitable for plotting Venn diagrams. For single-set regions (n_sets == 1), shows exclusive elements instead of all elements, which is more appropriate for Venn diagram region labeling.

**Returns:**
- `pd.DataFrame` with columns:
  - `set_names`: string representation (e.g., "A & B & C")
  - `n_sets`: number of sets in combination
  - `size`: size of intersection (or exclusive_size for n_sets == 1)
  - `elements`: list of elements (or exclusive_elements for n_sets == 1)

**Key Feature:**
- For `n_sets == 1` (single set regions): `size` = exclusive_size, `elements` = exclusive_elements
- For `n_sets > 1` (multi-set intersections): `size` and `elements` are the intersection values
- This makes Venn diagrams show region-specific counts correctly

**Example:**
```python
# Compute all overlaps first
calc.compute(min_size=0)

# Get plot-ready data
plot_df = calc.get_plot_data()

# Show first few rows
print(plot_df[['set_names', 'n_sets', 'size', 'elements']].head())

# Filter for specific region types
single_regions = plot_df[plot_df['n_sets'] == 1]
multi_regions = plot_df[plot_df['n_sets'] > 1]

# Export for plotting
plot_df.to_csv("plot_data.csv", index=False)
```

**Notes:**
- Automatically triggers `compute(min_size=0)` if not already done
- This ensures all 2^n - 1 combinations are available for plotting
- Single-set regions show exclusive elements (elements only in that set)
- Multi-set regions show intersection elements (elements in all those sets)

---

### query_elements(query_sets=None)

**Query overlap information for specific or all set combinations.**

Most flexible method for accessing overlap data programmatically.

**Parameters:**
- `query_sets`: list of str, optional
  - List of set names to query
  - If `None` (default): returns **all** possible combinations

**Returns:**
- If `query_sets` provided: Single `dict` with overlap info
- If `query_sets` is `None`: List of `dict` for all combinations

**Dictionary keys:**
- `sets`: tuple of set names
- `set_names`: string representation (e.g., "A & B")
- `n_sets`: number of sets in combination
- `size`: intersection size
- `elements`: sorted list of intersecting elements
- `exclusive_size`: exclusive elements count
- `exclusive_elements`: sorted exclusive elements

**Examples:**

```python
# Query specific combination
result = calc.query_elements(['SetA', 'SetB'])
print(f"Intersection: {result['elements']}")
print(f"Size: {result['size']}")
print(f"Exclusive: {result['exclusive_elements']}")

# Get all combinations (default behavior)
all_results = calc.query_elements()  # No arguments

print(f"Total combinations: {len(all_results)}")
for combo in all_results:
    if combo['size'] > 0:
        print(f"{combo['set_names']}: {combo['elements']}")
```

**Notes:**
- When `query_sets=None`, **includes all combinations** even with empty intersections
- Most flexible method for programmatic access

---

### __repr__()

**String representation of the calculator.**

Returns a formatted string showing the number of sets and their names.

**Example:**
```python
calc = OverlapCalculator({'A': {1,2}, 'B': {2,3}})
print(calc)
# Output: OverlapCalculator(n_sets=2, sets=['A', 'B'])
```

---

## Advanced Usage Examples

### 1. Batch Processing Multiple Datasets

```python
from caculated import OverlapCalculator

# Multiple experiments
experiments = {
    'Exp1_Day1': {'gene1', 'gene2', 'gene3', 'gene4'},
    'Exp1_Day2': {'gene2', 'gene3', 'gene5', 'gene6'},
    'Exp1_Day3': {'gene3', 'gene4', 'gene6', 'gene7'},
    'Exp2_Day1': {'gene1', 'gene3', 'gene8', 'gene9'},
    'Exp2_Day2': {'gene2', 'gene4', 'gene5', 'gene10'},
    'Exp2_Day3': {'gene3', 'gene6', 'gene9', 'gene11'}
}

calc = OverlapCalculator(experiments)

# Filter by experiment (name prefix)
exp1_sets = [s for s in calc.get_summary()['set_names'] if s.startswith('Exp1')]
exp2_sets = [s for s in calc.get_summary()['set_names'] if s.startswith('Exp2')]

# Analyze each experiment separately
for sets in [exp1_sets, exp2_sets]:
    result = calc.query_elements(sets)
    print(f"{sets}: {len(result['elements'])} common genes")
```

### 2. Finding Unique Patterns

```python
# Find elements that appear in exactly k sets
def find_exact_k_overlap(calc, k):
    """Find elements that appear in exactly k sets."""
    df = calc.compute(min_size=0)
    k_combinations = df[df['n_sets'] == k]
    
    # Get all elements from k-set combinations
    elements_in_k_sets = set()
    for _, row in k_combinations.iterrows():
        elements_in_k_sets.update(row['elements'])
    
    return elements_in_k_sets

# Use it
data = {
    'A': {1, 2, 3, 4, 5, 6, 7},
    'B': {1, 2, 3, 8, 9, 10},
    'C': {1, 2, 4, 5, 11, 12},
    'D': {1, 3, 4, 6, 13, 14}
}

calc = OverlapCalculator(data)

# Elements in exactly 2 sets
elements_in_2 = find_exact_k_overlap(calc, 2)
print(f"Elements in exactly 2 sets: {elements_in_2}")

# Elements in exactly 3 sets
elements_in_3 = find_exact_k_overlap(calc, 3)
print(f"Elements in exactly 3 sets: {elements_in_3}")
```

### 3. Progressive Filtering Strategy

```python
# Start with all combinations, progressively filter
calc = OverlapCalculator({'A': {1,2,3,4,5}, 'B': {2,3,4,6,7}, 'C': {3,4,5,7,8}})

# Step 1: Get all combinations
all_df = calc.compute(min_size=0)
print(f"Total combinations: {len(all_df)}")

# Step 2: Filter by complexity
single_sets = all_df[all_df['n_sets'] == 1]
pairwise = all_df[all_df['n_sets'] == 2]
triple = all_df[all_df['n_sets'] == 3]

print(f"Single sets: {len(single_sets)}")
print(f"Pairwise: {len(pairwise)}")
print(f"Triple overlap: {len(triple)}")

# Step 3: Filter by size
large_overlaps = all_df[all_df['size'] >= 3]
print(f"Large overlaps (≥3): {len(large_overlaps)}")

# Step 4: Find most significant
most_significant = all_df.nlargest(5, 'size')
print("\nTop 5 most significant overlaps:")
print(most_significant[['set_names', 'size', 'elements']])
```

### 4. Temporal Analysis

```python
# Analyze how overlaps change over time
time_series_data = {
    'Day1': {1, 2, 3, 4, 5},
    'Day2': {2, 3, 4, 6, 7, 8},
    'Day3': {3, 4, 5, 7, 9, 10},
    'Day4': {4, 5, 6, 10, 11, 12},
    'Day5': {5, 6, 7, 11, 13, 14}
}

calc = OverlapCalculator(time_series_data)
exclusive = calc.compute_exclusive()

# Track unique elements per day
print("Unique elements per day:")
for _, row in exclusive.iterrows():
    print(f"{row['set']}: {row['exclusive_size']} unique elements")

# Find persistent elements (appearing on 3+ days)
persistent_3plus = []
persistent_4plus = []

for i in range(3, 6):  # Check for 3, 4, 5 days
    sets_to_check = [f'Day{j}' for j in range(1, i+1)]
    result = calc.query_elements(sets_to_check)
    if result['size'] > 0:
        print(f"Elements on days 1-{i}: {result['elements']}")
```

### 5. Clustering Sets by Similarity

```python
import pandas as pd

# Cluster sets based on Jaccard similarity
calc = OverlapCalculator({
    'Cluster1_A': {1,2,3,4},
    'Cluster1_B': {2,3,4,5},
    'Cluster2_A': {10,11,12,13},
    'Cluster2_B': {11,12,13,14},
    'Cluster3_A': {20,21,22},
    'Cluster3_B': {21,22,23}
})

matrices = calc.get_pairwise_overlap()
jaccard = matrices['jaccard_matrix']

print("Jaccard Similarity Matrix:")
print(jaccard.round(3))

# Simple clustering: group sets with Jaccard > 0.5
threshold = 0.5
clusters = []
used_sets = set()

for set_name in jaccard.columns:
    if set_name in used_sets:
        continue
    
    similar = jaccard[set_name][jaccard[set_name] > threshold].index.tolist()
    clusters.append(similar)
    used_sets.update(similar)

print(f"\nIdentified clusters: {clusters}")
```

### 6. Export for External Tools

```python
# Export data in multiple formats for different tools
calc = OverlapCalculator({
    'GeneSet1': {'g1', 'g2', 'g3', 'g4'},
    'GeneSet2': {'g2', 'g3', 'g4', 'g5'},
    'GeneSet3': {'g3', 'g4', 'g5', 'g6'}
})

# 1. CSV for Excel/BI tools
df = calc.compute(min_size=0)
df.to_csv("overlaps_complete.csv", index=False)

# 2. JSON for web applications
import json
summary = calc.get_summary()
with open("summary.json", 'w') as f:
    json.dump(summary, f, indent=2, default=str)

# 3. Excel with multiple sheets
with pd.ExcelWriter("overlaps_report.xlsx") as writer:
    df.to_excel(writer, sheet_name='All Overlaps', index=False)
    calc.compute_exclusive().to_excel(writer, sheet_name='Exclusive', index=False)
    matrices = calc.get_pairwise_overlap()
    matrices['overlap_matrix'].to_excel(writer, sheet_name='Overlap Matrix')
    matrices['jaccard_matrix'].to_excel(writer, sheet_name='Jaccard Matrix')

# 4. Plot-ready data for R
plot_data = calc.get_plot_data()
plot_data.to_csv("venn_data.csv", index=False)
```

---

## Usage Examples

### Complete Workflow Example

```python
from caculated import OverlapCalculator

# 1. Prepare data
gene_sets = {
    'Tumor_A': {'TP53', 'KRAS', 'EGFR', 'MYC', 'BRCA1'},
    'Tumor_B': {'TP53', 'KRAS', 'PIK3CA', 'PTEN', 'MYC'},
    'Tumor_C': {'TP53', 'BRAF', 'EGFR', 'MYC', 'ALK'}
}

# 2. Initialize calculator
calc = OverlapCalculator(gene_sets)

# 3. Compute all overlaps including empty (2^n - 1 combinations)
calc.compute(min_size=0)
print("All Overlaps:")
df = calc.get_dataframe()
print(df[['set_names', 'size', 'elements']])

# 4. Get exclusive genes
exclusive = calc.compute_exclusive()
print("\nExclusive Genes per Tumor:")
for _, row in exclusive.iterrows():
    print(f"{row['set']}: {row['exclusive_elements']}")

# 5. Pairwise analysis
matrices = calc.get_pairwise_overlap()
print("\nPairwise Overlaps:")
print(matrices['overlap_matrix'])

# 6. Summary (uses cached results from compute(min_size=0))
summary = calc.get_summary()
print(f"\nTotal combinations (2^n - 1): {summary['n_combinations']}")
print(f"Total unique genes: {summary['total_unique_elements']}")
print(f"Genes common to all tumors: {summary['all_common_size']}")

# 7. Query specific combinations
genes_in_A_B = calc.query_elements(['Tumor_A', 'Tumor_B'])
print(f"\nGenes in A and B: {genes_in_A_B['elements']}")

# 8. Get all combinations
all_combos = calc.query_elements()
print(f"\nTotal combinations examined: {len(all_combos)}")

# 9. Export to CSV
calc.compute(min_size=0)  # Ensure all combinations included
df_all = calc.get_dataframe()
df_all.to_csv("all_overlaps.csv", index=False)
print(f"\nExported {len(df_all)} rows to CSV")
```

### Filtering Results

```python
# Get ALL combinations including empty (2^n - 1 rows)
all_combinations = calc.compute(min_size=0)

# Only large overlaps (≥3 elements)
large_overlaps = calc.compute(min_size=3)

# Only small overlaps (≤2 elements)
small_overlaps = calc.compute(max_size=2)

# Exact size (exactly 3 elements)
exact_overlaps = calc.compute(min_size=3, max_size=3)

# Exclude empty intersections (same as old behavior)
non_empty = calc.compute(min_size=1)
```

### Working with Results

```python
# Export to CSV
df = calc.get_dataframe()
df.to_csv("overlaps.csv", index=False)

# Filter DataFrame
large_overlaps = df[df['size'] >= 3]
triple_overlaps = df[df['n_sets'] == 3]

# Access specific columns
for elements in df['elements']:
    print(elements)
```

---

## Understanding the Output

### Overlap Dictionary Structure

```python
{
    'sets': ('SetA', 'SetB'),           # Tuple of set names
    'set_names': 'SetA & SetB',          # Human-readable name
    'n_sets': 2,                         # Number of sets
    'size': 3,                           # Intersection size
    'elements': [2, 3, 4],               # Intersecting elements (sorted)
    'exclusive_size': 1,                 # Exclusive elements count
    'exclusive_elements': [2]            # Exclusive elements (sorted)
}
```

### Exclusive Elements Dictionary

```python
{
    'set': 'SetA',                       # Set name
    'total_size': 5,                     # Total elements in set
    'exclusive_size': 2,                 # Exclusive to this set
    'exclusive_elements': [1, 5],        # Exclusive elements
    'overlap_size': 3                    # Shared with others
}
```

---

## Performance Considerations

### Complexity Analysis

#### Time Complexity

For `n` sets with average size `k`:

| Operation | Complexity | Description |
|-----------|------------|-------------|
| `compute()` | O(2ⁿ × k) | All combinations × intersection cost |
| `compute_exclusive()` | O(n × k) | n sets × union/difference cost |
| `get_pairwise_overlap()` | O(n² × k) | All pairs × intersection cost |
| `query_elements(specific)` | O(m × k) | m queried sets × intersection cost |
| `query_elements(all)` | O(2ⁿ × k) | Same as `compute()` |
| `get_summary()` | O(1) | Uses cached results |
| `get_dataframe()` | O(1) | Returns cached results |

**Combinations Growth:**
```
n=5:   2⁵ - 1 = 31    combinations   (fast)
n=10:  2¹⁰ - 1 = 1,023 combinations   (acceptable)
n=15:  2¹⁵ - 1 = 32,767 combinations  (slow)
n=20:  2²⁰ - 1 = 1,048,575 combinations (very slow)
```

#### Space Complexity

| Method | Space | Description |
|---------|--------|-------------|
| `compute()` | O(2ⁿ × k) | All combinations stored |
| `compute_exclusive()` | O(n × k) | n sets × elements |
| `get_pairwise_overlap()` | O(n²) | Two n×n matrices |
| Cached results | O(2ⁿ × k) | Stored in instance |

**Memory Usage Examples (k=100 elements/set):**
```
n=5:   31 combos × 100 = 3.1 KB
n=10:  1,023 combos × 100 = 102.3 KB
n=15:  32,767 combos × 100 = 3.28 MB
n=20:  1,048,575 combos × 100 = 104.9 MB
```

### Optimization Tips

1. **Use min_size filtering** for large datasets:
   ```python
   # Only get meaningful overlaps
   df = calc.compute(min_size=2)
   ```

2. **Cache results** for repeated queries:
   ```python
   # Compute once
   summary = calc.get_summary()
   
   # Use cached data multiple times
   for overlap in summary['all_overlaps']:
       process(overlap)
   ```

3. **Query specific combinations** when possible:
   ```python
   # Instead of computing all then filtering
   result = calc.query_elements(['SetA', 'SetB'])
   ```

---

## Best Practices

### 1. Input Data Preparation

#### Use Meaningful Set Names

```python
# ❌ Bad: Generic names
calc = OverlapCalculator([
    {1, 2, 3, 4, 5},
    {2, 3, 4, 6, 7},
    {3, 4, 5, 7, 8}
])

# ✅ Good: Descriptive names
calc = OverlapCalculator({
    'Control_Group': {1, 2, 3, 4, 5},
    'Treatment_A': {2, 3, 4, 6, 7},
    'Treatment_B': {3, 4, 5, 7, 8}
})
```

#### Use Appropriate Data Types

```python
# ❌ Bad: List elements (can contain duplicates)
calc = OverlapCalculator({
    'Set1': [1, 2, 3, 2, 1]  # Duplicates!
})

# ✅ Good: Set elements (unique)
calc = OverlapCalculator({
    'Set1': {1, 2, 3}  # No duplicates
})
```

#### Validate Input Before Processing

```python
def validate_sets(data):
    """Validate input data before creating calculator."""
    if not data:
        raise ValueError("Empty data provided")
    
    for name, elements in data.items():
        if not elements:
            print(f"Warning: Set '{name}' is empty")
        if len(elements) < 2:
            print(f"Warning: Set '{name}' has < 2 elements")

# Use it
data = {'A': {1, 2, 3}, 'B': {2, 3, 4}}
validate_sets(data)
calc = OverlapCalculator(data)
```

### 2. Computation Strategy

#### Choose Right min_size Parameter

```python
# For complete analysis (Venn diagrams, full reporting)
calc.compute(min_size=0)  # All 2^n - 1 combinations

# For meaningful overlaps only
calc.compute(min_size=1)  # Non-empty only

# For significant overlaps
calc.compute(min_size=3)  # At least 3 elements

# For rare patterns
calc.compute(max_size=2)  # Small overlaps only
```

#### Avoid Redundant Computations

```python
# ❌ Bad: Compute multiple times
df1 = calc.compute(min_size=1)
df2 = calc.compute(min_size=2)
df3 = calc.compute(min_size=3)

# ✅ Good: Compute once, filter after
df_all = calc.compute(min_size=0)
df1 = df_all[df_all['size'] >= 1]
df2 = df_all[df_all['size'] >= 2]
df3 = df_all[df_all['size'] >= 3]
```

### 3. Result Processing

#### Use DataFrame Operations

```python
# Compute once
df = calc.compute(min_size=0)

# Efficient filtering with pandas
large_overlaps = df[df['size'] > 5]  # Vectorized
triple_only = df[df['n_sets'] == 3]
specific_sets = df[df['set_names'].str.contains('SetA|SetB')]

# Complex queries
query = (df['size'] >= 3) & (df['n_sets'] >= 2)
filtered = df[query]
```

#### Use Summary for Quick Insights

```python
# Instead of manually computing statistics
# ❌ Manual approach
df = calc.compute(min_size=0)
n_sets = len(df['sets'].unique())
max_overlap = df['size'].max()

# ✅ Use built-in summary
summary = calc.get_summary()
n_sets = summary['n_sets']
max_overlap = summary['max_overlap_size']
total_unique = summary['total_unique_elements']
```

### 4. Error Handling

#### Handle Empty Results Gracefully

```python
def safe_query(calc, set_names):
    """Query sets and handle empty results."""
    try:
        result = calc.query_elements(set_names)
        if result['size'] == 0:
            print(f"Warning: No overlap for {set_names}")
            return None
        return result
    except ValueError as e:
        print(f"Error: {e}")
        return None

# Use it
result = safe_query(calc, ['SetA', 'SetB'])
if result:
    print(f"Overlap: {result['elements']}")
```

#### Validate Set Names

```python
def validate_set_names(calc, requested_names):
    """Ensure all requested sets exist."""
    available = set(calc.get_summary()['set_names'])
    requested = set(requested_names)
    
    missing = requested - available
    if missing:
        raise ValueError(f"Unknown sets: {missing}")

# Use it
try:
    validate_set_names(calc, ['SetA', 'SetB', 'UnknownSet'])
    result = calc.query_elements(['SetA', 'SetB', 'UnknownSet'])
except ValueError as e:
    print(f"Validation failed: {e}")
```

### 5. Memory Management

#### Process Large Datasets in Chunks

```python
# For very large datasets, process in subsets
def process_large_dataset(data, chunk_size=10):
    """Process large dataset in chunks."""
    all_set_names = list(data.keys())
    results = []
    
    for i in range(0, len(all_set_names), chunk_size):
        chunk_names = all_set_names[i:i+chunk_size]
        chunk_data = {k: data[k] for k in chunk_names}
        
        calc = OverlapCalculator(chunk_data)
        df = calc.compute(min_size=1)
        results.append(df)
        
        print(f"Processed chunk {i//chunk_size + 1}: {len(df)} overlaps")
    
    return pd.concat(results, ignore_index=True)

# Use it
large_data = {f'Set{i}': set(range(100*i, 100*i+50)) for i in range(100)}
results = process_large_dataset(large_data)
```

### 6. Code Organization

#### Create Helper Functions

```python
class OverlapAnalyzer:
    """Wrapper around OverlapCalculator with custom methods."""
    
    def __init__(self, data):
        self.calc = OverlapCalculator(data)
        self.df = self.calc.compute(min_size=0)
    
    def get_top_overlaps(self, n=5):
        """Get top n overlaps by size."""
        return self.df.nlargest(n, 'size')
    
    def get_elements_in_k_sets(self, k):
        """Get elements appearing in exactly k sets."""
        k_combos = self.df[self.df['n_sets'] == k]
        elements = set()
        for _, row in k_combos.iterrows():
            elements.update(row['elements'])
        return elements
    
    def export_report(self, filename):
        """Export comprehensive report."""
        with pd.ExcelWriter(filename) as writer:
            self.df.to_excel(writer, sheet_name='Overlaps')
            self.calc.compute_exclusive().to_excel(writer, sheet_name='Exclusive')
            self.calc.get_pairwise_overlap()['jaccard_matrix'].to_excel(
                writer, sheet_name='Jaccard')

# Use it
data = {'A': {1,2,3}, 'B': {2,3,4}, 'C': {3,4,5}}
analyzer = OverlapAnalyzer(data)
print(analyzer.get_top_overlaps(3))
analyzer.export_report("report.xlsx")
```

---

## Visualization Guide

### 1. Venn Diagram Data Preparation

```python
# Get plot-ready data
calc = OverlapCalculator({
    'SetA': {1, 2, 3, 4, 5},
    'SetB': {2, 3, 4, 6, 7},
    'SetC': {3, 4, 5, 7, 8}
})

plot_data = calc.get_plot_data()

# Single-set regions (exclusive elements)
single_sets = plot_data[plot_data['n_sets'] == 1]
print("Single-set regions:")
for _, row in single_sets.iterrows():
    print(f"  {row['set_names']}: {row['size']} elements")

# Multi-set regions (intersections)
multi_sets = plot_data[plot_data['n_sets'] > 1]
print("\nMulti-set regions:")
for _, row in multi_sets.iterrows():
    print(f"  {row['set_names']}: {row['size']} elements")
```

### 2. Using with Matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np

# Simple bar chart of overlap sizes
df = calc.compute(min_size=1)

plt.figure(figsize=(12, 6))
plt.bar(range(len(df)), df['size'])
plt.xlabel('Combination')
plt.ylabel('Overlap Size')
plt.title('Overlap Sizes for All Combinations')
plt.xticks(range(len(df)), df['set_names'], rotation=45, ha='right')
plt.tight_layout()
plt.savefig('overlap_sizes.png', dpi=300)
plt.show()
```

### 3. Using with Seaborn Heatmap

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Jaccard similarity heatmap
matrices = calc.get_pairwise_overlap()
jaccard_df = matrices['jaccard_matrix']

plt.figure(figsize=(10, 8))
sns.heatmap(jaccard_df, annot=True, cmap='YlOrRd', 
            cbar_kws={'label': 'Jaccard Similarity'})
plt.title('Pairwise Jaccard Similarity')
plt.tight_layout()
plt.savefig('jaccard_heatmap.png', dpi=300)
plt.show()

# Overlap count heatmap
overlap_df = matrices['overlap_matrix']
plt.figure(figsize=(10, 8))
sns.heatmap(overlap_df, annot=True, cmap='Blues',
            cbar_kws={'label': 'Overlap Count'})
plt.title('Pairwise Overlap Counts')
plt.tight_layout()
plt.savefig('overlap_heatmap.png', dpi=300)
plt.show()
```

### 4. Network Visualization

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create network from pairwise overlaps
matrices = calc.get_pairwise_overlap()
overlap_matrix = matrices['overlap_matrix']

G = nx.Graph()

# Add nodes
for set_name in overlap_matrix.columns:
    G.add_node(set_name)

# Add edges with weights (overlap size)
for i, set1 in enumerate(overlap_matrix.columns):
    for j, set2 in enumerate(overlap_matrix.columns):
        if i < j:  # Avoid duplicate edges
            weight = overlap_matrix.iloc[i, j]
            if weight > 0:
                G.add_edge(set1, set2, weight=weight)

# Draw network
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, k=2, iterations=50)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=1000, 
                       node_color='lightblue')

# Draw edges with thickness proportional to overlap
for u, v, d in G.edges(data=True):
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                         width=d['weight']/max(d['weight'] for *_, _, d in G.edges(data=True))*3)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10)

plt.title('Set Overlap Network')
plt.axis('off')
plt.tight_layout()
plt.savefig('overlap_network.png', dpi=300)
plt.show()
```

### 5. Export for External Visualization Tools

```python
# Export for R's VennDiagram package
plot_data = calc.get_plot_data()
plot_data.to_csv("venn_data.csv", index=False)

# R code to visualize:
# library(VennDiagram)
# data <- read.csv("venn_data.csv")
# venn.plot(data, size=c(2,2))
```

---

## Common Use Cases

### 1. Bioinformatics - Gene Set Overlap

Analyze overlap between gene sets from different experiments or conditions.

```python
# Gene sets from different cancer types
cancer_genes = {
    'Lung_Cancer': {'TP53', 'KRAS', 'EGFR', ...},
    'Breast_Cancer': {'TP53', 'BRCA1', 'BRCA2', ...},
    'Colon_Cancer': {'APC', 'TP53', 'KRAS', ...}
}

calc = OverlapCalculator(cancer_genes)
summary = calc.get_summary()

# Find genes common to all cancers
common_genes = summary['all_common_size']
print(f"Genes in all cancers: {common_genes}")

# Find cancer-specific genes
exclusive = calc.compute_exclusive()
for _, row in exclusive.iterrows():
    print(f"{row['set']}-specific genes: {row['exclusive_elements']}")
```

### 2. Data Science - Feature Selection

Compare feature sets from different models or feature selection methods.

```python
# Features selected by different algorithms
feature_sets = {
    'RandomForest': {'feat_1', 'feat_3', 'feat_5', ...},
    'Lasso': {'feat_2', 'feat_3', 'feat_6', ...},
    'Correlation': {'feat_1', 'feat_2', 'feat_3', ...}
}

calc = OverlapCalculator(feature_sets)

# Features selected by all methods
matrices = calc.get_pairwise_overlap()
print("Feature agreement matrix:")
print(matrices['overlap_matrix'])
```

### 3. Market Research - Customer Segments

Analyze overlap between customer segments.

```python
# Customer segments
customers = {
    'Premium': {'C001', 'C005', 'C010', ...},
    'Frequent': {'C001', 'C003', 'C005', ...},
    'Recent': {'C002', 'C005', 'C008', ...}
}

calc = OverlapCalculator(customers)

# Find premium, frequent, recent customers (all segments)
triple = calc.query_elements(['Premium', 'Frequent', 'Recent'])
print(f"VIP customers: {triple['elements']}")
```

### 4. Customer Segmentation - Marketing

Identify customer behavior patterns across segments.

```python
# Customer segments
segments = {
    'VIP': {'C001', 'C005', 'C010', 'C015', 'C020'},
    'Frequent_Buyers': {'C001', 'C003', 'C005', 'C008', 'C012'},
    'Recent_Customers': {'C002', 'C005', 'C008', 'C013', 'C018'},
    'High_Spenders': {'C001', 'C004', 'C010', 'C016', 'C022'},
    'Loyalty_Members': {'C001', 'C006', 'C011', 'C016', 'C021'}
}

calc = OverlapCalculator(segments)
matrices = calc.get_pairwise_overlap()

# Find most valuable customers (in multiple segments)
print("Customer Overlap Matrix:")
print(matrices['overlap_matrix'])

# Find VIP segments (customers in 3+ segments)
summary = calc.get_summary()
triple_plus = [combo for combo in summary['all_overlaps'] 
                if combo['n_sets'] >= 3 and combo['size'] > 0]

print(f"\nCustomers in 3+ segments: {len(triple_plus)} combinations")
for combo in triple_plus:
    print(f"  {combo['set_names']}: {combo['elements']}")
```

### 5. Feature Selection - Machine Learning

Identify robust features across different models.

```python
# Features selected by different algorithms
feature_sets = {
    'RandomForest': {'feat_1', 'feat_3', 'feat_5', 'feat_7', 'feat_9'},
    'GradientBoosting': {'feat_2', 'feat_3', 'feat_6', 'feat_8', 'feat_10'},
    'LogisticRegression': {'feat_1', 'feat_2', 'feat_4', 'feat_7', 'feat_11'},
    'NeuralNetwork': {'feat_3', 'feat_4', 'feat_5', 'feat_9', 'feat_12'},
    'SVM': {'feat_2', 'feat_5', 'feat_7', 'feat_10', 'feat_13'}
}

calc = OverlapCalculator(feature_sets)

# Find consensus features (selected by all methods)
all_methods = calc.query_elements(list(feature_sets.keys()))
print(f"Consensus features (all methods): {all_methods['elements']}")

# Find robust features (selected by 3+ methods)
robust_features = []
for i in range(3, 6):
    for combo in calc.query_elements():
        if combo['n_sets'] == i and combo['size'] > 0:
            print(f"Features in {i} methods: {combo['elements']}")

# Find algorithm-specific features
exclusive = calc.compute_exclusive()
print("\nAlgorithm-specific features:")
for _, row in exclusive.iterrows():
    print(f"  {row['set']}: {row['exclusive_elements']}")
```

### 6. Text Analysis - Document Comparison

Compare word/document sets across different sources.

```python
from collections import Counter
import re

def extract_words(text):
    """Extract unique words from text."""
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

# Documents
documents = {
    'Doc1': extract_words("This is the first document about data analysis."),
    'Doc2': extract_words("The second document discusses machine learning."),
    'Doc3': extract_words("Third document covers deep learning and neural networks."),
    'Doc4': extract_words("Fourth document explores statistical methods.")
}

calc = OverlapCalculator(documents)

# Find common vocabulary
all_docs = calc.query_elements(list(documents.keys()))
print(f"Words in all documents: {all_docs['elements']}")

# Find unique vocabulary per document
exclusive = calc.compute_exclusive()
print("\nUnique words per document:")
for _, row in exclusive.iterrows():
    print(f"  {row['set']}: {row['exclusive_elements']}")
```

### 7. Survey Analysis - Multi-response Questions

Analyze survey responses where respondents can select multiple options.

```python
# Survey responses (respondents who selected each option)
survey_responses = {
    'Option_A': {'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8'},
    'Option_B': {'R2', 'R4', 'R6', 'R8', 'R10', 'R12', 'R14'},
    'Option_C': {'R1', 'R3', 'R5', 'R7', 'R9', 'R11', 'R13'},
    'Option_D': {'R2', 'R5', 'R8', 'R11', 'R14', 'R17', 'R20'}
}

calc = OverlapCalculator(survey_responses)

# Find respondents selecting multiple options
df = calc.compute(min_size=2)
print(f"Respondents with 2+ selections: {len(df)} patterns")

# Most common combinations
top_combinations = df.nlargest(5, 'size')
print("\nTop 5 most common selection patterns:")
for _, row in top_combinations.iterrows():
    print(f"  {row['set_names']}: {row['size']} respondents")

# Respondents selecting all options
all_four = calc.query_elements(list(survey_responses.keys()))
print(f"\nSelecting all options: {all_four['size']} respondents")
```

---

## Troubleshooting

### Problem: Empty Results

**Cause:** All intersections are empty or filtered out by min_size

**Solution:**
```python
# Check without filtering
df = calc.compute(min_size=0)  # Note: 0 will still be excluded

# Or get all combinations (including empty)
all_combos = calc.query_elements()
empty_combos = [c for c in all_combos if c['size'] == 0]
print(f"Empty combinations: {len(empty_combos)}")
```

### Problem: Memory Error with Many Sets

**Cause:** Too many combinations (2ⁿ grows exponentially)

**Solution:**
```python
# Use size filtering
small_df = calc.compute(min_size=5)  # Only large overlaps

# Or query specific combinations
result = calc.query_elements(['Set1', 'Set2', 'Set3'])
```

### Problem: Unknown Set Name Error

**Cause:** Querying a set name that doesn't exist

**Solution:**
```python
# Check available set names
summary = calc.get_summary()
print(f"Available sets: {summary['set_names']}")

# Then query with correct names
result = calc.query_elements([summary['set_names'][0], summary['set_names'][1]])
```

---

## FAQ

### General Questions

**Q: What is the maximum number of sets OverlapCalculator can handle?**

A: There's no hard limit, but consider practical constraints:
- n=10: ~1K combinations (fast)
- n=15: ~33K combinations (acceptable)
- n=20: ~1M combinations (slow, memory intensive)
- n>20: Use filtering or query specific combinations

**Q: Why does my DataFrame show fewer rows than expected?**

A: Check your `min_size` parameter:
```python
# Expected 2^n - 1 rows, but getting fewer?
calc.compute(min_size=1)  # Excludes empty intersections!

# Fix:
calc.compute(min_size=0)  # Includes all combinations
```

**Q: Can I update the data after creating a calculator?**

A: No, calculator instances are immutable. Create a new instance:
```python
# Initial data
calc = OverlapCalculator({'A': {1,2}, 'B': {2,3}})

# New data - create new calculator
new_calc = OverlapCalculator({'A': {1,2,3}, 'B': {2,3,4}})
```

**Q: What's the difference between `elements` and `exclusive_elements`?**

A: 
- `elements`: All elements in the intersection
- `exclusive_elements`: Elements only in that specific combination

**Example:**
```
Set A = {1, 2, 3, 4}
Set B = {3, 4, 5, 6}

Intersection A & B:
- elements = [3, 4] (all common elements)
- exclusive_elements = [3, 4] (elements only in A&B, not elsewhere)
```

**Q: How do I get elements common to ALL sets?**

A: Use `get_summary()` or query all sets:
```python
summary = calc.get_summary()
common_size = summary['all_common_size']

# Or query directly:
all_sets = list(calc.get_summary()['set_names'])
result = calc.query_elements(all_sets)
print(f"Common to all: {result['elements']}")
```

### Performance Questions

**Q: Why is my computation slow?**

A: Common causes and solutions:
1. Too many sets: Use `min_size` filtering
2. Large sets: No easy fix, but consider preprocessing
3. Repeated computation: Cache results

```python
# Problem: Computing multiple times
df1 = calc.compute(min_size=1)
df2 = calc.compute(min_size=2)

# Solution: Compute once, filter
df_all = calc.compute(min_size=0)
df1 = df_all[df_all['size'] >= 1]
df2 = df_all[df_all['size'] >= 2]
```

**Q: How can I reduce memory usage?**

A: Use size filtering and avoid storing all results:
```python
# Problem: All combinations in memory
df = calc.compute(min_size=0)  # 2^n - 1 rows

# Solution 1: Filter early
df = calc.compute(min_size=5)  # Only large overlaps

# Solution 2: Process in chunks
for set_combo in [['A','B'], ['A','C'], ['B','C']]:
    result = calc.query_elements(set_combo)
    process(result)
    # result not stored, minimal memory
```

### Output Questions

**Q: Why are results sorted?**

A: For consistency and prioritization:
1. By `n_sets` descending (complex overlaps first)
2. By `size` descending (large overlaps first)

To disable sorting:
```python
df = calc.compute(min_size=0)
df_sorted = df  # Already sorted
df_unsorted = df.sort_index()  # Original order
```

**Q: How do I get results in a different format?**

A: Convert from DataFrame:
```python
df = calc.compute(min_size=0)

# To dictionary list
result_list = df.to_dict('records')

# To JSON
import json
json_str = df.to_json(orient='records')

# To list of elements
elements_list = df['elements'].tolist()

# To numpy array
import numpy as np
elements_array = np.array(df['elements'].tolist())
```

### Integration Questions

**Q: Can I use OverlapCalculator with pandas DataFrames?**

A: Yes, convert DataFrame to sets:
```python
# From DataFrame
df = pd.DataFrame({
    'gene': ['g1', 'g2', 'g3', 'g4', 'g5'],
    'expression_A': [1, 1, 0, 1, 1],
    'expression_B': [0, 1, 1, 1, 0]
})

# Extract expressed genes
set_A = set(df[df['expression_A'] > 0]['gene'])
set_B = set(df[df['expression_B'] > 0]['gene'])

# Create calculator
calc = OverlapCalculator({'A': set_A, 'B': set_B})
```

**Q: Can I integrate with scikit-learn?**

A: Yes, for feature selection:
```python
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

# Get features from different selectors
selector1 = SelectKBest(f_classif, k=10)
selector2 = SelectKBest(f_classif, k=10)

# Assume X is your feature matrix
features1 = set(selector1.fit(X, y).get_support(indices=True))
features2 = set(selector2.fit(X, y).get_support(indices=True))

# Analyze overlap
calc = OverlapCalculator({
    'Selector1': features1,
    'Selector2': features2
})
consensus = calc.query_elements(['Selector1', 'Selector2'])
print(f"Consensus features: {consensus['elements']}")
```

---

## Method Reference Table

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `data` | `OverlapCalculator` | Initialize with sets |
| `compute` | `min_size`, `max_size` | `pd.DataFrame` | All overlaps as DataFrame |
| `compute_exclusive` | - | `pd.DataFrame` | Exclusive elements per set |
| `get_pairwise_overlap` | - | `dict` | Overlap & Jaccard matrices |
| `get_summary` | - | `dict` | Complete statistics |
| `get_dataframe` | - | `pd.DataFrame` | Get/ensure computation |
| `query_elements` | `query_sets` | `dict` or `list` | Query specific or all combos |
| `__repr__` | - | `str` | String representation |

---

## Comparison with Alternatives

### OverlapCalculator vs. Manual Implementation

| Aspect | OverlapCalculator | Manual Implementation |
|---------|-------------------|---------------------|
| Development time | Minutes | Hours/Days |
| Bug risk | Low (well-tested) | High |
| Features | Comprehensive | Limited |
| Performance | Optimized | Variable |
| Maintenance | Minimal | High |
| Documentation | Extensive | None |
| **Winner** | **✅** | |

### OverlapCalculator vs. Specialized Libraries

| Library | OverlapCalculator | SciPy | R-Venn |
|----------|-------------------|---------|---------|
| Python | ✅ Native | ✅ Native | ❌ Requires R |
| Multiple sets | ✅ Any number | ⚠️ Limited | ⚠️ Limited |
| Output format | ✅ DataFrame | ❌ Arrays | ❌ Mixed |
| Statistics | ✅ Comprehensive | ❌ Basic | ❌ Basic |
| Plotting | ⚠️ Data prep only | ❌ None | ✅ Built-in |
| **Winner** | **✅ General-purpose** | ✅ Numerical | ✅ Visualization |

### When to Use Each

**Use OverlapCalculator when:**
- Working in Python ecosystem
- Need flexible set operations
- Want detailed statistics
- Processing multiple datasets
- Building custom analysis pipelines

**Use SciPy when:**
- Doing numerical analysis
- Need matrix operations
- Working with large arrays
- Integration with numpy ecosystem

**Use R-Venn when:**
- Quick Venn diagram visualization
- Working in R ecosystem
- Need publication-ready plots
- Simple 2-3 set analysis

---

## API Design Philosophy

### 1. Lazy Computation

Calculations are performed **only when needed**:

```python
# No computation yet
calc = OverlapCalculator({'A': {1,2}, 'B': {2,3}})

# First access triggers computation
df = calc.compute()  # Computation happens here

# Subsequent accesses use cache
df2 = calc.get_dataframe()  # No recomputation
```

**Benefits:**
- Fast initialization
- Avoid unnecessary work
- Memory efficient
- Predictable performance

### 2. Immutable Design

Input data cannot be modified after creation:

```python
# Cannot do this:
calc.sets_list[0].add(99)  # Bad practice!

# Create new instance instead:
new_data = {'A': {1,2,99}, 'B': {2,3}}
new_calc = OverlapCalculator(new_data)
```

**Benefits:**
- Thread-safe
- Predictable behavior
- Easy to reason about
- Prevents accidental modification

### 3. Caching Strategy

Results are cached to avoid recomputation:

```python
# Computation #1
df1 = calc.compute(min_size=1)  # Computed and cached

# Computation #2 (same parameters)
df2 = calc.compute(min_size=1)  # Returns cached results

# Computation #3 (different parameters)
df3 = calc.compute(min_size=2)  # Recomputes, new cache
```

**What's Cached:**
- `_results_df`: Results from `compute()`
- `_exclusive_results`: Results from `compute_exclusive()`

**Cache Invalidation:**
- Always occurs when parameters change
- Never occurs spontaneously
- Predictable behavior

### 4. Flexible Input

Multiple formats accepted for convenience:

```python
# Dictionary (recommended)
calc = OverlapCalculator({'A': {1,2}, 'B': {2,3}})

# List of sets (auto-named)
calc = OverlapCalculator([{1,2}, {2,3}])  # Named Set1, Set2

# List of tuples (explicit names)
calc = OverlapCalculator([('A', {1,2}), ('B', {2,3})])
```

**Benefits:**
- Works with existing data structures
- Minimal code changes
- Clear intent with dict
- Flexible for all use cases

---

## Testing and Validation

### Unit Test Examples

```python
import unittest

class TestOverlapCalculator(unittest.TestCase):
    def setUp(self):
        self.data = {
            'A': {1, 2, 3, 4},
            'B': {2, 3, 4, 5},
            'C': {3, 4, 5, 6}
        }
        self.calc = OverlapCalculator(self.data)
    
    def test_initialization(self):
        """Test calculator initialization."""
        self.assertEqual(self.calc.get_summary()['n_sets'], 3)
        self.assertIn('A', self.calc.get_summary()['set_names'])
    
    def test_total_combinations(self):
        """Test correct number of combinations."""
        df = self.calc.compute(min_size=0)
        self.assertEqual(len(df), 2**3 - 1)  # 7
    
    def test_pairwise_symmetry(self):
        """Test that pairwise matrix is symmetric."""
        matrices = self.calc.get_pairwise_overlap()
        overlap = matrices['overlap_matrix']
        self.assertTrue((overlap == overlap.T).all().all())
    
    def test_jaccard_range(self):
        """Test Jaccard values are in [0, 1]."""
        matrices = self.calc.get_pairwise_overlap()
        jaccard = matrices['jaccard_matrix']
        self.assertTrue((jaccard >= 0).all().all())
        self.assertTrue((jaccard <= 1).all().all())
    
    def test_exclusive_calculation(self):
        """Test exclusive elements are correct."""
        exclusive = self.calc.compute_exclusive()
        # A = {1,2,3,4}, others = {2,3,4,5,6}
        # A exclusive = {1}
        a_exclusive = exclusive[exclusive['set'] == 'A']['exclusive_elements'].iloc[0]
        self.assertEqual(a_exclusive, [1])
    
    def test_query_validation(self):
        """Test that invalid queries raise errors."""
        with self.assertRaises(ValueError):
            self.calc.query_elements(['InvalidSet'])

if __name__ == '__main__':
    unittest.main()
```

### Integration Test Examples

```python
def test_full_pipeline():
    """Test complete analysis pipeline."""
    # Setup
    data = {
        'GeneSet1': {'g1', 'g2', 'g3'},
        'GeneSet2': {'g2', 'g3', 'g4'},
        'GeneSet3': {'g3', 'g4', 'g5'}
    }
    calc = OverlapCalculator(data)
    
    # Test computation
    df = calc.compute(min_size=0)
    assert len(df) == 7  # 2^3 - 1
    
    # Test summary
    summary = calc.get_summary()
    assert summary['n_sets'] == 3
    assert summary['total_unique_elements'] == 5
    
    # Test export
    import io
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    assert len(buffer.getvalue()) > 0
    
    print("✅ All pipeline tests passed!")

# Run test
test_full_pipeline()
```

---

## Contributing

### Code Style Guidelines

Follow PEP 8 for Python code:
```python
# ✅ Good
def compute_overlap(data):
    result = {}
    for key in data:
        result[key] = len(data[key])
    return result

# ❌ Bad
def computeOverlap(data):  # CamelCase
    result={}
    for key in data:  # No spacing
        result[key]=len(data[key])  # No spacing
    return result
```

### Adding New Features

When extending OverlapCalculator:

1. **Maintain backward compatibility**
```python
# ✅ Good - optional parameter with default
def compute(self, min_size=0, max_size=None, new_param=None):
    # Implementation

# ❌ Bad - required parameter
def compute(self, min_size=0, max_size=None, new_required_param):
    # Breaks existing code
```

2. **Document thoroughly**
```python
def new_method(self, param1, param2):
    """
    Brief description.
    
    Detailed explanation of what the method does.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
        
    Returns
    -------
    type
        Description of return value
        
    Examples
    --------
    >>> calc.new_method('value', 123)
    {'result': ...}
    """
    pass
```

3. **Add tests**
```python
def test_new_method(self):
    """Test new method."""
    calc = OverlapCalculator({'A': {1,2}, 'B': {2,3}})
    result = calc.new_method('test', 123)
    self.assertEqual(result['expected'], 'value')
```

---

## Version History

### v1.0 (Current)
- ✅ Initial release
- ✅ All core functionality implemented
- ✅ Support for multiple input formats (dict, list, tuples)
- ✅ Comprehensive analysis methods
- ✅ Dictionary and DataFrame outputs
- ✅ Result caching for performance
- ✅ Size filtering (min_size, max_size)
- ✅ Pairwise overlap and Jaccard similarity matrices
- ✅ Exclusive elements calculation
- ✅ Flexible querying (specific or all combinations)
- ✅ Summary statistics
- ✅ Plot-ready data for Venn diagrams
- ✅ Extensive documentation and examples

### Planned Features (Future Versions)
- 🔄 Parallel computation for large datasets
- 🔄 Streaming mode for memory-efficient processing
- 🔄 Additional similarity metrics (Cosine, Dice, etc.)
- 🔄 Integration with popular visualization libraries
- 🔄 Statistical testing for overlap significance
- 🔄 Time-series analysis methods
- 🔄 Weighted sets support

---

## Acknowledgments

OverlapCalculator was developed to address the need for:
- Flexible set overlap analysis in Python
- Comprehensive statistics beyond basic intersection counting
- Integration with pandas/DataFrame workflows
- Clear, well-documented API
- Performance optimization for practical use cases

**Inspired by:**
- Set theory fundamentals
- Bioinformatics gene set analysis workflows
- Data science feature selection practices
- Market research customer segmentation techniques

**Used in:**
- Genomic research (gene expression analysis)
- Machine learning (feature selection comparison)
- Customer analytics (segmentation overlap)
- Text mining (document similarity)
- Survey analysis (multi-response questions)

---

## Glossary

| Term | Definition | Example |
|-------|-------------|-----------|
| **Set** | Collection of unique elements | {1, 2, 3, 4} |
| **Intersection** | Elements common to multiple sets | A ∩ B = {3, 4} |
| **Union** | All elements across sets | A ∪ B = {1, 2, 3, 4, 5, 6} |
| **Exclusive Elements** | Elements in only one set | A - (B ∪ C) |
| **Jaccard** | Similarity coefficient (0.0-1.0) | \|A ∩ B\| / \|A ∪ B\| |
| **Power Set** | All possible subsets | For n sets: 2^n subsets |
| **Combination** | Specific subset of sets | {A, B, C} is one combination |
| **DataFrame** | Pandas tabular data structure | Used for results and output |
| **Cached** | Stored for reuse | Avoids recomputation |

---

## Additional Resources

### Set Theory References

- [Wikipedia: Set Theory](https://en.wikipedia.org/wiki/Set_theory)
- [Wikipedia: Intersection](https://en.wikipedia.org/wiki/Intersection_(set_theory))
- [Wikipedia: Union](https://en.wikipedia.org/wiki/Union_(set_theory))

### Similarity Metrics

- [Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index)
- [Dice Coefficient](https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

### Python Libraries

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Python itertools](https://docs.python.org/3/library/itertools.html)

### Visualization

- [Matplotlib Gallery](https://matplotlib.org/gallery/)
- [Seaborn Gallery](https://seaborn.pydata.org/examples/)
- [NetworkX Gallery](https://networkx.org/documentation/stable/auto_examples/index.html)
- [R VennDiagram Package](https://cran.r-project.org/web/packages/VennDiagram/index.html)

### Related Tools

- [SciPy](https://scipy.org/) - Scientific computing
- [scikit-learn](https://scikit-learn.org/) - Machine learning
- [BioPython](https://biopython.org/) - Bioinformatics
- [R VennDiagram](https://cran.r-project.org/web/packages/VennDiagram/index.html) - Venn plots

---

## Quick Reference Card

### Essential Methods

```python
# Initialize
calc = OverlapCalculator({'A': {1,2}, 'B': {2,3}})

# Compute overlaps
df = calc.compute(min_size=0)

# Get summary
summary = calc.get_summary()

# Query specific sets
result = calc.query_elements(['A', 'B'])

# Export
df.to_csv("output.csv", index=False)
```

### Common Filters

```python
# All combinations
calc.compute(min_size=0)

# Non-empty only
calc.compute(min_size=1)

# Large overlaps
calc.compute(min_size=5)

# Small overlaps
calc.compute(max_size=3)

# Exact size
calc.compute(min_size=3, max_size=3)
```

### Key Parameters

| Parameter | Values | Effect |
|-----------|---------|---------|
| `min_size` | 0 | Include empty intersections |
| `min_size` | 1 | Exclude empty intersections |
| `min_size` | 5+ | Only significant overlaps |
| `max_size` | 3 | Small overlaps only |

### Performance Tips

1. Use `min_size` for large datasets
2. Cache results, avoid recomputation
3. Query specific sets when possible
4. Filter after computation, not before
5. Process large datasets in chunks

---

## Contact and Support

### Getting Help

1. **Documentation**: Read this guide thoroughly
2. **Code Examples**: Try provided examples
3. **Troubleshooting**: Check common issues
4. **FAQ**: Review frequently asked questions
5. **Code Docstrings**: Use `help(OverlapCalculator)`

### Reporting Issues

When reporting issues, include:

```python
# System information
import sys
import pandas as pd

print(f"Python version: {sys.version}")
print(f"Pandas version: {pd.__version__}")

# Example code that fails
data = {'A': {1,2}, 'B': {2,3}}
calc = OverlapCalculator(data)
df = calc.compute()  # What's the error?

# Error message
# Paste the full error traceback
```

### Feature Requests

To suggest new features:
1. Describe the use case
2. Explain why current methods aren't sufficient
3. Propose a solution
4. Provide examples if possible

---

**End of Documentation**

*Last Updated: 2025*
*Version: 1.0*
*Author: Dot4diw*

---

Thank you for using OverlapCalculator! We hope this comprehensive documentation helps you make the most of set overlap analysis in your projects.

## License

This code is provided as-is for educational and research purposes.

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the usage examples
3. Examine the docstrings in the code
4. Test with the provided example data

---

**End of Documentation**

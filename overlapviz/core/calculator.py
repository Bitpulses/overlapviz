"""
OverlapCalculator - Set Overlap Analysis Tool
@Using the GLM-4.7 large language model to add detailed code comments.

This module provides a comprehensive class for analyzing overlaps between
multiple sets. It supports various input formats and provides detailed
statistics about set intersections, exclusive elements, and pairwise relationships.

The core functionality includes:
- Computing all possible set combinations (2^n - 1 combinations)
- Calculating intersection sizes and elements for each combination
- Identifying exclusive elements for each set
- Generating pairwise overlap and Jaccard similarity matrices
- Flexible querying of specific combinations or all combinations
- Exporting results in DataFrame and dictionary formats

Author: Dot4diw
Version: 1.0
"""

# =============================================================================
# Import Statements
# =============================================================================
# This section imports all necessary modules and functions for the OverlapCalculator
# class to function properly. Each import serves a specific purpose.

# -------------------------------------------------------------------------
# pandas: Data manipulation and analysis
# -------------------------------------------------------------------------
# Purpose: Provides DataFrame and Series data structures for structured data storage
#
# Why pandas?
# - DataFrames provide tabular structure perfect for overlap results
# - Built-in methods for sorting, filtering, aggregating, and exporting
# - Seamless integration with data analysis and visualization tools
# - Efficient handling of large datasets
#
# Key pandas features used:
# - pd.DataFrame(): Create tabular data structures
# - .sort_values(): Sort results by specific columns
# - .to_csv(): Export results to CSV files
# - .to_dict(): Convert to dictionary format
# - .iloc[]: Position-based indexing for matrix operations
# - .reset_index(): Clean up DataFrame indices after sorting
#
# Example usage in this module:
# - Storing overlap results in self._results_df
# - Creating pairwise matrices with set names as indices
# - Exporting results to CSV for external analysis
# -------------------------------------------------------------------------
import pandas as pd  # For DataFrame operations and result storage

# -------------------------------------------------------------------------
# typing: Type hints for better code clarity and IDE support
# -------------------------------------------------------------------------
# Purpose: Provides standard type hints for Python type annotations
#
# Why typing?
# - Improves code readability by documenting expected types
# - Enables IDE autocompletion and type checking
# - Helps catch type-related bugs early
# - Makes the codebase more maintainable
#
# Type hints used:
# - List: For sequences of items (e.g., List[str], List[Set])
# - Set: Python set type for unordered collections
# - Dict: Dictionary type for key-value mappings
# - Tuple: Immutable sequences (e.g., Tuple[str, ...])
# - Any: Wildcard type for any value
# - Optional: For values that can be None (Optional[X] = Union[X, None])
# - Union: For values that can be one of several types
#
# Example usage in this module:
# - Union[Dict, List, List[Tuple]]: Multiple input format support
# - Optional[pd.DataFrame]: Cached results that may be None
# - List[Dict[str, Any]]: Return type for query_elements()
# -------------------------------------------------------------------------
from typing import List, Set, Dict, Tuple, Any, Optional, Union

# -------------------------------------------------------------------------
# itertools: Combinatorial algorithms
# -------------------------------------------------------------------------
# Purpose: Provides efficient implementations of iterator-based algorithms
#
# Why itertools.combinations?
# - Generates all possible combinations efficiently
# - Uses lazy evaluation (generates one combination at a time)
# - More memory-efficient than generating all combinations at once
# - Well-tested and optimized Python built-in
#
# combinations(iterable, r):
# - Generate all r-length subsequences of elements from the input iterable
# - Returns iterator of tuples
# - Order doesn't matter: (A, B) and (B, A) are the same combination
# - Number of combinations: C(n, r) = n! / (r! * (n-r)!)
#
# Example usage in this module:
# - combinations(range(n), r): Generate all r-set combinations from n sets
# - Used in compute() to iterate over all 2^n - 1 possible subsets
#
# Algorithm example:
# combinations([A, B, C], 2) → (A,B), (A,C), (B,C)
# combinations([A, B, C], 3) → (A,B,C)
# Total: 4 combinations = 2^3 - 1 (for r=1,2,3)
# -------------------------------------------------------------------------
from itertools import combinations  # For generating all possible set combinations


class OverlapCalculator:
    """
    Calculate all overlap situations for n sets
    
    This class provides comprehensive analysis of set overlaps, including:
    - All possible intersection combinations (2^n - 1 total)
    - Exclusive elements for each set (elements only in that set)
    - Pairwise overlap matrices with Jaccard similarity
    - Summary statistics and flexible querying
    - Results in both DataFrame and dictionary formats
    
    The calculator supports three input formats:
    1. Dictionary: {'Set1': {"g1","g2","g3"}, 'Set2': {"g2","g3","g4"}}
    2. List of sets: [{"g1","g2","g3"}, {"g2","g3","g4"}]
    3. List of tuples: [('Set1', {"g1","g2","g3"}), ('Set2', {"g2","g3","g4"})]
    
    Key mathematical principle:
    - For n sets, there are 2^n - 1 non-empty subsets/combinations
    - Each combination represents a unique intersection region
    - Empty intersections (size=0) are included when min_size=0
    
    Class Design:
    - Uses internal caching (_results_df, _exclusive_results) for efficiency
    - Lazy computation: compute() called only when needed
    - Immutable input: parsing creates internal copies of input data
    - Thread-safe: no shared mutable state between instances
    
    Performance Considerations:
    - Time complexity: O(2^n) for compute() due to all possible combinations
    - Space complexity: O(2^n * k) where k is average set size
    - For large n (>15), consider using min_size>0 to filter early
    - Pairwise operations are O(n^2) and scale well
    
    Typical Workflow:
    1. Initialize with data: calc = OverlapCalculator(data)
    2. Compute overlaps: df = calc.compute(min_size=0)
    3. Query results: summary = calc.get_summary()
    4. Export: df.to_csv("results.csv", index=False)
    """
    
    # -------------------------------------------------------------------------
    # Class-level Constants
    # -------------------------------------------------------------------------
    # These constants provide configuration options for the class
    # They are shared across all instances of OverlapCalculator
    #
    # Design pattern:
    # - Uppercase naming convention indicates constants (PEP 8)
    # - Defined at class level (not instance level) for shared configuration
    # - Can be overridden at instance level if needed
    # - Used for default parameter values in methods
    #
    # Current constants:
    # - DEFAULT_MIN_SIZE: Default minimum overlap size for filtering
    #
    # Future extension possibilities:
    # - DEFAULT_MAX_SIZE: Default maximum overlap size
    # - CACHE_ENABLED: Toggle result caching on/off
    # - SORT_ORDER: Default sorting for results
    # -------------------------------------------------------------------------
    
    # -------------------------------------------------------------------------
    # DEFAULT_MIN_SIZE: Default minimum overlap size for filtering
    # -------------------------------------------------------------------------
    # Purpose: Provides a sensible default for min_size parameter in compute()
    #
    # Value: 1
    # - Excludes empty intersections (size=0)
    # - Focuses on actual overlaps with at least one shared element
    #
    # Important note:
    # - This constant is NOT used by default in compute()
    # - compute() uses min_size=0 by default to include empty intersections
    # - This constant is available as a user-configurable option
    #
    # Use cases:
    # - User wants to skip empty intersections without specifying min_size=1
    # - Consistent behavior across multiple compute() calls
    # - Standardizing analysis workflow
    #
    # Example usage:
    # class CustomOverlapCalculator(OverlapCalculator):
    #     def compute_with_filtering(self):
    #         return self.compute(min_size=self.DEFAULT_MIN_SIZE)
    # -------------------------------------------------------------------------
    DEFAULT_MIN_SIZE = 1  # Default minimum overlap size for filtering
                          # Note: This is NOT used by default in compute()
                          # compute() uses min_size=0 by default to include empty intersections
    
    # -------------------------------------------------------------------------
    # __init__: Instance constructor
    # -------------------------------------------------------------------------
    # Purpose: Initialize a new OverlapCalculator instance with input data
    #
    # This is the entry point for creating a calculator object. It performs
    # all necessary setup to make the calculator ready for computations.
    #
    # Design philosophy:
    # - Fail-fast: Validate data immediately during construction
    # - Immutable input: Parse and store data in internal format
    # - Lazy computation: Don't compute until requested
    # - Clear API: Accept multiple input formats for flexibility
    #
    # Instance lifecycle:
    # 1. __init__ called with input data
    # 2. Internal variables initialized (sets_names, sets_list, caches)
    # 3. Input data parsed and validated
    # 4. Instance ready for method calls
    # 5. Methods use cached results when available
    # -------------------------------------------------------------------------
    def __init__(self, data: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]):
        """
        Initialize the OverlapCalculator with input data
        
        This constructor performs the following steps:
        1. Initialize all instance variables to default states
        2. Parse the input data into standardized internal format
        3. Validate the parsed data for consistency and correctness
        4. Store the data in immutable form for future computations
        
        The internal data structures after initialization:
        - self.sets_names: List of set identifiers (strings)
        - self.sets_list: List of Python set objects (hashable collections)
        - self._results_df: None (will be populated by compute())
        - self._exclusive_results: None (will be populated by compute_exclusive())
        
        Parameters
        ----------
        data : dict, list, or list of tuples
            Input set data in one of the supported formats:
            - Dictionary mapping set names to sets (recommended for clarity)
            - List of sets (auto-named as Set1, Set2, Set3, etc.)
            - List of tuples: (set_name, set_elements) for explicit naming
            
        Raises
        ------
        ValueError
            If input data is empty or validation fails (e.g., duplicate names)
        TypeError
            If input data format is not supported
            
        Examples
        --------
        >>> # Dictionary format (recommended - most explicit)
        >>> calc = OverlapCalculator({'Set1': {1,2,3}, 'Set2': {2,3,4}})
        >>> 
        >>> # List of sets (auto-generated names)
        >>> calc = OverlapCalculator([{1,2,3}, {2,3,4}])
        >>> # Sets will be named: Set1, Set2
        >>> 
        >>> # List of tuples (explicit naming without dict)
        >>> calc = OverlapCalculator([('Set1', {1,2,3}), ('Set2', {2,3,4})])
        >>> 
        >>> # After initialization, calculator is ready for computations
        >>> df = calc.compute()  # No re-parsing needed
        """
        # -------------------------------------------------------------------------
        # Initialize instance variables
        # -------------------------------------------------------------------------
        # These variables maintain the calculator's state throughout its lifecycle:
        #
        # self.sets_names: 
        #   - List of string identifiers for each set
        #   - Used for display, querying, and DataFrame indexing
        #   - Example: ['Set1', 'Set2', 'Set3', 'Set4']
        #
        # self.sets_list:
        #   - List of Python set objects containing the actual elements
        #   - Used for all set operations (intersection, union, difference)
        #   - Example: [{1,2,3,4,5}, {2,3,4,6,7}, {3,4,5,7,8}, {4,5,6,8,9}]
        #
        # self._results_df:
        #   - Cached DataFrame containing overlap computation results
        #   - Populated by compute() method, None until first computation
        #   - Cached to avoid redundant recomputation
        #
        # self._exclusive_results:
        #   - Cached DataFrame containing exclusive element results
        #   - Populated by compute_exclusive() method, None until computed
        #   - Cached to avoid redundant computation
        # -------------------------------------------------------------------------
        self.sets_names: List[str] = []  # List of set names for reference
        self.sets_list: List[Set] = []   # List of actual set objects (Python sets)
        self._results_df: Optional[pd.DataFrame] = None  # Cache for computed overlaps
        self._exclusive_results: Optional[pd.DataFrame] = None  # Cache for exclusive elements
        
        # -------------------------------------------------------------------------
        # Parse and validate input data
        # -------------------------------------------------------------------------
        # These methods transform the input into the standardized internal format
        # and ensure data integrity before any computations are performed
        #
        # _parse_input():
        #   - Converts any supported input format to (sets_names, sets_list)
        #   - Ensures all elements are Python sets (hashable, efficient operations)
        #   - Handles dictionary, list, and tuple list inputs uniformly
        #
        # _validate_data():
        #   - Ensures names and sets have matching counts
        #   - Verifies at least one set is provided
        #   - Checks for duplicate set names (would cause ambiguity)
        #
        # If either method raises an exception, object initialization fails
        # and the instance is not created (Python's behavior on __init__ errors)
        # -------------------------------------------------------------------------
        self._parse_input(data)  # Convert input to standardized format
        self._validate_data()    # Ensure data integrity
    
    def _parse_input(self, data: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]) -> None:
        """
        Parse input data from various supported formats into standardized internal representation
        
        This method handles three input formats and converts them to:
        - self.sets_names: List of set names (strings)
        - self.sets_list: List of set objects (Python sets)
        
        The conversion ensures consistent internal representation regardless of input format.
        All set elements are converted to Python sets for reliable set operations.
        
        Parameters
        ----------
        data : Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]
            Input data in one of the supported formats:
            - Dictionary: {name: elements, ...}
            - List of tuples: [(name, elements), ...]
            - List of sets: [elements1, elements2, ...]
            
        Raises
        ------
        ValueError
            If input list is empty
        TypeError
            If input format is not supported
        """
        # Handle dictionary input: {name: set, ...}
        # This is the most explicit format with user-defined names
        if isinstance(data, dict):
            self.sets_names = list(data.keys())      # Extract set names from keys
            self.sets_list = [set(v) for v in data.values()]  # Convert values to sets
            
        # Handle list input
        elif isinstance(data, list):
            # Validate non-empty list
            if len(data) == 0:
                raise ValueError("Input data cannot be empty")
            
            # Check if it's a list of (name, set) tuples
            # Format: [('Set1', {1,2,3}), ('Set2', {2,3,4})]
            if isinstance(data[0], tuple) and len(data[0]) == 2:
                # Extract names and sets from tuples
                self.sets_names = [item[0] for item in data]
                self.sets_list = [set(item[1]) for item in data]
            else:
                # Regular list of sets - auto-generate names
                # Format: [{1,2,3}, {2,3,4}]
                self.sets_names = [f"Set{i+1}" for i in range(len(data))]
                self.sets_list = [set(s) for s in data]
        else:
            # Unsupported data format - raise clear error
            raise TypeError(f"Unsupported input type: {type(data)}. "
                          f"Expected dict, list of sets, or list of tuples.")
    
    def _validate_data(self) -> None:
        """
        Validate the parsed data to ensure it meets requirements
        
        Performs the following checks:
        1. Number of names matches number of sets (consistency check)
        2. At least one set is provided (non-empty requirement)
        3. All set names are unique (identification requirement)
        
        These checks ensure the data is in a valid state for computation.
        
        Raises
        ------
        ValueError
            If any validation check fails
        """
        # Check 1: Names and sets count must match
        # This ensures our internal data structures are consistent
        if len(self.sets_list) != len(self.sets_names):
            raise ValueError("Number of set names and sets do not match")
        
        # Check 2: Must have at least one set
        # Cannot perform overlap analysis with no sets
        if len(self.sets_list) == 0:
            raise ValueError("At least one set must be provided")
        
        # Check 3: All set names must be unique
        # Duplicate names would make querying and identification ambiguous
        if len(self.sets_names) != len(set(self.sets_names)):
            raise ValueError("Set names must be unique - duplicates found")
    
    def compute(self, min_size: int = 0, max_size: Optional[int] = None) -> pd.DataFrame:
        """
        Compute all overlaps between sets and return as DataFrame
        
        This is the core method that calculates all possible intersections between
        sets. It generates all 2^n - 1 non-empty combinations of sets, computes their
        intersections, and filters based on size criteria.
        
        The results are cached in self._results_df to avoid recomputation.
        
        Mathematical Foundation:
        - For n sets, there are exactly 2^n - 1 non-empty subsets/combinations
        - Each combination represents a unique intersection region in a Venn diagram
        - Empty intersections (size=0) are valid combinations and included when min_size=0
        
        Parameters
        ----------
        min_size : int, default 0
            Minimum overlap size threshold. Only returns combinations with 
            intersection size >= min_size. Set to 0 to include empty intersections.
            Set to 1 to exclude empty intersections.
        max_size : int, optional
            Maximum overlap size threshold. Only returns combinations with 
            intersection size <= max_size
            
        Returns
        -------
        pd.DataFrame
            DataFrame with columns:
            - sets: tuple of set names (for identification)
            - set_names: string representation (e.g., "Set1 & Set2 & Set3")
            - n_sets: number of sets in this combination
            - size: size of intersection (0 for empty intersections)
            - elements: sorted list of intersecting elements ([] for empty)
            - exclusive_size: elements only in this combination (not in any other sets)
            - exclusive_elements: sorted list of exclusive elements
            
        Examples
        --------
        >>> calc = OverlapCalculator({'Set1': {1,2,3}, 'Set2': {2,3,4}})
        >>> 
        >>> # Get all combinations (including empty) - 2^n - 1 total
        >>> df = calc.compute(min_size=0)
        >>> print(f"Total combinations: {len(df)}")  # Should be 2^n - 1
        >>> 
        >>> # Get only non-empty overlaps
        >>> df = calc.compute(min_size=1)
        >>> print(df[['set_names', 'size', 'elements']])
        
        Notes
        -----
        - Results are cached in self._results_df to avoid redundant computation
        - With min_size=0, returns all 2^n - 1 possible combinations
        - With min_size=1, excludes empty intersections
        - Empty intersections have size=0 and elements=[]
        - Results are sorted by n_sets (descending) then size (descending)
        - This ordering prioritizes complex overlaps (many sets) and large intersections
        """
        # -------------------------------------------------------------------------
        # Algorithm Implementation: Generate All Possible Set Combinations
        # -------------------------------------------------------------------------
        # This section implements the core combinatorial algorithm that generates
        # all 2^n - 1 possible non-empty subsets of the n input sets.
        #
        # Mathematical Background:
        # - For n sets, the power set contains 2^n subsets
        # - Excluding the empty set, we have 2^n - 1 non-empty subsets
        # - Each subset corresponds to a unique intersection region in a Venn diagram
        #
        # Algorithm Strategy:
        # Instead of generating the power set directly, we iterate by subset size:
        # - For r = 1 to n (subset size)
        #   - Generate all C(n, r) combinations of choosing r sets from n
        #   - For each combination, compute the intersection
        #   - Store the result
        #
        # Example for n=3 sets:
        # r=1: (Set1), (Set2), (Set3)                                    → 3 combinations
        # r=2: (Set1&Set2), (Set1&Set3), (Set2&Set3)                     → 3 combinations
        # r=3: (Set1&Set2&Set3)                                           → 1 combination
        # Total: 3+3+1 = 7 = 2^3 - 1 combinations
        #
        # Complexity Analysis:
        # - Number of combinations: O(2^n) (exponential)
        # - Per combination intersection: O(k) where k is average set size
        # - Total time: O(2^n * k)
        # - Space for results: O(2^n * k) for storing all intersections
        #
        # Optimization Opportunities:
        # - Early filtering by min_size reduces intermediate storage
        # - Using Python's built-in set.intersection is highly optimized
        # - Caching avoids recomputation (self._results_df)
        # -------------------------------------------------------------------------
        results = []  # Collect results for DataFrame construction
        n = len(self.sets_list)  # Total number of input sets
        
        # -------------------------------------------------------------------------
        # Outer Loop: Iterate over all possible subset sizes (r)
        # -------------------------------------------------------------------------
        # r represents the size of the subset we're currently generating
        # - r=1: Single sets (individual set elements)
        # - r=2: Pairwise intersections
        # - r=3: Three-way intersections
        # - ...
        # - r=n: Intersection of ALL sets
        #
        # Note: We start at r=1 to skip the empty subset (r=0)
        # -------------------------------------------------------------------------
        for r in range(1, n + 1):
            
            # -------------------------------------------------------------------------
            # Inner Loop: Generate all combinations of r sets
            # -------------------------------------------------------------------------
            # combinations(range(n), r) uses itertools.combinations to generate
            # all C(n, r) = n! / (r! * (n-r)!) unique combinations
            #
            # Parameter explanation:
            # - range(n): Creates [0, 1, 2, ..., n-1] representing set indices
            # - r: Size of each combination to generate
            #
            # Example: n=3, r=2
            # combinations(range(3), 2) generates: (0,1), (0,2), (1,2)
            # These are indices for: (Set1&Set2), (Set1&Set3), (Set2&Set3)
            #
            # Each idxs tuple contains the indices of sets to intersect
            # -------------------------------------------------------------------------
            for idxs in combinations(range(n), r):
                
                # -------------------------------------------------------------------------
                # Step 1: Compute intersection of all sets in this combination
                # -------------------------------------------------------------------------
                # set.intersection(*[...]) computes the intersection of multiple sets
                #
                # Technical details:
                # - The unpacking operator (*) expands the list into separate arguments
                # - Equivalent to: set.intersection(self.sets_list[0], self.sets_list[1], ...)
                # - Result contains elements present in ALL of the selected sets
                # - Empty set means the selected sets have no common elements
                #
                # Example: idxs = (0, 2, 4) for sets [Set1, Set2, Set3, Set4, Set5]
                # → Intersection of Set1, Set3, Set5
                # -------------------------------------------------------------------------
                intersect_set = set.intersection(*[self.sets_list[i] for i in idxs])
                
                # -------------------------------------------------------------------------
                # Step 2: Apply size filtering (optional)
                # -------------------------------------------------------------------------
                # These conditions allow early filtering of results based on size
                #
                # min_size filter:
                # - If intersection has fewer elements than min_size, skip it
                # - Common use: min_size=1 to exclude empty intersections
                # - min_size=0 includes all combinations (including empty ones)
                #
                # max_size filter:
                # - If intersection has more elements than max_size, skip it
                # - Useful for focusing on small, specific overlaps
                # - None (default) means no upper limit
                #
                # Performance note:
                # - Filtering here reduces memory usage and processing time
                # - Especially important when most combinations are empty
                # -------------------------------------------------------------------------
                if len(intersect_set) < min_size:
                    continue  # Skip if intersection too small
                if max_size is not None and len(intersect_set) > max_size:
                    continue  # Skip if intersection too large
                
                # -------------------------------------------------------------------------
                # Step 3: Retrieve set names for this combination
                # -------------------------------------------------------------------------
                # Get the human-readable names corresponding to the indices in idxs
                # Stored as tuple (immutable) for reliable DataFrame indexing
                #
                # Example: idxs = (1, 3, 5) → set_names = ('Set2', 'Set4', 'Set6')
                # -------------------------------------------------------------------------
                set_names = tuple(self.sets_names[i] for i in idxs)
                
                # -------------------------------------------------------------------------
                # Step 4: Compute exclusive elements for this combination
                # -------------------------------------------------------------------------
                # Exclusive elements are elements that:
                # - Are present in the intersection (intersect_set)
                # - Are NOT present in any other sets
                #
                # Mathematical definition:
                # Exclusive(Combination) = ∩(sets in combination) - ∪(sets NOT in combination)
                #
                # Use case for Venn diagrams:
                # - Each region in a Venn diagram needs exclusive elements
                # - Example: Region for "A & B only" shows elements in A and B, but NOT in C, D, etc.
                # - This is exactly what exclusive_elements represents
                #
                # Example with sets A, B, C:
                # - Intersection of A & B = {1, 2, 3, 4}
                # - Set C = {3, 4, 5, 6}
                # - Exclusive elements for A & B = {1, 2} (not in C)
                # - Intersection A & B & C = {3, 4}
                # -------------------------------------------------------------------------
                if intersect_set and r < n:  # Only compute if not empty and not all sets
                    # -------------------------------------------------------------------------
                    # Case 1: Non-empty intersection, not all sets included
                    # -------------------------------------------------------------------------
                    # Get all other sets (those not in the current combination)
                    #
                    # Example: n=5 total sets, idxs=(0,2,4) for Sets 1, 3, 5
                    # → other_sets = [Set2, Set4] (indices 1 and 3)
                    # -------------------------------------------------------------------------
                    other_sets = [self.sets_list[i] for i in range(n) if i not in idxs]
                    
                    # Union of all elements from other sets
                    # This represents "everything that exists outside the current combination"
                    #
                    # Example: other_sets = [{2,3,5}, {4,6,7}]
                    # → union_others = {2,3,4,5,6,7}
                    # -------------------------------------------------------------------------
                    union_others = set.union(*other_sets) if other_sets else set()
                    
                    # Compute exclusive elements
                    # Using set difference operator: A - B = elements in A not in B
                    #
                    # Example: intersect_set = {1,2,3,4}, union_others = {2,3,4,5,6,7}
                    # → exclusive_set = {1} (only 1 is in intersect but not in others)
                    # -------------------------------------------------------------------------
                    exclusive_set = intersect_set - union_others
                    
                else:
                    # -------------------------------------------------------------------------
                    # Case 2: Either empty intersection OR all sets included
                    # -------------------------------------------------------------------------
                    # Subcase 2a: Empty intersection
                    # - No elements, so no exclusive elements
                    # - exclusive_set = empty set
                    #
                    # Subcase 2b: All sets included (r == n)
                    # - No "other sets" to exclude from
                    # - Everything in the intersection is exclusive by definition
                    # - exclusive_set = intersect_set
                    # -------------------------------------------------------------------------
                    exclusive_set = set() if not intersect_set else intersect_set
                
                # -------------------------------------------------------------------------
                # Step 5: Store results for this combination
                # -------------------------------------------------------------------------
                # Create a dictionary containing all computed information
                # This dictionary will become one row in the final DataFrame
                #
                # Field explanations:
                # - sets: Tuple of set names (immutable, hashable for DataFrame indexing)
                # - set_names: Human-readable string with " & " separator
                # - n_sets: Number of sets in this combination (useful for filtering)
                # - size: Cardinality of the intersection (0 for empty intersections)
                # - elements: Sorted list for consistent output and easy reading
                # - exclusive_size: Count of exclusive elements (for summary stats)
                # - exclusive_elements: Sorted list for Venn diagram labeling
                #
                # Note: Elements are sorted using Python's default ordering
                #       (alphabetical for strings, numeric for numbers)
                # -------------------------------------------------------------------------
                results.append({
                    "sets": set_names,  # Tuple of set names (immutable identifier)
                    "set_names": " & ".join(set_names),  # Human-readable name
                    "n_sets": r,  # Number of sets in combination
                    "size": len(intersect_set),  # Intersection size (0 for empty)
                    "elements": sorted(intersect_set),  # Sorted list of elements
                    "exclusive_size": len(exclusive_set),  # Exclusive elements count
                    "exclusive_elements": sorted(exclusive_set)  # Sorted exclusive elements
                })
        
        # -------------------------------------------------------------------------
        # Step 6: Convert results list to DataFrame
        # -------------------------------------------------------------------------
        # Pandas DataFrame provides:
        # - Tabular structure for easy viewing and analysis
        # - Built-in sorting, filtering, and aggregation capabilities
        # - Export to CSV, Excel, JSON, and other formats
        # - Integration with data analysis tools
        # -------------------------------------------------------------------------
        self._results_df = pd.DataFrame(results)
        
        # -------------------------------------------------------------------------
        # Step 7: Sort results for optimal presentation
        # -------------------------------------------------------------------------
        # Sorting strategy: Prioritize complex and significant overlaps
        #
        # Primary sort key: n_sets (descending)
        # Rationale:
        # - Higher n_sets = more sets involved = more complex overlap
        # - Complex overlaps are often more interesting biologically/scientifically
        # - Example: (A&B&C&D&E) shown before (A&B)
        #
        # Secondary sort key: size (descending)
        # Rationale:
        # - Larger size = more elements in the intersection = more significant
        # - Helps identify major patterns vs minor coincidences
        # - Example: (A&B&C with 100 elements) shown before (A&B&C with 5 elements)
        #
        # reset_index(drop=True):
        # - Creates a clean 0, 1, 2, ... index after sorting
        # - drop=True prevents creating an "index" column with old values
        # - Makes indexing and slicing more predictable
        # -------------------------------------------------------------------------
        if not self._results_df.empty:
            self._results_df = self._results_df.sort_values(
                ['n_sets', 'size'], 
                ascending=[False, False]  # Descending order for both keys
            ).reset_index(drop=True)  # Reset index after sorting
        
        return self._results_df
    
    def compute_exclusive(self) -> pd.DataFrame:
        """
        Compute exclusive elements for each individual set
        
        Exclusive elements are those that belong to only ONE set and not to any
        other sets in the collection. This method calculates these for each set.
        
        Mathematical Definition:
        - Exclusive(A) = A - (B ∪ C ∪ D ∪ ...) for sets A, B, C, D, ...
        - Elements that appear only in set A and nowhere else
        
        Returns
        -------
        pd.DataFrame
            DataFrame with columns:
            - set: set name
            - total_size: total elements in the set
            - exclusive_size: elements only in this set
            - exclusive_elements: sorted list of exclusive elements
            - overlap_size: elements shared with other sets
            
        Notes
        -----
        - Results are cached in self._exclusive_results for reuse
        - overlap_size = total_size - exclusive_size
        - Exclusive elements are useful for identifying set-specific features
        """
        # -------------------------------------------------------------------------
        # Algorithm: Compute exclusive elements for each set
        # -------------------------------------------------------------------------
        # Exclusive elements definition:
        # For a set A, Exclusive(A) = A - (B ∪ C ∪ D ∪ ...)
        # where B, C, D, ... are all other sets in the collection
        #
        # Visual interpretation in Venn diagram:
        # - The region of Set A that does NOT overlap with any other set
        # - The "only A" region in the Venn diagram
        #
        # Example with sets A, B, C:
        # A = {1, 2, 3, 4, 5}
        # B = {2, 3, 6, 7}
        # C = {3, 4, 8, 9}
        #
        # Union of others (B ∪ C) = {2, 3, 4, 6, 7, 8, 9}
        # Exclusive(A) = A - (B ∪ C) = {1, 5}
        # → Elements 1 and 5 appear only in A, not in B or C
        # -------------------------------------------------------------------------
        results = []  # Collect results for DataFrame construction
        n = len(self.sets_list)  # Total number of sets
        
        # -------------------------------------------------------------------------
        # Outer Loop: Process each set individually
        # -------------------------------------------------------------------------
        # For each set, we compute its exclusive elements
        # This means examining each set in isolation against all other sets
        # -------------------------------------------------------------------------
        for i in range(n):
            # -------------------------------------------------------------------------
            # Step 1: Get the current set being analyzed
            # -------------------------------------------------------------------------
            # current_set is the set for which we're computing exclusive elements
            # Example: If i=2, current_set = self.sets_list[2] = Set3
            # -------------------------------------------------------------------------
            current_set = self.sets_list[i]
            
            # -------------------------------------------------------------------------
            # Step 2: Get all other sets (excluding the current one)
            # -------------------------------------------------------------------------
            # Create a list of all sets except the current set
            #
            # Example: n=5, i=2
            # → other_sets = [sets[0], sets[1], sets[3], sets[4]]
            # → other_sets = [Set1, Set2, Set4, Set5] (skipping Set3)
            # -------------------------------------------------------------------------
            other_sets = [self.sets_list[j] for j in range(n) if j != i]
            
            # -------------------------------------------------------------------------
            # Step 3: Compute union of all other sets
            # -------------------------------------------------------------------------
            # This union represents "everything that exists outside the current set"
            # - If an element is in this union, it's shared with another set
            # - If an element is NOT in this union, it's exclusive to the current set
            #
            # Example: other_sets = [{2,3,6,7}, {3,4,8,9}]
            # → union_others = {2, 3, 4, 6, 7, 8, 9}
            #
            # Note: set.union(*other_sets) unpacks the list and computes union
            #       The empty set check handles edge case of single-set input
            # -------------------------------------------------------------------------
            union_others = set.union(*other_sets) if other_sets else set()
            
            # -------------------------------------------------------------------------
            # Step 4: Compute exclusive elements using set difference
            # -------------------------------------------------------------------------
            # Using Python's set difference operator: A - B = elements in A not in B
            #
            # exclusive = current_set - union_others
            # = elements in current_set that are NOT in any other set
            #
            # Example:
            # current_set = {1, 2, 3, 4, 5}
            # union_others = {2, 3, 4, 6, 7, 8, 9}
            # exclusive = {1, 5}
            #
            # Interpretation:
            # - Elements 1 and 5 appear ONLY in current_set
            # - Elements 2, 3, 4 appear in current_set AND at least one other set
            # -------------------------------------------------------------------------
            exclusive = current_set - union_others
            
            # -------------------------------------------------------------------------
            # Step 5: Store results for this set
            # -------------------------------------------------------------------------
            # Create a dictionary with comprehensive information about the set
            #
            # Field explanations:
            # - set: Name of the set (for identification)
            # - total_size: Total number of elements in the set
            # - exclusive_size: Count of elements only in this set
            # - exclusive_elements: Sorted list of exclusive elements (for Venn diagrams)
            # - overlap_size: Elements shared with other sets (total - exclusive)
            #
            # Mathematical relationship:
            # overlap_size = total_size - exclusive_size
            #               = len(current_set) - len(exclusive)
            #               = len(current_set ∩ (union of other sets))
            # -------------------------------------------------------------------------
            results.append({
                "set": self.sets_names[i],  # Set name (e.g., "Set3")
                "total_size": len(current_set),  # Total elements in set
                "exclusive_size": len(exclusive),  # Count of exclusive elements
                "exclusive_elements": sorted(exclusive),  # Sorted list of exclusive elements
                "overlap_size": len(current_set) - len(exclusive)  # Elements shared with others
            })
        
        # -------------------------------------------------------------------------
        # Step 6: Convert to DataFrame and cache
        # -------------------------------------------------------------------------
        # Create DataFrame from results list for easy analysis and export
        # Cache the result to avoid recomputation if method called again
        # -------------------------------------------------------------------------
        self._exclusive_results = pd.DataFrame(results)
        return self._exclusive_results
    
    def get_pairwise_overlap(self) -> Dict[str, pd.DataFrame]:
        """
        Generate pairwise overlap and Jaccard similarity matrices
        
        This method creates two symmetric matrices showing relationships between
        all pairs of sets:
        1. Overlap matrix: counts of intersecting elements (|A ∩ B|)
        2. Jaccard matrix: Jaccard similarity coefficients (0.0 - 1.0)
        
        Jaccard Similarity Formula:
        Jaccard(A, B) = |A ∩ B| / |A ∪ B|
        - 0.0 = no overlap (disjoint sets)
        - 1.0 = identical sets (A = B)
        - Values between represent degree of similarity
        
        Returns
        -------
        dict
            Dictionary containing two DataFrames:
            - 'overlap_matrix': Symmetric DataFrame with intersection counts
            - 'jaccard_matrix': Symmetric DataFrame with Jaccard coefficients
            
        Examples
        --------
        >>> matrices = calc.get_pairwise_overlap()
        >>> print("Overlap Matrix (intersection counts):")
        >>> print(matrices['overlap_matrix'])
        >>> print("\nJaccard Similarity Matrix (0.0-1.0):")
        >>> print(matrices['jaccard_matrix'].round(3))
        """
        # -------------------------------------------------------------------------
        # Algorithm: Generate pairwise overlap and similarity matrices
        # -------------------------------------------------------------------------
        # This method creates two symmetric n×n matrices where:
        # - Rows represent sets (indexed by set names)
        # - Columns represent sets (indexed by set names)
        # - Each cell shows a relationship between the row set and column set
        #
        # Example for 3 sets (A, B, C):
        # Overlap Matrix:
        #       A    B    C
        # A   [5]   3    2
        # B   [3]   [6]  4
        # C   [2]   [4]  [7]
        #
        # Diagonal elements [5, 6, 7] = set sizes (overlap with self)
        # Off-diagonal elements = pairwise overlaps
        # Matrix is symmetric: overlap_matrix[i,j] = overlap_matrix[j,i]
        # -------------------------------------------------------------------------
        n = len(self.sets_names)  # Number of sets
        
        # -------------------------------------------------------------------------
        # Step 1: Initialize matrices with zeros
        # -------------------------------------------------------------------------
        # Create n×n DataFrames with set names as both row and column indices
        #
        # overlap_matrix: Integer matrix for intersection counts
        # - Initial value: 0 (no overlap until computed)
        # - Type: int (counts are whole numbers)
        #
        # jaccard_matrix: Float matrix for Jaccard similarity coefficients
        # - Initial value: 0.0 (no similarity until computed)
        # - Type: float (Jaccard is a ratio between 0.0 and 1.0)
        #
        # Using DataFrame provides:
        # - Automatic row/column labeling with set names
        # - Easy indexing by set name (e.g., overlap_matrix['A']['B'])
        # - Built-in display formatting
        # - Export capabilities (to_csv, to_excel, etc.)
        # -------------------------------------------------------------------------
        overlap_matrix = pd.DataFrame(0, 
                                    index=self.sets_names, 
                                    columns=self.sets_names)
        
        jaccard_matrix = pd.DataFrame(0.0, 
                                     index=self.sets_names, 
                                     columns=self.sets_names)
        
        # -------------------------------------------------------------------------
        # Step 2: Calculate pairwise metrics for all set pairs
        # -------------------------------------------------------------------------
        # Optimization strategy:
        # - Only compute upper triangle (i <= j) due to matrix symmetry
        # - Then mirror results to lower triangle (i > j)
        # - This reduces computation from n² to n(n+1)/2 ≈ 50% savings
        #
        # Loop structure:
        # for i in range(n):           # Outer loop: all rows
        #   for j in range(i, n):      # Inner loop: columns from diagonal to end
        #
        # Example for n=3:
        # i=0: j=0,1,2 → (0,0), (0,1), (0,2) → diagonal + upper triangle row 0
        # i=1: j=1,2   → (1,1), (1,2)          → diagonal + upper triangle row 1
        # i=2: j=2     → (2,2)                 → diagonal only
        # Total: 6 computations vs 9 if full matrix
        # -------------------------------------------------------------------------
        for i in range(n):
            for j in range(i, n):
                # -------------------------------------------------------------------------
                # Step 2a: Get the two sets being compared
                # -------------------------------------------------------------------------
                # set_i is the set at index i
                # set_j is the set at index j
                #
                # Note: When i == j (diagonal), set_i and set_j are the same set
                # -------------------------------------------------------------------------
                set_i = self.sets_list[i]
                set_j = self.sets_list[j]
                
                # -------------------------------------------------------------------------
                # Step 2b: Compute intersection size (|A ∩ B|)
                # -------------------------------------------------------------------------
                # Using Python's set intersection operator: &
                #
                # Example:
                # set_i = {1, 2, 3, 4, 5}
                # set_j = {2, 3, 4, 6, 7}
                # set_i & set_j = {2, 3, 4}
                # intersection = len({2, 3, 4}) = 3
                #
                # Diagonal case (i == j):
                # set_i & set_i = set_i
                # intersection = len(set_i) = size of the set
                # -------------------------------------------------------------------------
                intersection = len(set_i & set_j)
                
                # -------------------------------------------------------------------------
                # Step 2c: Compute union size (|A ∪ B|)
                # -------------------------------------------------------------------------
                # Using Python's set union operator: |
                #
                # Example:
                # set_i = {1, 2, 3, 4, 5}
                # set_j = {2, 3, 4, 6, 7}
                # set_i | set_j = {1, 2, 3, 4, 5, 6, 7}
                # union = len({1, 2, 3, 4, 5, 6, 7}) = 7
                #
                # Diagonal case (i == j):
                # set_i | set_i = set_i
                # union = len(set_i) = size of the set
                # -------------------------------------------------------------------------
                union = len(set_i | set_j)
                
                # -------------------------------------------------------------------------
                # Step 2d: Fill both triangles in overlap matrix
                # -------------------------------------------------------------------------
                # Due to symmetry (intersection of A&B = intersection of B&A),
                # we fill both positions with the same value
                #
                # overlap_matrix.iloc[i, j]: Row i, Column j
                # overlap_matrix.iloc[j, i]: Row j, Column i
                #
                # Diagonal case (i == j):
                # Both operations write to the same position
                # Effectively redundant but harmless
                # -------------------------------------------------------------------------
                overlap_matrix.iloc[i, j] = intersection
                overlap_matrix.iloc[j, i] = intersection
                
                # -------------------------------------------------------------------------
                # Step 2e: Compute Jaccard similarity and fill matrix
                # -------------------------------------------------------------------------
                # Jaccard formula: J(A, B) = |A ∩ B| / |A ∪ B|
                #
                # Jaccard properties:
                # - Range: 0.0 ≤ Jaccard ≤ 1.0
                # - 0.0: No overlap (disjoint sets)
                # - 1.0: Identical sets
                # - 0.5: Half the union is in the intersection
                #
                # Edge case handling:
                # - If union == 0 (both sets are empty), division would cause error
                # - Define Jaccard = 0.0 for two empty sets (conventional choice)
                #
                # Example:
                # intersection = 3, union = 7
                # Jaccard = 3/7 ≈ 0.429
                #
                # Diagonal case (i == j):
                # intersection = union = set size
                # Jaccard = size/size = 1.0 (sets are identical to themselves)
                # -------------------------------------------------------------------------
                jaccard = intersection / union if union > 0 else 0.0
                jaccard_matrix.iloc[i, j] = jaccard
                jaccard_matrix.iloc[j, i] = jaccard
        
        return {
            'overlap_matrix': overlap_matrix,  # Raw intersection counts
            'jaccard_matrix': jaccard_matrix   # Similarity coefficients (0.0 to 1.0)
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics of all set overlaps
        
        This method provides a high-level overview including:
        - Basic counts and sizes
        - Elements common to all sets (intersection of all n sets)
        - Maximum overlap information (largest intersection found)
        - Complete overlap data in dictionary format
        - Statistics about empty vs non-empty combinations
        
        Returns
        -------
        dict
            Dictionary containing comprehensive statistics:
            - 'n_sets': number of input sets
            - 'set_names': list of all set names
            - 'set_sizes': dictionary mapping names to sizes
            - 'total_unique_elements': size of union of all sets
            - 'all_common_size': elements present in ALL sets
            - 'max_overlap_size': size of largest overlap
            - 'max_overlap_sets': which sets have the maximum overlap
            - 'all_overlaps': list of all overlap dictionaries from last compute()
            - 'n_combinations': number of combinations from last compute()
            - 'empty_combinations': number of empty intersections (size=0)
            - 'non_empty_combinations': number of non-empty intersections
            
        Notes
        -----
        - Automatically triggers compute() with default parameters if not already done
        - Returns statistics based on whatever the last compute() produced (respects filters)
        - Call compute(min_size=0) explicitly before get_summary() if you need all 2^n - 1 combinations
        - This is a simple getter - does NOT recompute or modify cached results
        """
        # -------------------------------------------------------------------------
        # Step 1: Ensure computation has been performed
        # -------------------------------------------------------------------------
        # If no computation has been done yet, trigger compute() with default parameters
        #
        # Important behavior:
        # - This does NOT recompute if results already exist
        # - Returns cached results from the most recent compute() call
        # - If previous compute() had filters (min_size, max_size), those are reflected
        #
        # To get ALL 2^n - 1 combinations:
        # - Call compute(min_size=0) explicitly before get_summary()
        # - Otherwise, only combinations from the last compute() are included
        #
        # Default behavior:
        # - compute() with no arguments uses min_size=0
        # - This includes all combinations, even empty ones
        # -------------------------------------------------------------------------
        if self._results_df is None:
            self.compute()
        
        # -------------------------------------------------------------------------
        # Step 2: Build basic summary statistics (set-level)
        # -------------------------------------------------------------------------
        # These statistics are independent of overlap computation
        # They describe the input sets themselves
        #
        # Summary structure:
        # - n_sets: Total number of sets in the analysis
        # - set_names: List of all set identifiers (preserves input order)
        # - set_sizes: Dictionary mapping each set name to its element count
        # - total_unique_elements: Size of the union of all sets
        #
        # Example:
        # n_sets = 3
        # set_names = ['Set1', 'Set2', 'Set3']
        # set_sizes = {'Set1': 5, 'Set2': 7, 'Set3': 4}
        # total_unique_elements = 12 (union of all three sets)
        # -------------------------------------------------------------------------
        summary = {
            'n_sets': len(self.sets_list),  # Total number of input sets
            'set_names': self.sets_names,   # List of all set names in order
            'set_sizes': {  # Dictionary mapping set names to their sizes
                name: len(s) 
                for name, s in zip(self.sets_names, self.sets_list)
            },
            'total_unique_elements': len(set.union(*self.sets_list)),  # Union size
        }
        
        # -------------------------------------------------------------------------
        # Step 3: Add overlap-specific statistics (from cached results)
        # -------------------------------------------------------------------------
        # These statistics depend on the compute() results
        # They provide insights into overlap patterns
        #
        # 3a: Elements common to ALL sets
        # -------------------------------------------------------------------------
        # This is the intersection of all n sets
        # Represents elements present in every single set
        #
        # Example: For 3 sets A, B, C
        # - Intersection A∩B∩C = elements in all three sets
        # - This is the "common core" across all conditions
        #
        # Implementation:
        # - Filter results for rows where n_sets == total number of sets
        # - There should be exactly 1 row (intersection of all sets)
        # - Extract the 'size' value from that row
        #
        # Edge case handling:
        # - If filtered DataFrame is empty (shouldn't happen), return 0
        # - Uses .iloc[0] to safely access first row if exists
        # -------------------------------------------------------------------------
        all_common = self._results_df[
            self._results_df['n_sets'] == len(self.sets_list)
        ]
        summary['all_common_size'] = all_common['size'].iloc[0] if not all_common.empty else 0
        
        # -------------------------------------------------------------------------
        # 3b: Maximum overlap information
        # -------------------------------------------------------------------------
        # Identifies the largest intersection across all combinations
        # Useful for understanding the most significant overlap pattern
        #
        # max_overlap_size: Largest intersection size found
        # max_overlap_sets: Which set combination has this maximum overlap
        #
        # Example:
        # - If Set2 & Set5 & Set7 has 12 elements (largest)
        # - max_overlap_size = 12
        # - max_overlap_sets = ('Set2', 'Set5', 'Set7')
        #
        # Implementation:
        # - .size.max() finds the maximum value in the 'size' column
        # - .size.idxmax() returns the index of the row with maximum size
        # - .loc[idxmax, 'sets'] retrieves the set names from that row
        # -------------------------------------------------------------------------
        summary['max_overlap_size'] = self._results_df['size'].max()
        summary['max_overlap_sets'] = self._results_df.loc[
            self._results_df['size'].idxmax(), 'sets'
        ]
        
        # -------------------------------------------------------------------------
        # 3c: Complete overlap data and statistics
        # -------------------------------------------------------------------------
        # These provide comprehensive information about all combinations
        #
        # all_overlaps: List of dictionaries, one per combination
        # - Contains all columns from the results DataFrame
        # - Useful for programmatic processing or custom analysis
        # - Format: [{...combo1...}, {...combo2...}, ...]
        #
        # n_combinations: Total number of combinations
        # - Depends on previous compute() filters (min_size, max_size)
        # - With min_size=0: 2^n - 1 total combinations
        # - With min_size=1: only non-empty combinations
        #
        # empty_combinations: Count of intersections with size=0
        # - Useful for understanding how many regions in Venn diagram are empty
        # - Example: If 30/127 combinations are empty, many regions overlap
        #
        # non_empty_combinations: Count of intersections with size>0
        # - Complement of empty_combinations
        # - Represents meaningful overlaps with actual elements
        # -------------------------------------------------------------------------
        summary['all_overlaps'] = self._results_df.to_dict('records')
        summary['n_combinations'] = len(self._results_df)  # Total number of combinations
        summary['empty_combinations'] = len(self._results_df[self._results_df['size'] == 0])
        summary['non_empty_combinations'] = len(self._results_df[self._results_df['size'] > 0])
        
        return summary
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the computed overlap results as a DataFrame
        
        Returns a DataFrame with the results from the most recent compute() call.
        This is a simple getter that does not recompute or modify data.
        
        Returns
        -------
        pd.DataFrame
            DataFrame containing overlap computation results
            
        Notes
        -----
        Automatically triggers compute() if not already done
        Returns whatever the last compute() produced (including any filters)
        """
        # Ensure computation is done
        # Note: This simply returns cached results. Call compute(min_size=0) explicitly
        # before get_dataframe() if you need all 2^n - 1 combinations including empty ones.
        if self._results_df is None:
            self.compute()
        return self._results_df
    
    def get_plot_data(self) -> pd.DataFrame:
        """
        Get DataFrame formatted for Venn diagram plotting
        
        Returns a DataFrame with selected columns suitable for plotting Venn diagrams.
        For single-set regions (n_sets == 1), shows exclusive elements instead of 
        all elements, which is more appropriate for Venn diagram region labeling.
        
        Returns
        -------
        pd.DataFrame
            DataFrame with columns: set_names, n_sets, size, elements
            For n_sets == 1: size = exclusive_size, elements = exclusive_elements
            For n_sets > 1: size and elements are the intersection values
            
        Notes
        -----
        Automatically triggers compute(min_size=0) if not already done
        This ensures all 2^n - 1 combinations are available for plotting
        """
        # -------------------------------------------------------------------------
        # Step 1: Ensure all combinations are available
        # -------------------------------------------------------------------------
        # Venn diagrams require complete data (all 2^n - 1 combinations)
        # to correctly represent all regions
        #
        # If no computation has been done:
        # - Call compute(min_size=0) to get ALL combinations
        # - min_size=0 ensures empty intersections are included
        #
        # Important behavior:
        # - This guarantees completeness for plotting
        # - If computation exists but has filters, they may be ignored
        #   (only if computation doesn't exist yet)
        # -------------------------------------------------------------------------
        if self._results_df is None:
            self.compute(min_size=0)
        
        # -------------------------------------------------------------------------
        # Step 2: Create a working copy of the relevant columns
        # -------------------------------------------------------------------------
        # We need specific columns for Venn diagram plotting
        # Using .copy() ensures we don't modify the cached DataFrame
        #
        # Selected columns:
        # - set_names: Human-readable combination name (for labeling)
        # - n_sets: Number of sets in combination (for region identification)
        # - size: Intersection size (for display in Venn diagram)
        # - elements: List of elements (for labeling or debugging)
        # - exclusive_size: Count of exclusive elements (for single sets)
        # - exclusive_elements: List of exclusive elements (for single sets)
        #
        # Why copy()?
        # - Modifying plot_df shouldn't affect self._results_df
        # - Cached DataFrame should remain unchanged
        # - Allows multiple calls to get_plot_data() independently
        # -------------------------------------------------------------------------
        plot_df = self._results_df[['set_names', 'n_sets', 'size', 'elements', 'exclusive_size', 'exclusive_elements']].copy()
        
        # -------------------------------------------------------------------------
        # Step 3: Replace single-set data with exclusive elements
        # -------------------------------------------------------------------------
        # This is the KEY transformation for correct Venn diagram rendering
        #
        # Problem: For single sets (n_sets=1), the 'size' and 'elements' columns
        #          contain ALL elements in that set, not just the exclusive ones
        #
        # Solution: Replace with exclusive elements for single-set regions
        #
        # Example with sets A, B, C:
        # In the results DataFrame:
        # - Row for Set1 (n_sets=1): size=5, elements=[1,2,3,4,5]
        # - This includes elements that overlap with Set2 and Set3!
        #
        # But for Venn diagram region "only A" (not overlapping with B or C):
        # - We need exclusive elements: [elements only in Set1]
        # - Say exclusive elements are [1, 2]
        #
        # After transformation:
        # - size = 2 (exclusive_size)
        # - elements = [1, 2] (exclusive_elements)
        #
        # Multi-set regions (n_sets > 1):
        # - No change needed
        # - Intersection data is correct as-is
        # - Example: "A & B" region correctly shows elements in both A and B
        #
        # Implementation details:
        # - Create boolean mask: single_set_mask = (n_sets == 1)
        # - Use .loc[mask, column] to update only masked rows
        # - Apply update to both 'size' and 'elements' columns
        # -------------------------------------------------------------------------
        single_set_mask = plot_df['n_sets'] == 1
        plot_df.loc[single_set_mask, 'size'] = plot_df.loc[single_set_mask, 'exclusive_size']
        plot_df.loc[single_set_mask, 'elements'] = plot_df.loc[single_set_mask, 'exclusive_elements']
        
        # -------------------------------------------------------------------------
        # Step 4: Clean up temporary columns
        # -------------------------------------------------------------------------
        # Remove exclusive_size and exclusive_elements columns
        # They were needed for the transformation but not for the final output
        #
        # Final output columns:
        # - set_names: Combination identifier
        # - n_sets: Number of sets (useful for filtering)
        # - size: Corrected size (exclusive for single sets, intersection for multi-sets)
        # - elements: Corrected elements (exclusive for single sets, intersection for multi-sets)
        #
        # Why drop?
        # - Keeps output clean and focused
        # - Prevents confusion about which size/elements to use
        # - Makes DataFrame smaller and easier to work with
        # -------------------------------------------------------------------------
        plot_df = plot_df.drop(columns=['exclusive_size', 'exclusive_elements'])
        
        # -------------------------------------------------------------------------
        # Return DataFrame ready for Venn diagram plotting
        # -------------------------------------------------------------------------
        # The returned DataFrame can be used by plotting libraries or custom code
        # to generate Venn diagrams with correct region sizes and labels
        # -------------------------------------------------------------------------
        return plot_df
    
    def query_elements(self, query_sets: Optional[List[str]] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Query overlap information for specific set combinations
        
        This flexible method allows querying specific set combinations or
        retrieving all possible combinations when no argument is provided.
        
        Two modes of operation:
        1. Specific query: Provide list of set names to get one combination
        2. All combinations: No arguments returns all 2^n - 1 combinations
        
        Parameters
        ----------
        query_sets : list of str, optional
            List of set names to query. If None (default), returns ALL 
            possible overlap combinations (2^n - 1 total).
            
        Returns
        -------
        dict or list of dict
            - If query_sets provided: Single dictionary with overlap info
            - If query_sets is None: List of dictionaries for all combinations
            
        Dictionary keys (consistent across both return types):
        - 'sets': tuple of set names (immutable identifier)
        - 'set_names': string representation (human-readable)
        - 'n_sets': number of sets in combination
        - 'size': intersection size (0 for empty intersections)
        - 'elements': sorted list of intersecting elements
        - 'exclusive_size': exclusive elements count
        - 'exclusive_elements': sorted list of exclusive elements
        
        Examples
        --------
        >>> # Query specific combination (returns single dict)
        >>> result = calc.query_elements(['SetA', 'SetB'])
        >>> print(f"Intersection size: {result['size']}")
        >>> print(f"Elements: {result['elements']}")
        >>> print(f"Exclusive to A&B: {result['exclusive_elements']}")
        
        >>> # Get all combinations (returns list of dicts)
        >>> all_results = calc.query_elements()  # No arguments
        >>> print(f"Total combinations: {len(all_results)}")
        >>> for combo in all_results:
        >>>     if combo['size'] > 0:  # Only show non-empty
        >>>         print(f"{combo['set_names']}: {combo['elements']}")
        """
        # -------------------------------------------------------------------------
        # Mode 1: No specific sets provided - return ALL combinations
        # -------------------------------------------------------------------------
        # When query_sets is None, compute and return all 2^n - 1 possible combinations
        #
        # Use cases:
        # - Generating complete reports
        # - Exporting all overlap data to external systems
        # - Performing custom analysis not supported by built-in methods
        # - Debugging or exploring data structure
        #
        # Implementation notes:
        # - Uses same algorithm as compute() for consistency
        # - Does NOT use cached results (always recomputes)
        # - Returns list of dicts instead of DataFrame
        # - Each dict contains complete information for one combination
        #
        # Return format:
        # [
        #   {
        #     'sets': ('Set1', 'Set2'),              # Tuple of set names
        #     'set_names': 'Set1 & Set2',             # String representation
        #     'n_sets': 2,                            # Number of sets
        #     'size': 5,                              # Intersection size
        #     'elements': [1, 2, 3, 4, 5],            # Sorted elements
        #     'exclusive_size': 3,                     # Exclusive count
        #     'exclusive_elements': [1, 2, 3]         # Exclusive elements
        #   },
        #   ... (one dict per combination)
        # ]
        # -------------------------------------------------------------------------
        if query_sets is None:
            results = []
            n = len(self.sets_list)
            
            # -------------------------------------------------------------------------
            # Generate all combinations using same algorithm as compute()
            # -------------------------------------------------------------------------
            # Outer loop: Iterate over subset sizes (1 to n)
            # Inner loop: Generate all combinations for each subset size
            # -------------------------------------------------------------------------
            for r in range(1, n + 1):
                for idxs in combinations(range(n), r):
                    # -------------------------------------------------------------------------
                    # Step 1: Compute intersection for this combination
                    # -------------------------------------------------------------------------
                    intersect_set = set.intersection(*[self.sets_list[i] for i in idxs])
                    
                    # -------------------------------------------------------------------------
                    # Step 2: Get set names for this combination
                    # -------------------------------------------------------------------------
                    set_names = tuple(self.sets_names[i] for i in idxs)
                    
                    # -------------------------------------------------------------------------
                    # Step 3: Compute exclusive elements
                    # -------------------------------------------------------------------------
                    # Same logic as in compute() method
                    # -------------------------------------------------------------------------
                    if intersect_set and r < n:
                        other_sets = [self.sets_list[i] for i in range(n) if i not in idxs]
                        union_others = set.union(*other_sets) if other_sets else set()
                        exclusive_set = intersect_set - union_others
                    else:
                        exclusive_set = set()
                    
                    # -------------------------------------------------------------------------
                    # Step 4: Store result dictionary
                    # -------------------------------------------------------------------------
                    results.append({
                        'sets': set_names,
                        'set_names': " & ".join(set_names),
                        'n_sets': r,
                        'size': len(intersect_set),
                        'elements': sorted(intersect_set),
                        'exclusive_size': len(exclusive_set),
                        'exclusive_elements': sorted(exclusive_set)
                    })
            
            return results
        
        # -------------------------------------------------------------------------
        # Mode 2: Query specific set combination
        # -------------------------------------------------------------------------
        # When query_sets is provided, compute overlap only for those specific sets
        #
        # Use cases:
        # - Testing a specific hypothesis (e.g., "Do genes A, B, and C overlap?")
        # - Focused analysis on a subset of conditions
        # - Interactive exploration with user input
        # - Performance optimization when only one combination is needed
        #
        # Advantages over compute():
        # - Faster: only computes one intersection vs all 2^n - 1
        # - More precise: direct query instead of filtering full results
        # - Simpler: returns single dict instead of DataFrame
        #
        # Return format (single dictionary):
        # {
        #   'sets': ('Set1', 'Set2', 'Set3'),           # Tuple of queried set names
        #   'set_names': 'Set1 & Set2 & Set3',          # String representation
        #   'n_sets': 3,                                # Number of sets
        #   'size': 2,                                  # Intersection size
        #   'elements': [1, 2],                        # Sorted elements
        #   'exclusive_size': 1,                        # Exclusive count
        #   'exclusive_elements': [1]                   # Exclusive elements
        # }
        # -------------------------------------------------------------------------
        
        # -------------------------------------------------------------------------
        # Step 1: Validate all provided set names
        # -------------------------------------------------------------------------
        # Ensure each name in query_sets exists in self.sets_names
        #
        # Validation is critical because:
        # - Typo detection (e.g., user types "Sett1" instead of "Set1")
        # - Prevents IndexError when calling .index()
        # - Provides helpful error message with available options
        # -------------------------------------------------------------------------
        for name in query_sets:
            if name not in self.sets_names:
                raise ValueError(f"Unknown set name: '{name}'. "
                               f"Available sets: {self.sets_names}")
        
        # -------------------------------------------------------------------------
        # Step 2: Get indices of queried sets
        # -------------------------------------------------------------------------
        # Map set names to their indices in self.sets_list
        #
        # Example:
        # - query_sets = ['Set2', 'Set5', 'Set7']
        # - self.sets_names = ['Set1', 'Set2', 'Set3', 'Set4', 'Set5', 'Set6', 'Set7']
        # - idxs = [1, 4, 6]
        #
        # Note: We could use a dictionary for O(1) lookup, but .index() is fast enough
        #       for typical use cases (n < 1000 sets)
        # -------------------------------------------------------------------------
        idxs = [self.sets_names.index(name) for name in query_sets]
        
        # -------------------------------------------------------------------------
        # Step 3: Compute intersection of queried sets
        # -------------------------------------------------------------------------
        # Using same intersection logic as compute() for consistency
        #
        # Example: idxs = [1, 4, 6]
        # → Intersection of Set2, Set5, and Set7
        # -------------------------------------------------------------------------
        intersect_set = set.intersection(*[self.sets_list[i] for i in idxs])
        
        # -------------------------------------------------------------------------
        # Step 4: Compute exclusive elements
        # -------------------------------------------------------------------------
        # Same logic as compute() method
        # - If r < n: subtract union of other sets
        # - If r == n: all elements are exclusive
        # -------------------------------------------------------------------------
        n = len(self.sets_list)
        r = len(idxs)
        if r < n:
            other_sets = [self.sets_list[i] for i in range(n) if i not in idxs]
            union_others = set.union(*other_sets) if other_sets else set()
            exclusive_set = intersect_set - union_others
        else:
            exclusive_set = intersect_set
        
        # -------------------------------------------------------------------------
        # Step 5: Return result dictionary
        # -------------------------------------------------------------------------
        # Note: We return query_sets (input names) instead of set_names (converted)
        #       to preserve the exact order and naming provided by user
        # -------------------------------------------------------------------------
        return {
            'sets': tuple(query_sets),
            'set_names': " & ".join(query_sets),
            'n_sets': r,
            'size': len(intersect_set),
            'elements': sorted(intersect_set),
            'exclusive_size': len(exclusive_set),
            'exclusive_elements': sorted(exclusive_set)
        }
    
    # -------------------------------------------------------------------------
    # __repr__: String representation of the calculator instance
    # -------------------------------------------------------------------------
    # Purpose: Provide a concise, informative string representation of the instance
    #
    # When is __repr__ called?
    # - When you print() an instance
    # - When you type the instance name in an interactive session
    # - When you include the instance in a string formatting expression
    # - When debugging with repr(instance)
    #
    # Design goals:
    # - Show essential information (number of sets and their names)
    # - Be unambiguous and helpful for debugging
    # - Be similar to how you would create the instance
    # - Be concise (not too verbose)
    #
    # Return format:
    # "OverlapCalculator(n_sets=X, sets=[...])"
    #
    # Example output:
    # OverlapCalculator(n_sets=3, sets=['Set1', 'Set2', 'Set3'])
    #
    # Relationship to __str__:
    # - If __str__ is not defined, __repr__ is used as fallback
    # - __repr__ aims for unambiguous, detailed representation
    # - __str__ aims for user-friendly representation
    # - For this class, we only implement __repr__ (sufficient for both use cases)
    # -------------------------------------------------------------------------
    def __repr__(self) -> str:
        """
        String representation of the calculator instance
        
        This method provides a concise and informative representation of the
        OverlapCalculator instance, showing the number of sets and their names.
        
        Returns
        -------
        str
            Formatted string showing number of sets and their names
            Format: "OverlapCalculator(n_sets=X, sets=[name1, name2, ...])"
            
        Examples
        --------
        >>> # Create a calculator instance
        >>> calc = OverlapCalculator({'Set1': {1,2}, 'Set2': {2,3}})
        >>> 
        >>> # Print the instance (calls __repr__)
        >>> print(calc)
        OverlapCalculator(n_sets=2, sets=['Set1', 'Set2'])
        >>> 
        >>> # Interactive display (also calls __repr__)
        >>> calc
        OverlapCalculator(n_sets=2, sets=['Set1', 'Set2'])
        >>> 
        >>> # With more sets
        >>> data = {'A': {1,2}, 'B': {2,3}, 'C': {3,4}, 'D': {4,5}}
        >>> calc = OverlapCalculator(data)
        >>> print(calc)
        OverlapCalculator(n_sets=4, sets=['A', 'B', 'C', 'D'])
        
        Notes
        -----
        - This representation is useful for debugging and logging
        - Shows the key state information (number and names of sets)
        - Does not show the actual elements (would be too verbose)
        - Does not show computed results (state can change with methods)
        """
        # -------------------------------------------------------------------------
        # Implementation
        # -------------------------------------------------------------------------
        # Use f-string for clear, readable format string
        #
        # Components:
        # - "OverlapCalculator": Class name (for identification)
        # - "n_sets={len(self.sets_list)}": Number of input sets
        # - "sets={self.sets_names}": List of set names
        #
        # Example construction:
        # self.sets_list = [{1,2}, {2,3}]  # Length = 2
        # self.sets_names = ['Set1', 'Set2']
        # return f"OverlapCalculator(n_sets=2, sets=['Set1', 'Set2'])"
        # -------------------------------------------------------------------------
        return f"OverlapCalculator(n_sets={len(self.sets_list)}, sets={self.sets_names})"


# =============================================================================
# Usage Examples and Demonstration
# =============================================================================
# This section demonstrates the full functionality of the OverlapCalculator class
# with a realistic example using 7 sets with overlapping gene elements.
# The example progressively showcases different analysis methods.
# 
# Example Scenario: Analyzing gene expression overlaps across 7 experimental conditions
# - Each set represents a set of genes identified in a specific condition
# - Genes are represented as "g1", "g2", etc.
# - Overlaps reveal genes that are shared across multiple conditions
# =============================================================================

if __name__ == "__main__":
    # -------------------------------------------------------------------------
    # Create Sample Data
    # -------------------------------------------------------------------------
    # Define test data using dictionary format (recommended for clarity)
    # Each key-value pair represents a set with its unique identifier and elements
    # 
    # Note: In this example, genes are arranged to create various overlap patterns:
    # - g1 appears only in Set1 (unique to Set1)
    # - g2 appears in Set1 and Set2 (pairwise overlap)
    # - g3, g4 appear in Set1, Set2, Set3 (three-way overlap)
    # - g4 appears in all sets (common to all conditions)
    # ...and more complex patterns
    # -------------------------------------------------------------------------
    data_dict = {
        'Set1': {"g1", "g2", "g3", "g4", "g5"},      # Genes in condition 1
        'Set2': {"g2", "g3", "g4", "g6", "g7"},      # Genes in condition 2
        'Set3': {"g3", "g4", "g5", "g7", "g8"},      # Genes in condition 3
        'Set4': {"g4", "g5", "g6", "g8", "g9"},      # Genes in condition 4
        'Set5': {"g5", "g6", "g7", "g9", "g10"},     # Genes in condition 5
        'Set6': {"g6", "g7", "g8", "g9", "g10"},     # Genes in condition 6
        'Set7': {"g7", "g8", "g9", "g10", "g11"}     # Genes in condition 7
    }
    
    # -------------------------------------------------------------------------
    # Initialize the Calculator
    # -------------------------------------------------------------------------
    # Create an OverlapCalculator instance with the data
    # The constructor automatically parses and validates the input data
    # 
    # Expected output from print(calc): 
    # OverlapCalculator(n_sets=7, sets=['Set1', 'Set2', 'Set3', 'Set4', 'Set5', 'Set6', 'Set7'])
    # -------------------------------------------------------------------------
    calc = OverlapCalculator(data_dict)
    
    # -------------------------------------------------------------------------
    # Compute All Overlaps (Including Empty Intersections)
    # -------------------------------------------------------------------------
    # Demonstration 1: Get all possible combinations (2^n - 1 = 2^7 - 1 = 127 total)
    # 
    # Key Points:
    # - min_size=0 includes all combinations, even those with empty intersections
    # - This is useful for generating complete Venn diagram data
    # - Results are sorted by n_sets (descending) then size (descending)
    # -------------------------------------------------------------------------
    print("=== All Overlap Situations (including empty) ===")
    df = calc.compute(min_size=0)  # Include empty intersections
    print(f"Total combinations (2^n - 1): {len(df)}")
    print(df[['set_names', 'size', 'elements']])

    # -------------------------------------------------------------------------
    # Export Complete Overlap Results to CSV
    # -------------------------------------------------------------------------
    # Demonstration 2: Query all combinations using the default parameter
    # and export to CSV for external analysis or reporting
    #
    # Key Points:
    # - query_elements() with no arguments returns all 2^n - 1 combinations
    # - get_dataframe() returns the cached DataFrame from the last compute() call
    # - CSV export enables downstream analysis in Excel, R, or other tools
    # - Output file: all_overlaps.csv (includes all columns: sets, set_names, n_sets, 
    #   size, elements, exclusive_size, exclusive_elements)
    # -------------------------------------------------------------------------
    print("\n=== Query All Possible Combinations (using default) ===")
    all_results = calc.query_elements()  # Using default value - returns all combinations
    print("++++++++++++++++++++++++++++++++++")
    all = calc.get_dataframe()
    all.to_csv("all_overlaps.csv", index=False)
    print(all)
    print("++++++++++++++++++++++++++++++++++")


    # -------------------------------------------------------------------------
    # Export Plot-Ready Data for Venn Diagrams
    # -------------------------------------------------------------------------
    # Demonstration 3: Get data formatted specifically for Venn diagram plotting
    #
    # Key Points:
    # - get_plot_data() automatically ensures min_size=0 for complete data
    # - For single-set regions (n_sets=1), returns exclusive elements instead 
    #   of all elements (correct for Venn diagram labeling)
    # - For multi-set regions (n_sets>1), returns the intersection data
    # - Output file: plotdata_overlaps.csv (columns: set_names, n_sets, size, elements)
    #
    # Note: Exclusive elements for single sets ensure Venn diagrams show 
    #       region-specific elements correctly (e.g., the part of Set1 that 
    #       doesn't overlap with any other set)
    # -------------------------------------------------------------------------
    print("+++++++++++++++getPlot data+++++++++++++++++++")
    all = calc.get_plot_data()
    all.to_csv("plotdata_overlaps.csv", index=False)
    print(all)
    print("++++++++++++++++++++++++++++++++++")

    
    # -------------------------------------------------------------------------
    # Compute Non-empty Overlaps Only
    # -------------------------------------------------------------------------
    # Demonstration 4: Filter out empty intersections for cleaner output
    #
    # Key Points:
    # - min_size=1 excludes combinations with size=0
    # - Useful for focusing on actual overlaps rather than theoretical possibilities
    # - Reduces output size from 127 to only combinations with shared elements
    # -------------------------------------------------------------------------
    print("\n=== Non-empty Overlaps Only ===")
    df_non_empty = calc.compute(min_size=1)  # Only non-empty intersections
    print(df_non_empty[['set_names', 'size', 'elements']])
    
    # -------------------------------------------------------------------------
    # Compute Exclusive Elements for Each Set
    # -------------------------------------------------------------------------
    # Demonstration 5: Identify elements unique to each set
    #
    # Key Points:
    # - Exclusive elements appear in only ONE set and nowhere else
    # - This helps identify set-specific features (e.g., genes unique to a condition)
    # - overlap_size = total_size - exclusive_size (elements shared with other sets)
    # - Results are cached for future access
    #
    # Output columns:
    # - set: name of the set
    # - total_size: total number of elements in the set
    # - exclusive_size: count of elements only in this set
    # - exclusive_elements: list of exclusive elements (sorted)
    # - overlap_size: elements shared with other sets
    # -------------------------------------------------------------------------
    print("\n=== Exclusive Elements ===")
    exclusive_df = calc.compute_exclusive()
    print(exclusive_df[['set', 'total_size', 'exclusive_size', 'overlap_size']])
    
    # -------------------------------------------------------------------------
    # Generate Pairwise Overlap Matrix
    # -------------------------------------------------------------------------
    # Demonstration 6: Analyze pairwise relationships between all sets
    #
    # Key Points:
    # - Creates a symmetric matrix showing intersection counts for all set pairs
    # - Diagonal elements show set sizes (intersection of a set with itself)
    # - Off-diagonal elements show shared elements between two sets
    # - Matrix is symmetric (intersection of A & B = intersection of B & A)
    #
    # Example interpretation:
    # - Row "Set1", Column "Set2" = number of elements in both Set1 and Set2
    # - Row "Set1", Column "Set1" = total elements in Set1
    # -------------------------------------------------------------------------
    print("\n=== Pairwise Overlap Matrix ===")
    matrices = calc.get_pairwise_overlap()
    print(matrices['overlap_matrix'])
    
    # -------------------------------------------------------------------------
    # Generate Jaccard Similarity Matrix
    # -------------------------------------------------------------------------
    # Demonstration 7: Quantify similarity between sets using Jaccard coefficient
    #
    # Key Points:
    # - Jaccard(A, B) = |A ∩ B| / |A ∪ B|
    # - Values range from 0.0 (no overlap) to 1.0 (identical sets)
    # - Accounts for both intersection and union sizes
    # - More informative than raw overlap counts when sets have different sizes
    #
    # Example interpretation:
    # - 0.0 = disjoint sets (no shared elements)
    # - 0.5 = 50% overlap (half the elements are shared)
    # - 1.0 = identical sets
    # -------------------------------------------------------------------------
    print("\n=== Jaccard Similarity Matrix ===")
    print(matrices['jaccard_matrix'].round(3))
    
    # -------------------------------------------------------------------------
    # Generate Comprehensive Summary Statistics
    # -------------------------------------------------------------------------
    # Demonstration 8: Get a high-level overview of the entire overlap analysis
    #
    # Key Points:
    # - Provides quick insights without examining full results
    # - Useful for reporting and understanding data structure
    # - Based on cached results from the most recent compute() call
    #
    # Summary includes:
    # - n_sets: total number of input sets (7 in this example)
    # - set_names: list of all set identifiers
    # - set_sizes: dictionary mapping each set to its total element count
    # - total_unique_elements: size of the union of all sets
    # - all_common_size: number of elements present in ALL sets
    # - max_overlap_size: largest intersection found across all combinations
    # - max_overlap_sets: which set combination has the maximum overlap
    # - all_overlaps: complete list of overlap dictionaries
    # - n_combinations: total number of combinations from last compute()
    # - empty_combinations: count of intersections with size=0
    # - non_empty_combinations: count of intersections with size>0
    # -------------------------------------------------------------------------
    print("\n=== Summary Information ===")
    summary = calc.get_summary()
    print(f"Number of sets: {summary['n_sets']}")
    print(f"Set names: {summary['set_names']}")
    print(f"Set sizes: {summary['set_sizes']}")
    print(f"Total unique elements: {summary['total_unique_elements']}")
    print(f"Elements common to all sets: {summary['all_common_size']}")
    print(f"Maximum overlap size: {summary['max_overlap_size']}")
    print(f"Maximum overlap sets: {summary['max_overlap_sets']}")
    print(f"\nAll overlaps (first 3): {summary['all_overlaps'][:3]}")
    
    # -------------------------------------------------------------------------
    # Query Specific Set Combination
    # -------------------------------------------------------------------------
    # Demonstration 9: Analyze a specific combination of sets in detail
    #
    # Key Points:
    # - Query elements shared by specific sets (Set1, Set2, Set3 in this case)
    # - Returns both intersection and exclusive elements
    # - Exclusive elements: in the intersection but NOT in any other sets
    # - Useful for focused analysis of specific hypotheses or conditions
    #
    # Return values:
    # - sets: tuple of queried set names (for identification)
    # - set_names: human-readable string representation
    # - n_sets: number of sets in this combination
    # - size: intersection size
    # - elements: sorted list of intersecting elements
    # - exclusive_size: count of elements exclusive to this combination
    # - exclusive_elements: sorted list of exclusive elements
    #
    # Example: query_elements(['Set1', 'Set2', 'Set3']) returns information
    # about elements present in ALL of Set1, Set2, and Set3
    # -------------------------------------------------------------------------
    print("\n=== Query Specific Sets ===")
    result = calc.query_elements(['Set1', 'Set2', 'Set3'])
    print(f"SetA & SetB & SetC elements: {result['elements']}")
    print(f"Full overlap info:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    # -------------------------------------------------------------------------
    # Display All Non-empty Combinations
    # -------------------------------------------------------------------------
    # Demonstration 10: Iterate through all combinations and display meaningful overlaps
    #
    # Key Points:
    # - all_results contains all 2^n - 1 combinations (including empty ones)
    # - Filtering by combo['size'] > 0 shows only combinations with actual overlaps
    # - Useful for quickly identifying which combinations share elements
    # - Enumeration (i+1) provides easy reference for each overlap
    #
    # Note: This demonstrates the programmatic access to query_elements() results,
    #       which can be used for custom filtering, reporting, or visualization
    # -------------------------------------------------------------------------
    print(f"Total overlap combinations: {len(all_results)}")
    print(f"All combinations with elements:")
    for i, combo in enumerate(all_results):
        if combo['size'] > 0:  # Only show non-empty overlaps
            print(f"  {i+1}. {combo['set_names']}: {combo['elements']} (size: {combo['size']})")

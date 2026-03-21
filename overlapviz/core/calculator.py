"""
OverlapCalculator - Set Overlap Analysis Tool

This module provides a comprehensive class for analyzing overlaps between
multiple sets. It supports various input formats and provides detailed
statistics about set intersections, exclusive elements, and pairwise relationships.

Author: Dot4diw
Version: 1.0
"""

import pandas as pd
from typing import List, Set, Dict, Tuple, Any, Optional, Union
from itertools import combinations


class OverlapCalculator:
    """
    Calculate all overlap situations for n sets
    
    Supports three input formats:
    1. Dictionary: {'Set1': {"g1","g2","g3"}, 'Set2': {"g2","g3","g4"}}
    2. List of sets: [{"g1","g2","g3"}, {"g2","g3","g4"}]
    3. List of tuples: [('Set1', {"g1","g2","g3"}), ('Set2', {"g2","g3","g4"})]
    
    Key mathematical principle:
    - For n sets, there are 2^n - 1 non-empty subsets/combinations
    - Each combination represents a unique intersection region
    """
    
    DEFAULT_MIN_SIZE = 1
    
    def __init__(self, data: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]):
        """
        Initialize the OverlapCalculator with input data
        
        Parameters
        ----------
        data : dict, list, or list of tuples
            Input set data in one of the supported formats:
            - Dictionary mapping set names to sets (recommended)
            - List of sets (auto-named as Set1, Set2, Set3, etc.)
            - List of tuples: (set_name, set_elements) for explicit naming
        """
        self.sets_names: List[str] = []
        self.sets_list: List[Set] = []
        self._results_df: Optional[pd.DataFrame] = None
        self._exclusive_results: Optional[pd.DataFrame] = None
        
        self._parse_input(data)
        self._validate_data()
    
    def _parse_input(self, data: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]) -> None:
        """Parse input data from various supported formats into standardized internal representation"""
        if isinstance(data, dict):
            self.sets_names = list(data.keys())
            self.sets_list = [set(v) for v in data.values()]
        elif isinstance(data, list):
            if len(data) == 0:
                raise ValueError("Input data cannot be empty")
            
            if isinstance(data[0], tuple) and len(data[0]) == 2:
                self.sets_names = [item[0] for item in data]
                self.sets_list = [set(item[1]) for item in data]
            else:
                self.sets_names = [f"Set{i+1}" for i in range(len(data))]
                self.sets_list = [set(s) for s in data]
        else:
            raise TypeError(f"Unsupported input type: {type(data)}. "
                          f"Expected dict, list of sets, or list of tuples.")
    
    def _validate_data(self) -> None:
        """Validate the parsed data to ensure it meets requirements"""
        if len(self.sets_list) != len(self.sets_names):
            raise ValueError("Number of set names and sets do not match")
        
        if len(self.sets_list) == 0:
            raise ValueError("At least one set must be provided")
        
        if len(self.sets_names) != len(set(self.sets_names)):
            raise ValueError("Set names must be unique - duplicates found")
    
    def compute(self, min_size: int = 0, max_size: Optional[int] = None) -> pd.DataFrame:
        """
        Compute all overlaps between sets and return as DataFrame
        
        Generates all 2^n - 1 non-empty combinations of sets, computes their
        intersections, and filters based on size criteria.
        
        Parameters
        ----------
        min_size : int, default 0
            Minimum overlap size threshold. Set to 0 to include empty intersections.
        max_size : int, optional
            Maximum overlap size threshold.
            
        Returns
        -------
        pd.DataFrame
            DataFrame with columns: sets, set_names, n_sets, size, elements,
            exclusive_size, exclusive_elements
        """
        results = []
        n = len(self.sets_list)
        
        for r in range(1, n + 1):
            for idxs in combinations(range(n), r):
                intersect_set = set.intersection(*[self.sets_list[i] for i in idxs])
                
                if len(intersect_set) < min_size:
                    continue
                if max_size is not None and len(intersect_set) > max_size:
                    continue
                
                set_names = tuple(self.sets_names[i] for i in idxs)
                
                if intersect_set and r < n:
                    other_sets = [self.sets_list[i] for i in range(n) if i not in idxs]
                    union_others = set.union(*other_sets) if other_sets else set()
                    exclusive_set = intersect_set - union_others
                else:
                    exclusive_set = set() if not intersect_set else intersect_set
                
                results.append({
                    "sets": set_names,
                    "set_names": " & ".join(set_names),
                    "n_sets": r,
                    "size": len(intersect_set),
                    "elements": sorted(intersect_set),
                    "exclusive_size": len(exclusive_set),
                    "exclusive_elements": sorted(exclusive_set)
                })
        
        self._results_df = pd.DataFrame(results)
        
        if not self._results_df.empty:
            self._results_df = self._results_df.sort_values(
                ['n_sets', 'size'], 
                ascending=[False, False]
            ).reset_index(drop=True)
        
        return self._results_df
    
    def compute_exclusive(self) -> pd.DataFrame:
        """
        Compute exclusive elements for each individual set
        
        Exclusive elements are those that belong to only ONE set.
        Exclusive(A) = A - (B ∪ C ∪ D ∪ ...) for sets A, B, C, D, ...
        
        Returns
        -------
        pd.DataFrame
            DataFrame with columns: set, total_size, exclusive_size,
            exclusive_elements, overlap_size
        """
        results = []
        n = len(self.sets_list)
        
        for i in range(n):
            current_set = self.sets_list[i]
            other_sets = [self.sets_list[j] for j in range(n) if j != i]
            union_others = set.union(*other_sets) if other_sets else set()
            exclusive = current_set - union_others
            
            results.append({
                "set": self.sets_names[i],
                "total_size": len(current_set),
                "exclusive_size": len(exclusive),
                "exclusive_elements": sorted(exclusive),
                "overlap_size": len(current_set) - len(exclusive)
            })
        
        self._exclusive_results = pd.DataFrame(results)
        return self._exclusive_results
    
    def get_pairwise_overlap(self) -> Dict[str, pd.DataFrame]:
        """
        Generate pairwise overlap and Jaccard similarity matrices
        
        Jaccard Similarity: J(A, B) = |A ∩ B| / |A ∪ B|
        - 0.0 = no overlap, 1.0 = identical sets
        
        Returns
        -------
        dict
            Dictionary containing 'overlap_matrix' and 'jaccard_matrix'
        """
        n = len(self.sets_names)
        
        overlap_matrix = pd.DataFrame(0, index=self.sets_names, columns=self.sets_names)
        jaccard_matrix = pd.DataFrame(0.0, index=self.sets_names, columns=self.sets_names)
        
        for i in range(n):
            for j in range(i, n):
                set_i = self.sets_list[i]
                set_j = self.sets_list[j]
                
                intersection = len(set_i & set_j)
                union = len(set_i | set_j)
                
                overlap_matrix.iloc[i, j] = intersection
                overlap_matrix.iloc[j, i] = intersection
                
                jaccard = intersection / union if union > 0 else 0.0
                jaccard_matrix.iloc[i, j] = jaccard
                jaccard_matrix.iloc[j, i] = jaccard
        
        return {
            'overlap_matrix': overlap_matrix,
            'jaccard_matrix': jaccard_matrix
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics of all set overlaps
        
        Returns
        -------
        dict
            Dictionary containing n_sets, set_names, set_sizes, total_unique_elements,
            all_common_size, max_overlap_size, max_overlap_sets, all_overlaps,
            n_combinations, empty_combinations, non_empty_combinations
        """
        if self._results_df is None:
            self.compute()
        
        summary = {
            'n_sets': len(self.sets_list),
            'set_names': self.sets_names,
            'set_sizes': {
                name: len(s) 
                for name, s in zip(self.sets_names, self.sets_list)
            },
            'total_unique_elements': len(set.union(*self.sets_list)),
        }
        
        all_common = self._results_df[
            self._results_df['n_sets'] == len(self.sets_list)
        ]
        summary['all_common_size'] = all_common['size'].iloc[0] if not all_common.empty else 0
        
        summary['max_overlap_size'] = self._results_df['size'].max()
        summary['max_overlap_sets'] = self._results_df.loc[
            self._results_df['size'].idxmax(), 'sets'
        ]
        
        summary['all_overlaps'] = self._results_df.to_dict('records')
        summary['n_combinations'] = len(self._results_df)
        summary['empty_combinations'] = len(self._results_df[self._results_df['size'] == 0])
        summary['non_empty_combinations'] = len(self._results_df[self._results_df['size'] > 0])
        
        return summary
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the computed overlap results as a DataFrame
        
        Returns
        -------
        pd.DataFrame
            DataFrame containing overlap computation results
        """
        if self._results_df is None:
            self.compute()
        return self._results_df
    
    def get_plot_data(self) -> pd.DataFrame:
        """
        Get DataFrame formatted for Venn diagram plotting
        
        For single-set regions (n_sets == 1), shows exclusive elements.
        For multi-set regions (n_sets > 1), shows intersection values.
        
        Returns
        -------
        pd.DataFrame
            DataFrame with columns: set_names, n_sets, size, elements
        """
        if self._results_df is None:
            self.compute(min_size=0)
        
        #plot_df = self._results_df[['set_names', 'n_sets', 'size', 'elements', 'exclusive_size', 'exclusive_elements']].copy()
        plot_df = self._results_df[['set_names', 'n_sets', 'exclusive_size', 'exclusive_elements']].copy()

        
        # single_set_mask = plot_df['n_sets'] == 1
        # plot_df.loc[single_set_mask, 'size'] = plot_df.loc[single_set_mask, 'exclusive_size']
        # plot_df.loc[single_set_mask, 'elements'] = plot_df.loc[single_set_mask, 'exclusive_elements']
        
        # plot_df['size'] = plot_df['exclusive_size']#   - Cached to avoid redundant computation
        # plot_df['elements'] = plot_df['exclusive_elements']#   - Cached to avoid redundant computation
        
        # plot_df = plot_df.drop(columns=['exclusive_size', 'exclusive_elements'])
        plot_df = plot_df.rename(columns={
            'exclusive_size': 'size',
            'exclusive_elements': 'elements'
            })
        
        return plot_df
    
    def query_elements(self, query_sets: Optional[List[str]] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Query overlap information for specific set combinations
        
        Parameters
        ----------
        query_sets : list of str, optional
            List of set names to query. If None, returns all combinations.
            
        Returns
        -------
        dict or list of dict
            Single dict if query_sets provided, list of dicts otherwise
        """
        if query_sets is None:
            results = []
            n = len(self.sets_list)
            
            for r in range(1, n + 1):
                for idxs in combinations(range(n), r):
                    intersect_set = set.intersection(*[self.sets_list[i] for i in idxs])
                    set_names = tuple(self.sets_names[i] for i in idxs)
                    
                    if intersect_set and r < n:
                        other_sets = [self.sets_list[i] for i in range(n) if i not in idxs]
                        union_others = set.union(*other_sets) if other_sets else set()
                        exclusive_set = intersect_set - union_others
                    else:
                        exclusive_set = set()
                    
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
        
        for name in query_sets:
            if name not in self.sets_names:
                raise ValueError(f"Unknown set name: '{name}'. "
                               f"Available sets: {self.sets_names}")
        
        idxs = [self.sets_names.index(name) for name in query_sets]
        intersect_set = set.intersection(*[self.sets_list[i] for i in idxs])
        
        n = len(self.sets_list)
        r = len(idxs)
        if r < n:
            other_sets = [self.sets_list[i] for i in range(n) if i not in idxs]
            union_others = set.union(*other_sets) if other_sets else set()
            exclusive_set = intersect_set - union_others
        else:
            exclusive_set = intersect_set
        
        return {
            'sets': tuple(query_sets),
            'set_names': " & ".join(query_sets),
            'n_sets': r,
            'size': len(intersect_set),
            'elements': sorted(intersect_set),
            'exclusive_size': len(exclusive_set),
            'exclusive_elements': sorted(exclusive_set)
        }
    
    def __repr__(self) -> str:
        """String representation of the calculator instance"""
        return f"OverlapCalculator(n_sets={len(self.sets_list)}, sets={self.sets_names})"


if __name__ == "__main__":
    data_dict = {
        'Set1': {"g1", "g2", "g3", "g4", "g5"},
        'Set2': {"g2", "g3", "g4", "g6", "g7"},
        'Set3': {"g3", "g4", "g5", "g7", "g8"},
        'Set4': {"g4", "g5", "g6", "g8", "g9"},
        'Set5': {"g5", "g6", "g7", "g9", "g10"},
        'Set6': {"g6", "g7", "g8", "g9", "g10"},
        'Set7': {"g7", "g8", "g9", "g10", "g11"}
    }
    
    calc = OverlapCalculator(data_dict)
    
    print("=== All Overlap Situations (including empty) ===")
    df = calc.compute(min_size=0)
    print(f"Total combinations (2^n - 1): {len(df)}")
    print(df[['set_names', 'size', 'elements']])

    print("\n=== Query All Possible Combinations ===")
    all_results = calc.query_elements()
    print("++++++++++++++++++++++++++++++++++")
    all = calc.get_dataframe()
    all.to_csv("all_overlaps.csv", index=False)
    print(all)
    print("++++++++++++++++++++++++++++++++++")

    print("+++++++++++++++getPlot data+++++++++++++++++++")
    all = calc.get_plot_data()
    all.to_csv("plotdata_overlaps.csv", index=False)
    print(all)
    print("++++++++++++++++++++++++++++++++++")
    
    print("\n=== Non-empty Overlaps Only ===")
    df_non_empty = calc.compute(min_size=1)
    print(df_non_empty[['set_names', 'size', 'elements']])
    
    print("\n=== Exclusive Elements ===")
    exclusive_df = calc.compute_exclusive()
    print(exclusive_df[['set', 'total_size', 'exclusive_size', 'overlap_size']])
    
    print("\n=== Pairwise Overlap Matrix ===")
    matrices = calc.get_pairwise_overlap()
    print(matrices['overlap_matrix'])
    
    print("\n=== Jaccard Similarity Matrix ===")
    print(matrices['jaccard_matrix'].round(3))
    
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
    
    print("\n=== Query Specific Sets ===")
    result = calc.query_elements(['Set1', 'Set2', 'Set3'])
    print(f"SetA & SetB & SetC elements: {result['elements']}")
    print(f"Full overlap info:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    print(f"\nTotal overlap combinations: {len(all_results)}")
    print(f"All combinations with elements:")
    for i, combo in enumerate(all_results):
        if combo['size'] > 0:
            print(f"  {i+1}. {combo['set_names']}: {combo['elements']} (size: {combo['size']})")

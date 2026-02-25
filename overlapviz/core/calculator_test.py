import sys
import pandas as pd

# Import the OverlapCalculator class
# Adjust the import path as needed
try:
    from calculator import OverlapCalculator
except ImportError:
    print("Error: Cannot import OverlapCalculator. Ensure caculated.py is in the same directory.")
    sys.exit(1)

if __name__ == "__main__":
    # -------------------------------------------------------------------------
    # Step 1: Create Sample Data
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
    # Step 2: Initialize the Calculator
    # -------------------------------------------------------------------------
    # Create an OverlapCalculator instance with the data
    # The constructor automatically parses and validates the input data
    # 
    # Expected output from print(calc): 
    # OverlapCalculator(n_sets=7, sets=['Set1', 'Set2', 'Set3', 'Set4', 'Set5', 'Set6', 'Set7'])
    # -------------------------------------------------------------------------
    calc = OverlapCalculator(data_dict)
    
    # -------------------------------------------------------------------------
    # Step 3: Compute All Overlaps (Including Empty Intersections)
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
    # Step 4: Export Complete Overlap Results to CSV
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
    # Step 5: Export Plot-Ready Data for Venn Diagrams
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
    # Step 6: Compute Non-empty Overlaps Only
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
    # Step 7: Compute Exclusive Elements for Each Set
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
    # Step 8: Generate Pairwise Overlap Matrix
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
    # Step 9: Generate Jaccard Similarity Matrix
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
    # Step 10: Generate Comprehensive Summary Statistics
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
    # Step 11: Query Specific Set Combination
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
    # Step 12: Display All Non-empty Combinations
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


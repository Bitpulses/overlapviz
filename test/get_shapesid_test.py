"""Test VennPlot.get_shapes() method
Get all available shape IDs for specified number of sets
"""

import sys
import os
#sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from overlapviz.venn import VennPlot

def test_get_shapes():
    """Test getting shapes for different number of sets"""
    print("=" * 60)
    print("Testing VennPlot.get_shapes() method")
    print("=" * 60)

    # Test 2-7 sets
    for n_sets in range(2, 8):
        shapes = VennPlot.get_shapes(n_sets)
        print(f"\nAvailable shapes for {n_sets} sets:")
        if shapes:
            for shape_id in shapes:
                print(f"  - {shape_id}")
        else:
            print("  (No available shapes)")

    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


def test_get_shapes_with_details():
    """Test getting shapes and displaying detailed information"""
    print("\n" + "=" * 60)
    print("Testing getting shapes with detailed information")
    print("=" * 60)

    import pickle
    from pathlib import Path

    # Get pkl file path
    current_dir = Path(__file__).parent.parent / 'overlapviz' / 'venn'
    filepath = current_dir / 'geometric_data_v3.pkl'

    with open(filepath, 'rb') as f:
        data = pickle.load(f)

    for n_sets in range(2, 8):
        shapes = VennPlot.get_shapes(n_sets)
        if shapes:
            print(f"\n{n_sets} sets:")
            for shape_id in shapes:
                shape_data = data[shape_id]
                shape_type = shape_data.get('type', 'unknown')
                print(f"  - {shape_id} (Type: {shape_type})")


if __name__ == '__main__':
    test_get_shapes()
    test_get_shapes_with_details()

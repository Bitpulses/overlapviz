#!/usr/bin/env python3
"""
Test script to verify overlapviz installation
"""

def test_imports():
    """Test basic imports"""
    try:
        import overlapviz
        print("✓ Successfully imported overlapviz")
        
        # Test version
        print(f"  Version: {overlapviz.__version__}")
        print(f"  Author: {overlapviz.__author__}")
        print(f"  Exported: {overlapviz.__all__}")
        
        # Test core imports
        from overlapviz import VennPlot, PlotStyle, BasePlot
        print("✓ Successfully imported VennPlot, PlotStyle, BasePlot")
        
        # Test submodule imports
        from overlapviz.core import OverlapCalculator
        print("✓ Successfully imported OverlapCalculator")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    try:
        from overlapviz import VennPlot, PlotStyle
        
        # Test creating objects
        venn = VennPlot()
        style = PlotStyle()
        print("✓ Successfully created VennPlot and PlotStyle instances")
        
        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing overlapviz installation...")
    print("=" * 60)
    
    success = True
    success &= test_imports()
    print()
    success &= test_basic_functionality()
    
    print("=" * 60)
    if success:
        print("✓ All tests passed! Installation successful.")
    else:
        print("✗ Some tests failed. Please check the installation.")

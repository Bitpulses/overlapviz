"""
测试 OverlapCalculator 的交集计算逻辑是否正确
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from overlapviz.core.calculator import OverlapCalculator

def test_basic_intersection():
    """测试基本交集计算"""
    print("=" * 60)
    print("测试1: 基本交集计算")
    print("=" * 60)
    
    # 创建3个集合
    A = {1, 2, 3, 4, 5}
    B = {2, 3, 4, 5, 6}
    C = {3, 4, 5, 6, 7}
    
    data = {'A': A, 'B': B, 'C': C}
    calc = OverlapCalculator(data)
    df = calc.compute(min_size=0)
    
    print("\n原始集合:")
    print(f"A = {sorted(A)}")
    print(f"B = {sorted(B)}")
    print(f"C = {sorted(C)}")
    
    print("\n计算结果:")
    for _, row in df.iterrows():
        print(f"{row['set_names']:20s} | size: {row['size']:2d} | elements: {row['elements']}")
        print(f"{'':20s} | exclusive_size: {row['exclusive_size']:2d} | exclusive: {row['exclusive_elements']}")
    
    # 手动验证几个关键结果
    print("\n手动验证:")
    print(f"A ∩ B = {sorted(A & B)}")  # 应该是 {2, 3, 4, 5}
    print(f"A ∩ B ∩ C = {sorted(A & B & C)}")  # 应该是 {3, 4, 5}
    
    # 验证独占元素
    print(f"\nA only (A - B - C) = {sorted(A - B - C)}")  # 应该是 {1}
    print(f"A ∩ B only ((A ∩ B) - C) = {sorted((A & B) - C)}")  # 应该是 {2}
    print(f"A ∩ B ∩ C = {sorted(A & B & C)}")  # 应该是 {3, 4, 5}

def test_exclusive_elements():
    """测试独占元素计算"""
    print("\n" + "=" * 60)
    print("测试2: 独占元素计算")
    print("=" * 60)
    
    # 创建4个集合，有明确的独占区域
    A = {1, 2, 3, 4}
    B = {3, 4, 5, 6}
    C = {5, 6, 7, 8}
    D = {7, 8, 9, 10}
    
    data = {'A': A, 'B': B, 'C': C, 'D': D}
    calc = OverlapCalculator(data)
    df = calc.compute(min_size=0)
    
    print("\n原始集合:")
    print(f"A = {sorted(A)}")
    print(f"B = {sorted(B)}")
    print(f"C = {sorted(C)}")
    print(f"D = {sorted(D)}")
    
    print("\n所有交集和独占元素:")
    for _, row in df.iterrows():
        if row['size'] > 0:  # 只显示非空交集
            print(f"{row['set_names']:20s} | size: {row['size']:2d} | elements: {row['elements']}")
            print(f"{'':20s} | exclusive: {row['exclusive_elements']}")
    
    # 验证关键独占元素
    print("\n验证独占元素:")
    print(f"A only = {sorted(A - B - C - D)}")  # 应该是 {1, 2}
    print(f"A ∩ B only = {sorted((A & B) - C - D)}")  # 应该是 {3, 4}
    print(f"B ∩ C only = {sorted((B & C) - A - D)}")  # 应该是 {5, 6}
    print(f"C ∩ D only = {sorted((C & D) - A - B)}")  # 应该是 {7, 8}
    print(f"D only = {sorted(D - A - B - C)}")  # 应该是 {9, 10}

def test_all_combinations():
    """测试所有组合是否都被计算"""
    print("\n" + "=" * 60)
    print("测试3: 所有组合是否都被计算")
    print("=" * 60)
    
    # 对于n个集合，应该有 2^n - 1 个组合
    for n in range(2, 6):
        data = {f'Set{i+1}': set(range(i*10, i*10+5)) for i in range(n)}
        calc = OverlapCalculator(data)
        df = calc.compute(min_size=0)
        
        expected = 2**n - 1
        actual = len(df)
        
        print(f"n={n} 个集合: 期望 {expected} 个组合, 实际 {actual} 个组合", end="")
        if expected == actual:
            print(" ✓")
        else:
            print(" ✗ 错误!")

def test_empty_intersections():
    """测试空交集的处理"""
    print("\n" + "=" * 60)
    print("测试4: 空交集的处理")
    print("=" * 60)
    
    # 创建没有交集的集合
    A = {1, 2, 3}
    B = {4, 5, 6}
    C = {7, 8, 9}
    
    data = {'A': A, 'B': B, 'C': C}
    calc = OverlapCalculator(data)
    
    # 包含空交集
    df_with_empty = calc.compute(min_size=0)
    print(f"\n包含空交集 (min_size=0): {len(df_with_empty)} 个组合")
    
    # 不包含空交集
    df_no_empty = calc.compute(min_size=1)
    print(f"不包含空交集 (min_size=1): {len(df_no_empty)} 个组合")
    
    print("\n非空交集:")
    for _, row in df_no_empty.iterrows():
        print(f"{row['set_names']:10s} | size: {row['size']} | elements: {row['elements']}")

def test_complex_scenario():
    """测试复杂场景"""
    print("\n" + "=" * 60)
    print("测试5: 复杂场景 - 4个集合的多重重叠")
    print("=" * 60)
    
    # 创建一个复杂的重叠场景
    A = {1, 2, 3, 4, 5, 6, 7, 8}
    B = {2, 3, 4, 5, 6, 7, 8, 9}
    C = {3, 4, 5, 6, 7, 8, 9, 10}
    D = {4, 5, 6, 7, 8, 9, 10, 11}
    
    data = {'A': A, 'B': B, 'C': C, 'D': D}
    calc = OverlapCalculator(data)
    df = calc.compute(min_size=0)
    
    print("\n原始集合:")
    print(f"A = {sorted(A)}")
    print(f"B = {sorted(B)}")
    print(f"C = {sorted(C)}")
    print(f"D = {sorted(D)}")
    
    print("\n所有非空交集:")
    for _, row in df.iterrows():
        if row['size'] > 0:
            print(f"{row['set_names']:25s} | size: {row['size']:2d} | exclusive: {row['exclusive_elements']}")
    
    # 验证几个关键结果
    print("\n手动验证关键交集:")
    print(f"A ∩ B ∩ C ∩ D = {sorted(A & B & C & D)}")  # 应该是 {4, 5, 6, 7, 8}
    print(f"独占元素 = {sorted((A & B & C & D) - (A & B & C & D))}")  # 应该是 {4, 5, 6, 7, 8}（因为所有集合都参与了）

if __name__ == '__main__':
    test_basic_intersection()
    test_exclusive_elements()
    test_all_combinations()
    test_empty_intersections()
    test_complex_scenario()
    
    print("\n" + "=" * 60)
    print("所有测试完成!")
    print("=" * 60)

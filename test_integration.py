#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试：验证 step_mutlcheck 函数的递归处理能力
"""

import json
from parse_package import PackageParser

def test_integration():
    """测试集成解析"""
    
    print("=" * 60)
    print("集成测试：Package.pkg 解析")
    print("=" * 60)
    
    # 使用独立的解析器
    parser = PackageParser()
    result = parser.parse_file("Package.pkg")
    
    # 验证 TsMultiCheck 的解析结果
    multichheck_steps = [step for step in result if step["type"] == "utility-2fb63e30-6816-11e5-bfd3-4851b798ee63"]
    
    print(f"\n找到 {len(multichheck_steps)} 个 TsMultiCheck 步骤")
    
    for i, step in enumerate(multichheck_steps, 1):
        print(f"\n--- TsMultiCheck #{i} ---")
        print(f"ID: {step['id']}")
        print(f"MatchAll: {step.get('matchall', 'N/A')}")
        print(f"Time Option: {json.dumps(step.get('time_option'), ensure_ascii=False, indent=2)}")
        print(f"Children Count: {len(step.get('children', []))}")
        
        if step.get('children'):
            for j, child in enumerate(step['children'], 1):
                print(f"  Child #{j}: {child['name']} ({child['type']})")
                if child.get('expectation'):
                    print(f"    Expectation: {child['expectation']}")
    
    # 验证关键属性
    print("\n" + "=" * 60)
    print("验证关键属性")
    print("=" * 60)
    
    for step in multichheck_steps:
        assert 'matchall' in step, f"Missing matchall in {step['id']}"
        assert 'time_option' in step, f"Missing time_option in {step['id']}"
        assert 'children' in step, f"Missing children in {step['id']}"
        assert len(step['children']) > 0, f"No children in {step['id']}"
        
        # 验证子步骤的 parent_id
        for child in step['children']:
            assert child['parent_id'] == step['id'], f"Wrong parent_id in child {child['id']}"
    
    print("所有验证通过！")
    
    # 保存测试结果
    with open("test_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"\n测试结果已保存到 test_result.json")

if __name__ == "__main__":
    test_integration()
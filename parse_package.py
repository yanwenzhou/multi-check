#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package.pkg 解析器
将 Package.pkg XML 文件解析为 JSON 结构
"""

import xml.etree.ElementTree as ET
import json
from typing import Any, Dict, List, Optional

# XML 命名空间
ns = {"ns": "http://www.tracetronic.de/xml/ecu-test", "xsi": "http://www.w3.org/2001/XMLSchema-instance"}


class ValueExpression:
    """值表达式解析器"""
    
    @staticmethod
    def parse_value_expression(elem):
        """解析值表达式"""
        if elem is None:
            return None
        
        xsi_type = elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        
        if xsi_type == "integer":
            return int(elem.text) if elem.text else 0
        elif xsi_type == "string":
            return elem.text or ""
        elif xsi_type == "boolean":
            return elem.text.lower() == "true" if elem.text else False
        elif xsi_type == "undefined":
            return None
        else:
            # 对于复杂类型，返回类型和文本
            return {
                "type": xsi_type,
                "value": elem.text if elem.text else ""
            }
    
    @staticmethod
    def parse_i18n_item(elem):
        """解析国际化文本"""
        if elem is None:
            return None
        
        result = {}
        multilang = elem.find("./ns:MULTILANGDATA", namespaces=ns)
        if multilang is not None:
            elements = multilang.findall("./ns:ELEMENT", namespaces=ns)
            for el in elements:
                dkey = el.get("dkey")
                dvalue_elem = el.find("./ns:DVALUE", namespaces=ns)
                if dvalue_elem is not None:
                    result[dkey] = ValueExpression.parse_value_expression(dvalue_elem)
        
        lang_elem = elem.find("./ns:INITIAL-LANGUAGE", namespaces=ns)
        if lang_elem is not None:
            result["initial_language"] = lang_elem.text
        
        return result
    
    @staticmethod
    def parse_expression(elem):
        """解析表达式"""
        if elem is None:
            return None
        
        xsi_type = elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        result = {"type": xsi_type}
        
        # 手动表达式
        if xsi_type == "manualExpression":
            base_expr = elem.find("./ns:BASE-EXPRESSION", namespaces=ns)
            if base_expr is not None:
                base_type = base_expr.get("{http://www.w3.org/2001/XMLSchema-instance}type")
                if base_type == "varBaseExpression":
                    name_elem = base_expr.find("./ns:NAME", namespaces=ns)
                    if name_elem is not None:
                        result["variable"] = name_elem.text
        
        # 内置数值表达式
        elif xsi_type == "builtNumericExpression":
            rel_elem = elem.find("./ns:RELATION", namespaces=ns)
            val_elem = elem.find("./ns:VALUE", namespaces=ns)
            if rel_elem is not None:
                result["relation"] = rel_elem.text
            if val_elem is not None:
                result["value"] = ValueExpression.parse_value_expression(val_elem)
        
        return result
    
    @staticmethod
    def parse_time_option(elem):
        """解析TIME-OPTION"""
        if elem is None:
            return None
        
        result = {"type": elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")}
        expr_elem = elem.find("./ns:EXPRESSION", namespaces=ns)
        if expr_elem is not None:
            result["expression"] = ValueExpression.parse_expression(expr_elem)
        
        return result


class TestStep:
    """测试步骤类"""
    
    def __init__(self):
        self.id = None
        self.parent_id = None
        self.name = None
        self.type = None
        self.breakpoint = False
        self.enable = True
        self.children = []
        
        # 特定步骤的属性
        self.action = None  # TsBlock
        self.formula = None  # TsCalculation
        self.expectation = None  # TsCalculation
        self.matchall = None  # TsMultiCheck
        self.time_option = None  # TsMultiCheck
        self.time = None  # TsWait
        self.unit = None  # TsWait
        self.comment = None  # TsComment
        self.return_value = None  # TsReturn
        self.condition = None  # TsIf
        self.then_branch = None  # TsIf
        self.else_branch = None  # TsIf
        self.loop_type = None  # TsLoop
        self.loop_count = None  # TsLoop
        self.loop_condition = None  # TsLoop
    
    def to_dict(self):
        """转换为字典"""
        result = {
            "id": self.id,
            "parent_id": self.parent_id,
            "name": self.name,
            "type": self.type,
            "breakpoint": self.breakpoint,
            "enable": self.enable,
        }
        
        # 添加特定属性
        if self.action is not None:
            result["action"] = self.action
        if self.formula is not None:
            result["formula"] = self.formula
        if self.expectation is not None:
            result["expectation"] = self.expectation
        if self.matchall is not None:
            result["matchall"] = self.matchall
        if self.time_option is not None:
            result["time_option"] = self.time_option
        if self.time is not None:
            result["time"] = self.time
        if self.unit is not None:
            result["unit"] = self.unit
        if self.comment is not None:
            result["comment"] = self.comment
        if self.return_value is not None:
            result["return_value"] = self.return_value
        if self.condition is not None:
            result["condition"] = self.condition
        if self.then_branch is not None:
            result["then_branch"] = self.then_branch
        if self.else_branch is not None:
            result["else_branch"] = self.else_branch
        if self.loop_type is not None:
            result["loop_type"] = self.loop_type
        if self.loop_count is not None:
            result["loop_count"] = self.loop_count
        if self.loop_condition is not None:
            result["loop_condition"] = self.loop_condition
        
        # 添加子步骤
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        
        return result


class PackageParser:
    """Package.pkg 解析器"""
    
    def __init__(self):
        self.ve = ValueExpression()
        self.current_parent_id = None
    
    def parse_file(self, xml_filename: str) -> List[Dict]:
        """解析 XML 文件"""
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        
        test_steps = []
        
        # 遍历最上层的测试步骤
        for test_step_elem in root.findall("./ns:TESTSTEPS/ns:TESTSTEP", namespaces=ns):
            step = self.parse_test_step(test_step_elem, None)
            if step:
                test_steps.append(step)
        
        return [step.to_dict() for step in test_steps]
    
    def parse_test_step(self, elem, parent_id: Optional[str]) -> Optional[TestStep]:
        """解析单个测试步骤"""
        if elem is None:
            return None
        
        # 获取步骤类型
        xsi_type = elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        if not xsi_type:
            return None
        
        # 创建步骤对象
        step = TestStep()
        step.id = elem.get("id")
        step.parent_id = parent_id
        step.name = elem.get("name")
        step.type = xsi_type
        
        # 解析通用属性
        breakpoint_elem = elem.find("./ns:BREAKPOINT", namespaces=ns)
        if breakpoint_elem is not None:
            step.breakpoint = self.ve.parse_value_expression(breakpoint_elem)
        
        enabled_elem = elem.find("./ns:ENABLED", namespaces=ns)
        if enabled_elem is not None:
            step.enable = self.ve.parse_value_expression(enabled_elem)
        
        # 根据类型解析特定属性
        self.parse_step_by_type(elem, step, xsi_type)
        
        # 递归解析子步骤
        self.parse_children(elem, step)
        
        return step
    
    def parse_step_by_type(self, elem, step: TestStep, xsi_type: str):
        """根据类型解析步骤属性"""
        
        # TsBlock
        if xsi_type == "utility-2752ad1e-4fef-11dc-81d4-0013728784ee":
            action_elem = elem.find("./ns:ACTION", namespaces=ns)
            if action_elem is not None:
                step.action = self.ve.parse_i18n_item(action_elem)
        
        # TsCalculation
        elif xsi_type == "utility-4115fa00-5f3c-11df-8a53-001c233b3528":
            formula_elem = elem.find("./ns:FORMULA", namespaces=ns)
            if formula_elem is not None:
                step.formula = self.ve.parse_value_expression(formula_elem.find("./ns:VALUE", namespaces=ns))
            
            expect_elem = elem.find("./ns:EXPECTATION-OPTION", namespaces=ns)
            if expect_elem is not None:
                step.expectation = self.ve.parse_expression(expect_elem.find("./ns:EXPRESSION", namespaces=ns))
        
        # TsMultiCheck
        elif xsi_type == "utility-2fb63e30-6816-11e5-bfd3-4851b798ee63":
            matchall_elem = elem.find("./ns:MATCHALL", namespaces=ns)
            if matchall_elem is not None:
                step.matchall = self.ve.parse_value_expression(matchall_elem)
            
            time_option_elem = elem.find("./ns:TIME-OPTION", namespaces=ns)
            if time_option_elem is not None:
                step.time_option = self.ve.parse_time_option(time_option_elem)
        
        # TsWait
        elif xsi_type == "utility-62d5a961-4fef-11dc-9944-0013728784ee":
            time_elem = elem.find("./ns:TIME", namespaces=ns)
            if time_elem is not None:
                step.time = self.ve.parse_value_expression(time_elem.find("./ns:VALUE", namespaces=ns))
            
            unit_elem = elem.find("./ns:UNIT", namespaces=ns)
            if unit_elem is not None:
                step.unit = unit_elem.text
        
        # TsComment
        elif xsi_type == "utility-1f4de951-4fef-11dc-969a-0013728784ee":
            comment_elem = elem.find("./ns:COMMENT", namespaces=ns)
            if comment_elem is not None:
                step.comment = self.ve.parse_i18n_item(comment_elem)
        
        # TsReturn
        elif xsi_type == "utility-4f3c5500-f0f5-11dc-b88f-001b24fa84be":
            return_elem = elem.find("./ns:RETURN", namespaces=ns)
            if return_elem is not None:
                step.return_value = self.ve.parse_value_expression(return_elem.find("./ns:VALUE", namespaces=ns))
        
        # TsIf
        elif xsi_type == "utility-3609c41e-4fef-11dc-899a-0013728784ee":
            condition_elem = elem.find("./ns:CONDITION", namespaces=ns)
            if condition_elem is not None:
                step.condition = self.ve.parse_expression(condition_elem.find("./ns:EXPRESSION", namespaces=ns))
        
        # TsLoop
        elif xsi_type == "utility-3da58cf0-4fef-11dc-be56-0013728784ee":
            loop_type_elem = elem.find("./ns:LOOP-TYPE", namespaces=ns)
            if loop_type_elem is not None:
                step.loop_type = loop_type_elem.text
            
            count_elem = elem.find("./ns:COUNT", namespaces=ns)
            if count_elem is not None:
                step.loop_count = self.ve.parse_value_expression(count_elem.find("./ns:VALUE", namespaces=ns))
            
            cond_elem = elem.find("./ns:CONDITION", namespaces=ns)
            if cond_elem is not None:
                step.loop_condition = self.ve.parse_expression(cond_elem.find("./ns:EXPRESSION", namespaces=ns))
    
    def parse_children(self, elem, step: TestStep):
        """解析子步骤"""
        # 定义子步骤的标签
        child_tags = ["ns:TESTSTEP"]
        
        # 特殊步骤需要解析特定标签的子步骤
        xsi_type = elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        
        if xsi_type == "utility-3609c41e-4fef-11dc-899a-0013728784ee":  # TsIf
            child_tags.extend(["ns:THEN", "ns:ELSE"])
        elif xsi_type == "utility-3da58cf0-4fef-11dc-be56-0013728784ee":  # TsLoop
            child_tags.append("ns:BODY")
        
        # 递归解析子步骤
        for tag in child_tags:
            for child_elem in elem.findall(tag, namespaces=ns):
                child_step = self.parse_test_step(child_elem, step.id)
                if child_step:
                    step.children.append(child_step)
                    
                    # 特殊处理：将子步骤分配到特定分支
                    if tag == "ns:THEN":
                        step.then_branch = child_step.to_dict()
                    elif tag == "ns:ELSE":
                        step.else_branch = child_step.to_dict()


def main():
    """主函数"""
    parser = PackageParser()
    
    try:
        # 解析 Package.pkg
        result = parser.parse_file("Package.pkg")
        
        # 输出 JSON
        output_file = "package.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        print("解析成功！结果已保存到", output_file)
        print(f"共解析 {len(result)} 个顶层测试步骤")

        # 打印统计信息
        def count_steps(steps, stats=None):
            if stats is None:
                stats = {"total": 0, "types": {}}

            for step in steps:
                stats["total"] += 1
                step_type = step.get("type", "unknown")
                stats["types"][step_type] = stats["types"].get(step_type, 0) + 1

                if "children" in step:
                    count_steps(step["children"], stats)

            return stats

        stats = count_steps(result)
        print(f"总步骤数: {stats['total']}")
        print("步骤类型统计:")
        for step_type, count in stats["types"].items():
            print(f"  - {step_type}: {count}")

        # 打印示例
        if result:
            print("\n示例步骤:")
            print(json.dumps(result[0], ensure_ascii=False, indent=2))

    except Exception as e:
        print("解析失败:", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
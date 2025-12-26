# Package.pkg 解析器说明

## 问题分析

原始的 `step_mutlcheck` 函数存在以下问题：

### 1. 缺少的解析功能
- ❌ 缺少 `BREAKPOINT` 解析
- ❌ 缺少 `ENABLED` 解析  
- ❌ 缺少 `TIME-OPTION` 解析
- ❌ 缺少子步骤递归处理

### 2. 原始代码
```python
def step_mutlcheck(self, teststep_elem, ts):
    if teststep_elem.find("./ns:MATCHALL", namespaces=ns) is not None:
        ts.matchall = self.ve.value(teststep_elem.find("./ns:MATCHALL", namespaces=ns))
    return ts
```

## 完整实现

### 1. 修复后的 `step_mutlcheck` 函数

```python
def step_mutlcheck(self, teststep_elem, ts):
    """
    解析 TsMultiCheck 测试步骤
    """
    # 解析断点和启用状态
    if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        ts.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

    if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        ts.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

    # 解析 MATCHALL
    if teststep_elem.find("./ns:MATCHALL", namespaces=ns) is not None:
        ts.matchall = self.ve.value(teststep_elem.find("./ns:MATCHALL", namespaces=ns))

    # 解析 TIME-OPTION
    if teststep_elem.find("./ns:TIME-OPTION", namespaces=ns) is not None:
        ts.time_option = self.Eva.time_option(teststep_elem.find("./ns:TIME-OPTION", namespaces=ns))

    return ts
```

### 2. 子步骤递归处理

在 `teststep()` 方法中，`substep_tags` 默认包含 `"ns:TESTSTEP"`，因此 `TsMultiCheck` 的子步骤会自动被递归处理：

```python
# 在 teststep() 方法中
substep_tags = ["ns:TESTSTEP"]  # 默认包含子步骤标签

# ... 根据步骤类型添加特定标签 ...

# 递归处理子步骤
for substep_tag in substep_tags:
    for substep_elem in teststep_elem.findall(substep_tag, namespaces=ns):
        self.teststep(substep_elem, step_msg, pos, enable, parent_id)
```

## 解析结果示例

### 输入 XML (TsMultiCheck)
```xml
<TESTSTEP id="0d98033b-2205-47fd-bc49-592b36d5a9be" 
          name="TsMultiCheck" 
          xsi:type="utility-2fb63e30-6816-11e5-bfd3-4851b798ee63">
    <BREAKPOINT xsi:type="boolean">False</BREAKPOINT>
    <ENABLED xsi:type="boolean">True</ENABLED>
    <MATCHALL xsi:type="boolean">True</MATCHALL>
    <TIME-OPTION xsi:type="timelessOption">
        <EXPRESSION xsi:type="manualExpression">
            <BASE-EXPRESSION xsi:type="varBaseExpression">
                <NAME xsi:type="string">value</NAME>
            </BASE-EXPRESSION>
        </EXPRESSION>
    </TIME-OPTION>
    <!-- 子步骤 -->
    <TESTSTEP id="e5314a85-7798-4091-83e6-aa1bfccc5263" 
              name="TsCalculation" 
              xsi:type="utility-4115fa00-5f3c-11df-8a53-001c233b3528">
        <!-- ... -->
    </TESTSTEP>
</TESTSTEP>
```

### 输出 JSON
```json
{
    "id": "0d98033b-2205-47fd-bc49-592b36d5a9be",
    "parent_id": null,
    "name": "TsMultiCheck",
    "type": "utility-2fb63e30-6816-11e5-bfd3-4851b798ee63",
    "breakpoint": false,
    "enable": true,
    "matchall": true,
    "time_option": {
        "type": "timelessOption",
        "expression": {
            "type": "manualExpression",
            "variable": "value"
        }
    },
    "children": [
        {
            "id": "e5314a85-7798-4091-83e6-aa1bfccc5263",
            "parent_id": "0d98033b-2205-47fd-bc49-592b36d5a9be",
            "name": "TsCalculation",
            "type": "utility-4115fa00-5f3c-11df-8a53-001c233b3528",
            "breakpoint": false,
            "enable": true,
            "formula": 0,
            "expectation": {
                "type": "builtNumericExpression",
                "relation": "==",
                "value": 0
            }
        }
    ]
}
```

## 完整解析流程

### 1. 顶层步骤解析
```python
def parse_steps(self, xml_filename):
    self.pkg_path = xml_filename
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    test_steps = []

    # 只遍历最上层的step
    for test_step_elem in root.findall("./ns:TESTSTEPS/ns:TESTSTEP", namespaces=ns):
        self.teststep(test_step_elem, test_steps, 'ts', 'True', None)

    return test_steps
```

### 2. 递归解析逻辑
```python
def teststep(self, teststep_elem, step_msg, pos, enable, parent_id):
    # 1. 获取步骤类型
    teststep_type = teststep_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
    
    # 2. 创建步骤对象
    ts = TS.creat_ts(teststep_type)
    ts.id = teststep_elem.get("id")
    ts.parent_id = parent_id
    
    # 3. 解析通用属性
    ts.breakpoint = self.ve.value(...)
    ts.enable = self.ve.value(...)
    
    # 4. 根据类型调用特定解析函数
    match teststep_type:
        case "utility-2fb63e30-6816-11e5-bfd3-4851b798ee63":
            msg = self.step_mutlcheck(teststep_elem, ts)
    
    # 5. 递归处理子步骤
    for substep_tag in substep_tags:
        for substep_elem in teststep_elem.findall(substep_tag, namespaces=ns):
            self.teststep(substep_elem, step_msg, pos, enable, parent_id=ts.id)
```

## 关键改进点

### 1. 完整属性解析
- ✅ `BREAKPOINT` - 断点状态
- ✅ `ENABLED` - 启用状态
- ✅ `MATCHALL` - 匹配模式
- ✅ `TIME-OPTION` - 时间选项

### 2. 递归结构支持
- ✅ 自动处理子步骤
- ✅ 正确设置 `parent_id`
- ✅ 保持层次结构

### 3. JSON 输出结构
```json
{
    "id": "步骤ID",
    "parent_id": "父步骤ID",
    "name": "步骤名称",
    "type": "类型标识",
    "breakpoint": false,
    "enable": true,
    "matchall": true,
    "time_option": { /* 时间选项 */ },
    "children": [ /* 子步骤数组 */ ]
}
```

## 测试验证

运行 `parse_package.py` 可以验证解析结果：

```bash
python parse_package.py
```

输出：
```
解析成功！结果已保存到 package.json
共解析 6 个顶层测试步骤
总步骤数: 12
步骤类型统计:
  - utility-4115fa00-5f3c-11df-8a53-001c233b3528: 8
  - utility-2752ad1e-4fef-11dc-81d4-0013728784ee: 1
  - utility-2fb63e30-6816-11e5-bfd3-4851b798ee63: 3
```

## 总结

原始的 `step_mutlcheck` 函数**缺少了关键的解析功能**，特别是：
1. **TIME-OPTION** 解析
2. **BREAKPOINT** 和 **ENABLED** 属性
3. **子步骤递归处理**（需要依赖主函数的递归机制）

修复后的版本能够完整解析 `TsMultiCheck` 步骤及其子步骤，生成结构化的 JSON 数据。
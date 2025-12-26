import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))
from ..model.metric import Metric
from ..model.expectation import *
from ..model.expression import *
from ..model.ts import CallReturn, TouchInputAction, Parameter
from ..model.timeoption import TimeOption
from ..model.tbc import Job, Port_Type, Property
import os 

#所有的xml节点变量都加_elem后缀
# ns = {"ns": "http://www.tracetronic.de/xml/ecu-test"}

class ValueExpression():
    
    def __init__(self,ns = None) -> None:
        if ns is None:
            self.ns = {"ns": "http://www.tracetronic.de/xml/ecu-test"}
        else:
            self.ns = ns
        pass

    #"valueBaseExpression" "varBaseExpression"如果都是string时，value加引号表字符串，var不加表示变量 
    
    def abs_path(self, path1, path2):
        """
        path1 = "D:\data\ECU-TEST_223\Packages\nest\Package (1).pkg"
        path2 = r"../INCA_Test.pkg"
        return "D:\data\ECU-TEST_223\Packages\INCA_Test.pkg"
        """
        abs_path1 = os.path.abspath(path1)
        folder_path = os.path.dirname(abs_path1)
        absolute_paths = folder_path.split('\\')
        path2 = path2.replace("'","")
        relative_paths = path2.split("/")
        for relative_path in relative_paths:
            if relative_path == "..":
                absolute_paths.pop()
            else:
                absolute_paths.append(relative_path)
        absolute_path2 = os.path.join(*absolute_paths).replace(":",":\\")
        return absolute_path2


    def value(self,elem):
        type = elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        if type is None:
            type = elem.get("xsi_type")
            
        match type:
            case "valueBaseExpression":
                return self._value_base_expression(elem)
            
            case "functionBaseExpression":
                return self._function_base_expression(elem)
            
            case "varBaseExpression":
                return self._var_base_expression(elem)
            
            case "compareOpBaseExpression":
                return self._compare_opbase_expression(elem)

            case "binaryOpBaseExpression":
                return self._binary_opbase_expression(elem)
            
            case "builtNumericExpression":
                return self._built_numeric_expression(elem)
            
            case "builtStringExpression":
                return self._built_string_expression(elem)

            case "listOrTupleBaseExpression":
                return self._listOrTuple_base_expression(elem)
            
            case "attributeBaseExpression":
                return self._attribute_base_expression(elem)
            
            case "orBaseExpression":
                return self._or_base_expression(elem)
            
            case "andBaseExpression":
                return self._and_base_expression(elem)
            
            case 'unaryOpBaseExpression':
                return self._unary_op_base_expression(elem)

            case "sliceBaseExpression":
                return self._slice_base_expression(elem)
            
            case "manualExpression":
                return self._manual_expression(elem)
            
            case "manualNumericExpression":
                return self._manual_numeric_expression(elem)
            
            case "manualStringExpression":
                return self._manual_string_expression(elem)
                
            case 'expressionValue':
                return self._expression_value(elem)
            
            case 'I18NItem':
                return self._I18NItem(elem)
            
            case 'parentheses':
                return self._parentheses(elem)
            
            case 'dictBaseExpression':
                return self._dict_base_expression(elem)

            case 'expressionDictItem':
                return self._expression_dict_item(elem)
            
            case 'kwargBaseExpression':
                return self._kwarg_base_expression(elem)

            case 'setBaseExpression':
                return self._set_base_expression(elem)

            case'readOnlyExpression':
                return None
            
            case 'sparseVector':
                return self._sparse_vector(elem)
            
            case 'vectorSingleExpression':
                return self._vector_single_expression(elem)
            
            case 'sparseCurve':
                return self._sparse_curve(elem)
            
            case 'curveSingleExpression':
                return self._curve_single_expression(elem)
            
            case 'sparseMap':
                return self._sparse_map(elem)
            
            case 'mapSingleExpression':
                return self._map_single_expression(elem)
            
            case 'expressionVector':
                return self._expression_vector(elem)
            
            case 'expressionCurve':
                return self._expression_curve(elem)
            
            case 'expressionMap':
                return self._expression_map(elem)
            
            case 'expressionref':
                return self._expression_ref(elem)
            
            case "builtStringListExpression":
                return self._built_string_list_expression(elem)
            
            case 'localArtifactReference':
                return self._local_artifact_reference(elem)
            
            case 'imageFilterReference':
                return self._image_filter_reference(elem)
            
            case 'imageFilterArguments':
                return self._image_filter_arguments(elem)
            
            case 'imageFilterArgument':
                return self._image_filter_argument(elem)
            
            
            
            ################################数据类型####################################
            case "string":
                return self._string_expression(elem)
            
            case "float":
                return self._float_expression(elem)
            
            case "integer":
                return self._integer_expression(elem)
            
            case "boolean":
                return self._bool_expression(elem)
            
            case "byteStream":
                return self._bytestream(elem)
            
            case 'BitStream':
                return self._bitstream(elem)
            
            ################################非表达式####################################
            case 'callReturn':
                return self._call_return(elem)

            case 'metricInfo':
                return self._metric(elem)
            
            case 'timelessOption':
                return self._time_option(elem)
            
            case 'finallyTrueOption':
                return self._time_option(elem)
            
            case 'generallyTrueOption':
                return self._time_option(elem)
            
            case 'trueForWithinOption':
                return self._time_option(elem)
            
            case 'syncOnlyOption':
                return self._time_option(elem)
            
            case 'tsJobParameter':
                return self._job_parameter(elem)
            
            case "touchInputAction":
                return self._touch_input_action(elem)

            case "expressionQuantity":
                return self._expression_quantity(elem)
            

            ################################Tool Description####################################
            case 'jobDescriptor':
                return self._job_descriptor(elem)
            
            case 'propertyDescriptor':
                return self._property_descriptor(elem)

            case 'portImplInfo':
                return self._port_impl_info(elem)

            case 'implTypeDescriptor':
                return self._impl_type_descriptor(elem)
            
            case 'toolcaps':
                return self._port_type_id(elem)
            
            ################################    Mapping    ####################################
            case 'signalManipulationParams':
                return self._signal_manipulation_params(elem)

            case 'manipulationDuration':
                return self._manipulation_duration(elem)
            
            ################################    Prj    ####################################
            case "testManagementInfo":
                return self._test_management_info(elem)

            case "parameterEntry":
                return self._parameter_entry(elem)
            
            case "limitSettings":
                return self._limit_settings(elem)
            
            case "list":
                return self._list(elem)
            
            case "projectRef":
                return self._project_ref(elem)
            




            case _:
                print(f'ValueExpression 出现未解析的type：{type}')


    def _set_base_expression(self,elem):
        """
        <FORMULA xsi:type="setBaseExpression">
            <EXPRESSION-SET>
                <BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">1</VALUE>
                </BASE-EXPRESSION>
                <BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                    ...
                </BASE-EXPRESSION>
            </EXPRESSION-SET>
        </FORMULA>
        """
        base_expression_value = ''
        if elem.find("./ns:EXPRESSION-SET", namespaces= self.ns) is not None:
            for base_expression_elem in elem.findall("./ns:EXPRESSION-SET/ns:BASE-EXPRESSION", namespaces= self.ns):
                base_expression_value  += f"{self.value(base_expression_elem)}" + ','
                # base_expression_value  += 
            return "{"+base_expression_value[:-1]+"}"


    def _expression_dict_item(self,elem):
        """
        <ITEM xsi:type="expressionDictItem">
            <KEY format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">2</VALUE>
            </KEY>
            <VALUE format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">3</VALUE>
            </VALUE>
        </ITEM>
        """
        key = ''
        value= ''
        if elem.find("./ns:KEY", namespaces= self.ns) is not None:
            key = self.value(elem.find("./ns:KEY", namespaces= self.ns))
        if elem.find("./ns:VALUE", namespaces= self.ns) is not None:
            value = self.value(elem.find("./ns:VALUE", namespaces= self.ns))
        return f"{key}:{value},"


    def _dict_base_expression(self, elem):
        """
        <FORMULA xsi:type="dictBaseExpression">
            <EXPRESSION-DICT>
                <ITEM xsi:type="expressionDictItem">
                    <KEY format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="integer">1</VALUE>
                    </KEY>
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="integer">1</VALUE>
                    </VALUE>
                </ITEM>
                <ITEM xsi:type="expressionDictItem">
                ...
                </ITEM>
            </EXPRESSION-DICT>
        </FORMULA>
        """
        expression_dict = ""
        for item_elem in elem.findall("./ns:EXPRESSION-DICT/ns:ITEM", namespaces= self.ns):
            expression_dict += self.value(item_elem)
        return "{"+expression_dict[:-1]+"}"


    def _parentheses(self, elem):
        """
        <FIRST-COMPONENT xsi:type="parentheses">
            <COMPONENT xsi:type="compareOpBaseExpression">
            ...
            </COMPONENT>
        </FIRST-COMPONENT>
        """
        return self.value(elem.find("./ns:COMPONENT", namespaces= self.ns))


    def _compare_opbase_expression(self,elem):
        """
        <START-CONDITION xsi:type="compareOpBaseExpression">
			<NAME xsi:type="string">&lt;</NAME>
			<FIRST-COMPONENT xsi:type="varBaseExpression">
				<NAME xsi:type="string">loopCounter</NAME>
			</FIRST-COMPONENT>
			<SECOND-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">4</VALUE>
			</SECOND-COMPONENT>
		</START-CONDITION>
        """
        name = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        first_component_value = self.value(elem.find("./ns:FIRST-COMPONENT", namespaces= self.ns))
        second_component_value = self.value(elem.find("./ns:SECOND-COMPONENT", namespaces= self.ns))
        return f"{first_component_value} {name} {second_component_value}"


    def _value_base_expression(self,elem):
        """
        示例：
        <CASE-VALUE format-rev="2" xsi:type="valueBaseExpression">
			<VALUE xsi:type="integer">0</VALUE>
		</CASE-VALUE>
        """
        if elem.find("./ns:VALUE", namespaces= self.ns) is not None:
            value_elem = elem.find("./ns:VALUE", namespaces= self.ns)
            if value_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")=="string":
                # 值的形式给出string，表明有引号 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                return f"'{self.value(value_elem)}'"
            else:
                return self.value(value_elem)
    

    #直接返回字符串，后期去掉"'
    def _var_base_expression(self,elem):
        """
        <SWITCH-VALUE xsi:type="varBaseExpression">
			<NAME xsi:type="string">ExtrLifcnSts</NAME>
		</SWITCH-VALUE>
        """
        name = None
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            name = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        return name
    
    
    def _binary_opbase_expression(self,elem):
        """
        基本运算表达式
        <TESTSTEP format-rev="3" id="fd516e3d-36d4-4cf2-a2ef-0e993fe06699" name="TsCalculation" xsi:type="utility-4115fa00-5f3c-11df-8a53-001c233b3528">
			<VARIABLE-REFS>
				<VARIABLE-NAME dkey="default">
					<DVALUE xsi:type="string">a</DVALUE>
				</VARIABLE-NAME>
			</VARIABLE-REFS>
			<FORMULA xsi:type="binaryOpBaseExpression">
				<NAME xsi:type="string">BINARY_ADD</NAME>
				<FIRST-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="integer">1</VALUE>
				</FIRST-COMPONENT>
				<SECOND-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="integer">1</VALUE>
				</SECOND-COMPONENT>
			</FORMULA>
			<EXPECTATION-OPTION xsi:type="timelessOption">
				<EXPRESSION xsi:type="builtNumericExpression">
					<RELATION xsi:type="string">==</RELATION>
					<VALUE format-rev="2" xsi:type="valueBaseExpression">
						<VALUE xsi:type="integer">2</VALUE>
					</VALUE>
				</EXPRESSION>
			</EXPECTATION-OPTION>
		</TESTSTEP>
        """
        first_component_value = ''
        second_component_value = ''
        first_component = elem.find('./ns:FIRST-COMPONENT', namespaces= self.ns)
        second_component = elem.find('./ns:SECOND-COMPONENT', namespaces= self.ns)
        first_component_value = self.value(first_component)
        second_component_value = self.value(second_component)
        if elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_ADD':
            return f"({first_component_value} + {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_MULTIPLY':
            return f"({first_component_value} * {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_SUBTRACT':
            return f"({first_component_value} - {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_DIVIDE':
            return f"({first_component_value} / {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_SUBSCR':
            return f"({first_component_value}[{second_component_value}])"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_FLOOR_DIVIDE':    # 整除
            return f"({first_component_value} // {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_MODULO':          # 取余
            return f"({first_component_value} % {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_POWER':           # 幂
            return f"({first_component_value} ** {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_LSHIFT':          # 左移
            return f"({first_component_value} << {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_RSHIFT':          # 右移
            return f"({first_component_value} >> {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_AND':             # 与
            return f"({first_component_value} & {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_XOR':             # 异或
            return f"({first_component_value} ^ {second_component_value})"
        elif elem.find('./ns:NAME',namespaces= self.ns).text == 'BINARY_OR':              # 或
            return f"({first_component_value} | {second_component_value})"
        else:
            print(f"未识别的二元运算符：{elem.find('./ns:NAME',namespaces= self.ns).text}")
            return 'None'
    
    def _function_base_expression(self,elem):
        """
        函数表达式
		<CONDITION xsi:type="functionBaseExpression">
			<COMPONENT xsi:type="varBaseExpression">
				<NAME xsi:type="string">int</NAME>
			</COMPONENT>
			<ARGUMENTS>
				<ARGUMENT xsi:type="varBaseExpression">
					<NAME xsi:type="string">first_num</NAME>
				</ARGUMENT>
			</ARGUMENTS>
		</CONDITION>
        特殊func:
            dict(key1=1,key2=2)
            等价于{'key1': 2, 'key2': 1}
        <FORMULA xsi:type="functionBaseExpression">
            <COMPONENT xsi:type="varBaseExpression">
                <NAME xsi:type="string">dict</NAME>
            </COMPONENT>
            <KEYWORD-ARGUMENTS>
                <KEYWORD-ARGUMENT xsi:type="kwargBaseExpression">
                    <KEY format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="string">key1</VALUE>
                    </KEY>
                    <ARGUMENT format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="string">value1</VALUE>
                    </ARGUMENT>
                </KEYWORD-ARGUMENT>
                ...
            </KEYWORD-ARGUMENTS>
        </FORMULA>
        """
        component_value = ''
        if elem.find('./ns:COMPONENT', namespaces= self.ns) is not None:
            component_value = self.value(elem.find('./ns:COMPONENT', namespaces= self.ns))
        if elem.find('./ns:ARGUMENTS', namespaces= self.ns) is not None:
            argument_value = ''
            for argument_elem in elem.findall('./ns:ARGUMENTS/ns:ARGUMENT', namespaces= self.ns):
                argument_value = argument_value+str(self.value(argument_elem))+','
            return f"{component_value}({argument_value[:-1]})" # round(1,3,4)
        if elem.find('./ns:KEYWORD-ARGUMENTS', namespaces= self.ns) is not None:
            keyword_argument_value = ''
            for keyword_argument_elem in elem.findall('./ns:KEYWORD-ARGUMENTS/ns:KEYWORD-ARGUMENT', namespaces= self.ns):
                keyword_argument_value += self.value(keyword_argument_elem)
            return "dict("+keyword_argument_value[:-1]+")" # "dict("+f"{keyword_argument_value[:-1]}"+")"效果一样
        return f"{component_value}()"

    def _kwarg_base_expression(self,elem):
        """
        <KEYWORD-ARGUMENT xsi:type="kwargBaseExpression">
            <KEY format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="string">key1</VALUE>
            </KEY>
            <ARGUMENT format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="string">value1</VALUE>
            </ARGUMENT>
        </KEYWORD-ARGUMENT>
        """
        key = ''
        argument = ''
        if elem.find('./ns:KEY', namespaces= self.ns) is not None:
            key = self.value(elem.find('./ns:KEY', namespaces= self.ns)).replace("'","") # 这里要去掉引号
        if elem.find('./ns:ARGUMENT', namespaces= self.ns) is not None:
            argument = self.value(elem.find('./ns:ARGUMENT', namespaces= self.ns))
        return f"{key} = {argument},"


    def _built_numeric_expression(self,elem):
        """
        数学表达式
        <EXPRESSION xsi:type="builtNumericExpression">
			<RELATION xsi:type="string">&gt;=</RELATION>
			<VALUE format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">0</VALUE>
			</VALUE>
            <TOLERANCE style="absolute-value" xsi:type="Tolerance">
				<VALUE format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="integer">5</VALUE>
				</VALUE>
			</TOLERANCE>
		</EXPRESSION>
        """
        # 数值的误差容忍度
        comparsion = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find('./ns:RELATION', namespaces= self.ns) is not None:
            relation = self.value(elem.find('./ns:RELATION', namespaces= self.ns))
            comparsion.relation = relation
        if elem.find('./ns:VALUE', namespaces= self.ns) is not None:
            comparsion.value = str(self.value(elem.find('./ns:VALUE', namespaces= self.ns)))
        if elem.find('./ns:TOLERANCE', namespaces= self.ns) is not None:
            comparsion.numeric_tolerance_type = elem.find('./ns:TOLERANCE', namespaces= self.ns).get("style").replace('absolute-value','absolute').replace('decimal-places','fractional')
            comparsion.numeric_tolerance_value = str(self.value(elem.find('./ns:TOLERANCE/ns:VALUE', namespaces= self.ns)))
        # comparsion.numeric_relation = f"{comparsion.relation} {comparsion.value}"

        return comparsion


    def _manual_expression(self,elem):
        """
        <EXPRESSION xsi:type="manualExpression">
			<BASE-EXPRESSION xsi:type="varBaseExpression">
				<NAME xsi:type="string">value</NAME>
			</BASE-EXPRESSION>
		</EXPRESSION>
        """
        comparsion = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find('./ns:BASE-EXPRESSION',namespaces= self.ns) is not None:
            comparsion.base_expression = str(self.value(elem.find('./ns:BASE-EXPRESSION',namespaces= self.ns)))
        return comparsion


    def _manual_numeric_expression(self,elem):
        """
        <EXPRESSION xsi:type="manualNumericExpression">
			<BASE-EXPRESSION xsi:type="compareOpBaseExpression">
				<NAME xsi:type="string">&gt;=</NAME>
				<FIRST-COMPONENT xsi:type="varBaseExpression">
					<NAME xsi:type="string">value</NAME>
				</FIRST-COMPONENT>
				<SECOND-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="integer">0</VALUE>
				</SECOND-COMPONENT>
			</BASE-EXPRESSION>
		</EXPRESSION>
        """
        comparsion = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find('./ns:BASE-EXPRESSION',namespaces= self.ns) is not None:
            comparsion.base_expression = str(self.value(elem.find('./ns:BASE-EXPRESSION',namespaces= self.ns)))
        return comparsion
        

    def _built_string_expression(self,elem):
        """
		<EXPRESSION xsi:type="builtStringExpression">
			<CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
			<BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="string">Blinking</VALUE>
			</BASE-EXPRESSION>
		</EXPRESSION> 
        """
        comparsion = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find('./ns:CASE-SENSITIVE', namespaces= self.ns) is not None:
            case_sensitive_value = self.value(elem.find('./ns:CASE-SENSITIVE', namespaces= self.ns))
        if elem.find('./ns:BASE-EXPRESSION', namespaces= self.ns) is not None:
            base_expression_value = self.value(elem.find('./ns:BASE-EXPRESSION', namespaces= self.ns))
        if elem.find('./ns:TYPE', namespaces= self.ns) is not None:
            comparsion.string_type = self.value(elem.find('./ns:TYPE', namespaces= self.ns))
        comparsion.string_value = base_expression_value
        comparsion.string_sensitivity = case_sensitive_value
        return comparsion


    def _manual_string_expression(self,elem):
        """
		<EXPRESSION xsi:type="manualStringExpression">
			<CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
			<BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="string">Blinking</VALUE>
			</BASE-EXPRESSION>
		</EXPRESSION> 
        """
        comparsion = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find('./ns:CASE-SENSITIVE', namespaces= self.ns) is not None:
            comparsion.string_sensitivity = self.value(elem.find('./ns:CASE-SENSITIVE', namespaces= self.ns))
        if elem.find('./ns:BASE-EXPRESSION',namespaces= self.ns) is not None:
            comparsion.base_expression = str(self.value(elem.find('./ns:BASE-EXPRESSION',namespaces= self.ns)))   
        return comparsion
    
    
    def _attribute_base_expression(self,elem):
        """
        <FORMULA xsi:type="attributeBaseExpression">
			<COMPONENT xsi:type="varBaseExpression">
				<NAME xsi:type="string">keyResponse</NAME>
			</COMPONENT>
			<ATTR-NAME xsi:type="string">Response</ATTR-NAME>
		</FORMULA>
        """
        component_value = self.value(elem.find('./ns:COMPONENT', namespaces= self.ns))
        attr_name_value = self.value(elem.find('./ns:ATTR-NAME', namespaces= self.ns))
        return f"{component_value}.{attr_name_value}"


    def _listOrTuple_base_expression(self,elem):
        """
        <FORMULA xsi:type="listOrTupleBaseExpression">
            <IS-LIST xsi:type="boolean">True</IS-LIST>
            <EXPRESSION-LIST>
                <BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">0</VALUE>
                </BASE-EXPRESSION>
                <BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">1</VALUE>
                </BASE-EXPRESSION>
            </EXPRESSION-LIST>
        </FORMULA>
        """
        is_list_value = self.value(elem.find('./ns:IS-LIST', namespaces= self.ns))
        expression_list = ''
        expression_list_elem = elem.find('./ns:EXPRESSION-LIST', namespaces= self.ns)
        for base_expression_elem in expression_list_elem.findall('./ns:BASE-EXPRESSION', namespaces= self.ns):
            expression_list+=f"{self.value(base_expression_elem)},"
        if is_list_value:
            return '['+expression_list[:-1]+']'
        else:
            return '('+expression_list[:-1]+')'

    
    def _and_base_expression(self,elem):
        """
        <FORMULA xsi:type="andBaseExpression">
            <FIRST-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">1</VALUE>
            </FIRST-COMPONENT>
            <SECOND-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">2</VALUE>
            </SECOND-COMPONENT>
        </FORMULA>
        """
        first_component_value = self.value(elem.find('./ns:FIRST-COMPONENT',namespaces= self.ns))
        second_component_value = self.value(elem.find('./ns:SECOND-COMPONENT',namespaces= self.ns))
        return f"({first_component_value} and {second_component_value})"
    

    def _or_base_expression(self,elem):
        """
        <FORMULA xsi:type="orBaseExpression">
            <FIRST-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">1</VALUE>
            </FIRST-COMPONENT>
            <SECOND-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">2</VALUE>
            </SECOND-COMPONENT>
        </FORMULA>
        """
        first_component_value = self.value(elem.find('./ns:FIRST-COMPONENT',namespaces= self.ns))
        second_component_value = self.value(elem.find('./ns:SECOND-COMPONENT',namespaces= self.ns))
        return f"({first_component_value} or {second_component_value})"
    

    def _slice_base_expression(self,elem):
        """
        <DATA xsi:type="sliceBaseExpression">
            <COMPONENT xsi:type="varBaseExpression">
                <NAME xsi:type="string">keyID</NAME>
            </COMPONENT>
            <START format-rev="1" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">4</VALUE>
            </START>
            <STOP format-rev="1" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">12</VALUE>
            </STOP>
        </DATA>
        keyID[4:12]
        """
        stop_value = -1
        start_value = 0
        component_value = self.value(elem.find('./ns:COMPONENT',namespaces= self.ns))
        if elem.find('./ns:START',namespaces= self.ns) is not None:
            start_value = self.value(elem.find('./ns:START',namespaces= self.ns))
        if elem.find('./ns:STOP',namespaces= self.ns) is not None:
            stop_value = self.value(elem.find('./ns:STOP',namespaces= self.ns))
        return f"{component_value}[{start_value}:{stop_value}]"



    def _expression_value(self,elem):
        """
        <VALUE xsi:type="expressionValue">
			<DATA format-rev="1" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">2</VALUE>
			</DATA>
		</VALUE>
        """
        if elem.find('./ns:DATA',namespaces= self.ns) is not None:
            return self.value(elem.find('./ns:DATA',namespaces= self.ns))
        

    def _unary_op_base_expression(self,elem):
        """
        <FORMULA xsi:type="unaryOpBaseExpression">
            <NAME xsi:type="string">UNARY_NOT</NAME>
            <COMPONENT format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">1</VALUE>
            </COMPONENT>
        </FORMULA>
        """
        value = None
        name = None
        if elem.find('./ns:NAME',namespaces= self.ns) is not None:
            name = self.value(elem.find('./ns:NAME',namespaces= self.ns))
        if elem.find('./ns:COMPONENT',namespaces= self.ns) is not None:
            value = self.value(elem.find('./ns:COMPONENT',namespaces= self.ns))
        if name == 'UNARY_NOT':
            return f'not {value}'
        elif name == 'UNARY_NEGATIVE':
            return f'-{value}'

    #字符串
    def _I18NItem(self,elem):
        """
        <ACTION xsi:type="I18NItem">
            <MULTILANGDATA>
                <ELEMENT dkey="en_US">
                    <DVALUE xsi:type="string">TsBlock-Name</DVALUE>
                </ELEMENT>
            </MULTILANGDATA>
            <INITIAL-LANGUAGE xsi:type="string">en_US</INITIAL-LANGUAGE>
        </ACTION>
        """
        # 首先检查语言
        initial_language = 'en_US'
        value = None
        if elem.find("./ns:INITIAL-LANGUAGE", namespaces= self.ns) is not None:
            initial_language = self.value(elem.find("./ns:INITIAL-LANGUAGE", namespaces= self.ns))
        element_elems = elem.findall("./ns:MULTILANGDATA/ns:ELEMENT", namespaces= self.ns)
        for element_elem  in element_elems:
            if element_elem.get("dkey") == initial_language:
                value = self.value(element_elem.find("./ns:DVALUE", namespaces= self.ns))
        return value


    def _sparse_vector(self,elem):
        """
        <DATASTRUCTURE format-rev="1" xsi:type="sparseVector">
            <DIMENSION xsi:type="integer">4</DIMENSION>
            <VALUES>
                <ELEMENT idx="0">
                    <VALUE xsi:type="builtNumericExpression">
                        <RELATION xsi:type="string">==</RELATION>
                        <VALUE format-rev="2" xsi:type="valueBaseExpression">
                            <VALUE xsi:type="float">0.0</VALUE>
                        </VALUE>
                    </VALUE>
                </ELEMENT>
                <ELEMENT idx="3">
                    <VALUE xsi:type="builtNumericExpression">
                        <RELATION xsi:type="string">==</RELATION>
                        <VALUE format-rev="2" xsi:type="valueBaseExpression">
                            <VALUE xsi:type="float">2.0</VALUE>
                        </VALUE>
                    </VALUE>
                </ELEMENT>
            </VALUES>
        </DATASTRUCTURE>
        """
        # 用于read整个数组的期望值
        value = []
        dimension = None
        if elem.find("./ns:DIMENSION", namespaces= self.ns) is not None:
            dimension = self.value(elem.find("./ns:DIMENSION", namespaces= self.ns))
        value_elems = elem.findall("./ns:VALUES/ns:ELEMENT", namespaces= self.ns)
        for value_elem in value_elems:
            value.append([value_elem.get('idx'), (self.value(value_elem.find("./ns:VALUE", namespaces= self.ns)))]) # 不一定所有下标都要对比期望值
        return {"value":value,"dimension":dimension}


    def _vector_single_expression(self, elem):
        """
        <EXPRESSION xsi:type="vectorSingleExpression">
            <DATASTRUCTURE format-rev="1" xsi:type="sparseVector">
                <DIMENSION xsi:type="integer">19</DIMENSION>
                <VALUES>
                    <ELEMENT idx="0">
                        <VALUE xsi:type="builtNumericExpression">
                            <RELATION xsi:type="string">==</RELATION>
                            <VALUE format-rev="1" xsi:type="valueBaseExpression">
                                <VALUE xsi:type="integer">9</VALUE>
                            </VALUE>
                        </VALUE>
                    </ELEMENT>
                    <ELEMENT idx="1">
                        <VALUE xsi:type="builtNumericExpression">
                            <RELATION xsi:type="string">==</RELATION>
                            <VALUE format-rev="1" xsi:type="valueBaseExpression">
                                <VALUE xsi:type="integer">16</VALUE>
                            </VALUE>
                        </VALUE>
                    </ELEMENT>
                    ...
                    <ELEMENT idx="18">
                        <VALUE xsi:type="builtNumericExpression">
                            <RELATION xsi:type="string">==</RELATION>
                            <VALUE format-rev="1" xsi:type="valueBaseExpression">
                                <VALUE xsi:type="integer">128</VALUE>
                            </VALUE>
                        </VALUE>
                    </ELEMENT>
                </VALUES>
            </DATASTRUCTURE>
        </EXPRESSION>
        """
        expression = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        value = self.value(elem.find("./ns:DATASTRUCTURE", namespaces= self.ns))
        expression.dimension = value['dimension']
        expression.value = value['value']
        return expression
        

    def _sparse_curve(self, elem):
        """
        <DATASTRUCTURE format-rev="1" xsi:type="sparseCurve">
            <DIMENSION xsi:type="integer">7</DIMENSION>
            <DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                <DIMENSION xsi:type="integer">7</DIMENSION>
                <VALUES/>
            </DISTRIBUTION>
            <VALUES>
                <ELEMENT idx="0">
                    <VALUE xsi:type="builtNumericExpression">
                        <RELATION xsi:type="string">==</RELATION>
                        <VALUE xsi:type="unaryOpBaseExpression">
                            <NAME xsi:type="string">UNARY_NEGATIVE</NAME>
                            <COMPONENT format-rev="2" xsi:type="valueBaseExpression">
                                <VALUE xsi:type="float">600.0</VALUE>
                            </COMPONENT>
                        </VALUE>
                    </VALUE>
                </ELEMENT>
                <ELEMENT idx="3">
                    <VALUE xsi:type="builtNumericExpression">
                        <RELATION xsi:type="string">==</RELATION>
                        <VALUE xsi:type="unaryOpBaseExpression">
                            <NAME xsi:type="string">UNARY_NEGATIVE</NAME>
                            <COMPONENT format-rev="2" xsi:type="valueBaseExpression">
                                <VALUE xsi:type="float">600.0</VALUE>
                            </COMPONENT>
                        </VALUE>
                    </VALUE>
                </ELEMENT>
            </VALUES>
        </DATASTRUCTURE>
        """
        # to do
        value = []
        dimension = None
        if elem.find("./ns:DIMENSION", namespaces= self.ns) is not None:
            dimension = self.value(elem.find("./ns:DIMENSION", namespaces= self.ns))
        value_elems = elem.findall("./ns:VALUES/ns:ELEMENT", namespaces= self.ns)
        for value_elem in value_elems:
            value.append([value_elem.get('idx'), (self.value(value_elem.find("./ns:VALUE", namespaces= self.ns)))])# 不一定所有下标都要对比期望值
        return {"value":value,"dimension":dimension}
    

    def _curve_single_expression(self,elem):
        """
        <EXPRESSION xsi:type="curveSingleExpression">
            <DATASTRUCTURE format-rev="1" xsi:type="sparseCurve">
                <DIMENSION xsi:type="integer">7</DIMENSION>
                <DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                    <DIMENSION xsi:type="integer">7</DIMENSION>
                    <VALUES/>
                </DISTRIBUTION>
                <VALUES/>
            </DATASTRUCTURE>
        </EXPRESSION>
        """
        # to do
        expression = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        value = self.value(elem.find("./ns:DATASTRUCTURE", namespaces= self.ns))
        expression.dimension = value['dimension']
        expression.value = value['value']
        return expression
    
    
    def _sparse_map(self, elem):
        """
        <DATASTRUCTURE format-rev="1" xsi:type="sparseMap">
            <X-DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                <DIMENSION xsi:type="integer">10</DIMENSION>
                <VALUES/>
            </X-DISTRIBUTION>
            <Y-DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                <DIMENSION xsi:type="integer">5</DIMENSION>
                <VALUES/>
            </Y-DISTRIBUTION>
            <X-DIMENSION xsi:type="integer">10</X-DIMENSION>
            <Y-DIMENSION xsi:type="integer">5</Y-DIMENSION>
            <VALUES>
                <ELEMENT idx="1" idy="4">
                    <VALUE xsi:type="builtNumericExpression">
                        <RELATION xsi:type="string">==</RELATION>
                        <VALUE format-rev="2" xsi:type="valueBaseExpression">
                            <VALUE xsi:type="float">0.949999988079071</VALUE>
                        </VALUE>
                    </VALUE>
                </ELEMENT>
                <ELEMENT idx="3" idy="1">
                    <VALUE xsi:type="builtNumericExpression">
                        <RELATION xsi:type="string">==</RELATION>
                        <VALUE format-rev="2" xsi:type="valueBaseExpression">
                            <VALUE xsi:type="float">0.9200000166893005</VALUE>
                        </VALUE>
                    </VALUE>
                </ELEMENT>
            </VALUES>
        </DATASTRUCTURE>
        """
        value = []
        x_dimension = None
        y_dimension = None
        if elem.find("./ns:X-DIMENSION", namespaces= self.ns) is not None:
            x_dimension = self.value(elem.find("./ns:X-DIMENSION", namespaces= self.ns))
        if elem.find("./ns:Y-DIMENSION", namespaces= self.ns) is not None:
            y_dimension = self.value(elem.find("./ns:Y-DIMENSION", namespaces= self.ns))
        value_elems = elem.findall("./ns:VALUES/ns:ELEMENT", namespaces= self.ns)
        for value_elem in value_elems:
            value.append([value_elem.get('idx'), value_elem.get('idy'), (self.value(value_elem.find("./ns:VALUE", namespaces= self.ns)))])# 不一定所有下标都要对比期望值
        return {"value":value,"x_dimesion":x_dimension,"y_dimesion":y_dimension}
    

    def _map_single_expression(self,elem):
        """
        <EXPRESSION xsi:type="mapSingleExpression">
            <DATASTRUCTURE format-rev="1" xsi:type="sparseMap">
                <X-DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                    <DIMENSION xsi:type="integer">8</DIMENSION>
                    <VALUES/>
                </X-DISTRIBUTION>
                <Y-DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                    <DIMENSION xsi:type="integer">8</DIMENSION>
                    <VALUES/>
                </Y-DISTRIBUTION>
                <X-DIMENSION xsi:type="integer">8</X-DIMENSION>
                <Y-DIMENSION xsi:type="integer">8</Y-DIMENSION>
                <VALUES/>
            </DATASTRUCTURE>
        </EXPRESSION>
        """
        # to do 
        expression = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        value = self.value(elem.find("./ns:DATASTRUCTURE", namespaces= self.ns))
        expression.x_dimension = value['x_dimesion']
        expression.y_dimension = value['y_dimesion']
        expression.value = value['value']
        return expression


    def _expression_vector(self,elem):
        """
        <VALUE format-rev="1" xsi:type="expressionVector">
            <DIMENSION xsi:type="integer">16</DIMENSION>
            <VALUES>
                <ELEMENT idx="0">
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="float">255.0</VALUE>
                    </VALUE>
                </ELEMENT>
                <ELEMENT idx="5">
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="float">255.0</VALUE>
                    </VALUE>
                </ELEMENT>
                <ELEMENT idx="6">
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="float">255.0</VALUE>
                    </VALUE>
                </ELEMENT>
            </VALUES>
        </VALUE>
        """
        expression = Expression.creat_expression(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find("./ns:DIMENSION", namespaces= self.ns) is not None:
            expression.dimension = self.value(elem.find("./ns:DIMENSION", namespaces= self.ns))
        value_elems = elem.findall("./ns:VALUES/ns:ELEMENT", namespaces= self.ns)
        for value_elem in value_elems:
            expression.value.append([value_elem.get('idx'),self.value(value_elem.find("./ns:VALUE", namespaces= self.ns))])
        return expression


    def _expression_curve(self,elem):
        """
        <VALUE format-rev="1" xsi:type="expressionCurve">
            <DIMENSION xsi:type="integer">23</DIMENSION>
            <DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                <DIMENSION xsi:type="integer">23</DIMENSION>
                <VALUES/>
            </DISTRIBUTION>
            <VALUES>
                <ELEMENT idx="2">
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="float">150.0</VALUE>
                    </VALUE>
                </ELEMENT>
                <ELEMENT idx="8">
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="float">350.0</VALUE>
                    </VALUE>
                </ELEMENT>
            </VALUES>
        </VALUE>
        """
        expression = Expression.creat_expression(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find("./ns:DIMENSION", namespaces= self.ns) is not None:
            expression.dimension = self.value(elem.find("./ns:DIMENSION", namespaces= self.ns))
        value_elems = elem.findall("./ns:VALUES/ns:ELEMENT", namespaces= self.ns)
        for value_elem in value_elems:
            expression.value.append([value_elem.get('idx'),self.value(value_elem.find("./ns:VALUE", namespaces= self.ns))])
        return expression


    def _expression_map(self,elem):
        """
        <VALUE format-rev="1" xsi:type="expressionMap">
            <X-DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                <DIMENSION xsi:type="integer">16</DIMENSION>
                <VALUES/>
            </X-DISTRIBUTION>
            <Y-DISTRIBUTION format-rev="1" xsi:type="sparseVector">
                <DIMENSION xsi:type="integer">11</DIMENSION>
                <VALUES/>
            </Y-DISTRIBUTION>
            <X-DIMENSION xsi:type="integer">16</X-DIMENSION>
            <Y-DIMENSION xsi:type="integer">11</Y-DIMENSION>
            <VALUES>
                <ELEMENT idx="2" idy="2">
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="integer">10</VALUE>
                    </VALUE>
                </ELEMENT>
                <ELEMENT idx="4" idy="5">
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="integer">20</VALUE>
                    </VALUE>
                </ELEMENT>
            </VALUES>
        </VALUE>
        """
        expression = Expression.creat_expression(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find("./ns:X-DIMENSION", namespaces= self.ns) is not None:
           expression.x_dimension = self.value(elem.find("./ns:X-DIMENSION", namespaces= self.ns))
        if elem.find("./ns:Y-DIMENSION", namespaces= self.ns) is not None:
            expression.y_dimension = self.value(elem.find("./ns:Y-DIMENSION", namespaces= self.ns))
        value_elems = elem.findall("./ns:VALUES/ns:ELEMENT", namespaces= self.ns)
        for value_elem in value_elems:
            expression.value.append([value_elem.get('idx'), value_elem.get('idy'), (self.value(value_elem.find("./ns:VALUE", namespaces= self.ns)))])
        return expression
        
    
    def _expression_ref(self, elem):
        """
        <PACKAGE-REFERENCE xsi:type="expressionref">
            <PATH-EXPRESSION format-rev="1" xsi:type="valueBaseExpression">
                <VALUE xsi:type="string">PwrModSts_Set.pkg</VALUE>
            </PATH-EXPRESSION>
        </PACKAGE-REFERENCE>
        """
        return self.value(elem.find("./ns:PATH-EXPRESSION", namespaces= self.ns))
        
        
    def _built_string_list_expression(self, elem):
        """
        <EXPRESSION xsi:type="builtStringListExpression">
            <CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
            <TYPE xsi:type="integer">6</TYPE>
            <BASE-EXPRESSION xsi:type="listOrTupleBaseExpression">
                <IS-LIST xsi:type="boolean">True</IS-LIST>
                <EXPRESSION-LIST>
                    <BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="string">Unlocked</VALUE>
                    </BASE-EXPRESSION>
                    <BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="string">Partially_unlocked</VALUE>
                    </BASE-EXPRESSION>
                </EXPRESSION-LIST>
            </BASE-EXPRESSION>
        </EXPRESSION>
        """
        built_string_list_expression = Expectation.create_expectation(elem.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
        if elem.find("./ns:CASE-SENSITIVE", namespaces= self.ns) is not None:
            built_string_list_expression.case_sensitive = self.value(elem.find("./ns:CASE-SENSITIVE", namespaces= self.ns))
        if elem.find("./ns:TYPE", namespaces= self.ns) is not None:
            built_string_list_expression.type = self.value(elem.find("./ns:TYPE", namespaces= self.ns))
        if elem.find("./ns:BASE-EXPRESSION", namespaces= self.ns) is not None:
            built_string_list_expression.base_expression = self.value(elem.find("./ns:BASE-EXPRESSION", namespaces= self.ns))
        return built_string_list_expression

    ################################变量类型####################################

    def _string_expression(self,elem):
        return str(elem.text.replace("&lt;","<").replace("&gt;",">").replace("&quot;",'"')) if elem.text is not None else None
    

    def _bool_expression(self,elem):
        if elem.text is not None:
            if elem.text.lower() == 'true':
                return True
            else:
                return False
        else:
            return None
            

    def _integer_expression(self,elem):
        if elem.text is not None:
            try:
                return int(elem.text)
            except:
                try:
                    return int(elem.text, 16)
                except:
                    return float(elem.text)
        else:
            return None
    

    def _float_expression(self,elem):
        return float(elem.text) if elem.text is not None else None
    
    
    def _bitstream(self,elem):
        """
        <COMPLEX-DATA xsi:type="BitStream">
            <BIT-LENGTH xsi:type="integer">8</BIT-LENGTH>
            <DATA xsi:type="integer">18</DATA>
        </COMPLEX-DATA>
        """
        value = None
        bit_length = None  # 比特流长度暂时没用

        if elem.find("./ns:DATA", namespaces= self.ns) is not None:
            value = self.value(elem.find("./ns:DATA", namespaces= self.ns))

        if elem.find("./ns:BIT-LENGTH", namespaces= self.ns) is not None:
            value = self.value(elem.find("./ns:BIT-LENGTH", namespaces= self.ns))  

        return value


    def _bytestream(self,elem):
        """
        <COMPLEX-DATA xsi:type="byteStream">
            <CONTENT xsi:type="string">FF:FF:FF:FF:FF</CONTENT>
        </COMPLEX-DATA>
        """
        value = None
        if elem.find("./ns:CONTENT", namespaces= self.ns) is not None:
            value = self.value(elem.find("./ns:CONTENT", namespaces= self.ns))

        return value
    

    ################################非表达式####################################
    def _call_return(self,elem):
        """
        <RETURN xsi:type="callReturn">
            <NAME xsi:type="string">Power_ModePwrModSts_D002_0_POS</NAME>
            <METRIC format-rev="1" xsi:type="metricInfo">
                <Z-UNIT xsi:type="string">u_none</Z-UNIT>
                <VALUE-TYPE xsi:type="string">TEXT</VALUE-TYPE>
                <DATA-TYPE xsi:type="string">VALUE</DATA-TYPE>
            </METRIC>
            <SAVE-IN xsi:type="varBaseExpression">
                <NAME xsi:type="string">Power_ModePwrModSts_D002_0_POS</NAME>
            </SAVE-IN>
            <EXPECTATION xsi:type="readOnlyExpression"/>
        </RETURN>
        """
        call_return = CallReturn()
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            call_return.name = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        if elem.find("./ns:METRIC", namespaces= self.ns) is not None:
            call_return.metric = self.value(elem.find("./ns:METRIC", namespaces= self.ns))
        if elem.find("./ns:SAVE-IN", namespaces= self.ns) is not None:
            call_return.save_in = self.value(elem.find("./ns:SAVE-IN", namespaces= self.ns))
        if elem.find("./ns:EXPECTATION", namespaces= self.ns) is not None:
            call_return.expectation = self.value(elem.find("./ns:EXPECTATION", namespaces= self.ns))
        return  call_return
    

    def _call_parameter(self,elem):
        """
        <PARAMETER xsi:type="callParameter">
            <NAME xsi:type="string">Power_ModePwrModSts_D002_3_REQ_</NAME>
            <METRIC format-rev="1" xsi:type="metricInfo">
                <Z-UNIT xsi:type="string">u_none</Z-UNIT>
                <VALUE-TYPE xsi:type="string">TEXT</VALUE-TYPE>
                <DATA-TYPE xsi:type="string">VALUE</DATA-TYPE>
            </METRIC>
            <VALUE format-rev="1" xsi:type="valueBaseExpression">
                <VALUE xsi:type="string">Awake</VALUE>
            </VALUE>
        </PARAMETER>
        """
        parameter = Parameter()
        if elem.find('./ns:NAME',namespaces= self.ns) is not None:
            parameter.name = self.value(elem.find('./ns:NAME',namespaces= self.ns))
        if elem.find('./ns:METRIC',namespaces= self.ns) is not None:
            parameter.metric = self.value(elem.find('./ns:METRIC',namespaces= self.ns))
        if elem.find('./ns:VALUE',namespaces= self.ns) is not None:
            parameter.value = self.value(elem.find('./ns:VALUE',namespaces= self.ns))
        return parameter
    

    def _metric(self,elem):
        """
		<METRIC format-rev="1" xsi:type="metricInfo">
			<Z-UNIT xsi:type="string">u_none</Z-UNIT>
			<VALUE-TYPE xsi:type="string">PHYS</VALUE-TYPE>
			<DATA-TYPE xsi:type="string">VALUE</DATA-TYPE>
		</METRIC>
		"""

        data_type = self.value(elem.find("./ns:DATA-TYPE", namespaces= self.ns))

        metric_value = Metric.creat_metric(data_type=data_type)
        if elem.find("./ns:VALUE-TYPE", namespaces= self.ns) is not None:
            metric_value.value_type = self.value(elem.find("./ns:VALUE-TYPE", namespaces= self.ns))

        if elem.find("./ns:Z-UNIT", namespaces= self.ns) is not None:
            metric_value.z_unit = self.value(elem.find("./ns:Z-UNIT", namespaces= self.ns))

        if data_type == 'CURVE':
            if elem.find("./ns:X-UNIT", namespaces= self.ns) is not None:
                metric_value.x_unit = self.value(elem.find("./ns:X-UNIT", namespaces= self.ns))
            if elem.find("./ns:X-VALUE-TYPE", namespaces= self.ns) is not None:
                metric_value.x_value_type = self.value(elem.find("./ns:X-VALUE-TYPE", namespaces= self.ns))
        elif data_type == 'MAP':
            if elem.find("./ns:X-UNIT", namespaces= self.ns) is not None:
                metric_value.x_unit = self.value(elem.find("./ns:X-UNIT", namespaces= self.ns))
            if elem.find("./ns:X-VALUE-TYPE", namespaces= self.ns) is not None:
                metric_value.x_value_type = self.value(elem.find("./ns:X-VALUE-TYPE", namespaces= self.ns))
            if elem.find("./ns:Y-UNIT", namespaces= self.ns) is not None:
                metric_value.y_unit = self.value(elem.find("./ns:Y-UNIT", namespaces= self.ns))
            if elem.find("./ns:Y-VALUE-TYPE", namespaces= self.ns) is not None:
                metric_value.y_value_type = self.value(elem.find("./ns:Y-VALUE-TYPE", namespaces= self.ns))

        return metric_value
    

    def _time_option(self,elem):
        type = elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        time_option = TimeOption()
        time_option.time_type = type
        if elem.find("./ns:EXPRESSION", namespaces= self.ns) is not None:
            time_option.expression = self.value(elem.find("./ns:EXPRESSION", namespaces= self.ns))
        if elem.find("./ns:POLLING-CYCLE", namespaces= self.ns) is not None:
            time_option.Polling_cycle = self.value(elem.find("./ns:POLLING-CYCLE", namespaces= self.ns))
        if elem.find("./ns:POLLING-CYCLE-UNIT", namespaces= self.ns) is not None:
            time_option.Polling_cycle_unit = self.value(elem.find("./ns:POLLING-CYCLE-UNIT", namespaces= self.ns))
        if elem.find("./ns:TIME", namespaces= self.ns) is not None:
            time_option.time = self.value(elem.find("./ns:TIME", namespaces= self.ns))
        if elem.find("./ns:TIME-UNIT", namespaces= self.ns) is not None:
            time_option.time_unit = self.value(elem.find("./ns:TIME-UNIT", namespaces= self.ns))
        if elem.find("./ns:TIMEOUT", namespaces= self.ns) is not None:
            time_option.Timeout = self.value(elem.find("./ns:TIMEOUT", namespaces= self.ns))
        if elem.find("./ns:TIMEOUT-UNIT", namespaces= self.ns) is not None:
            time_option.Timeout_unit = self.value(elem.find("./ns:TIMEOUT-UNIT", namespaces= self.ns))
        if elem.find("./ns:MINDURATION", namespaces= self.ns) is not None:
            time_option.Minimum_duration = self.value(elem.find("./ns:MINDURATION", namespaces= self.ns))
        if elem.find("./ns:MINDURATION-UNIT", namespaces= self.ns) is not None:
            time_option.Minimum_duration_unit = self.value(elem.find("./ns:MINDURATION-UNIT", namespaces= self.ns))
        return time_option


    def _job_parameter(self,elem):
        """
        <JOB-PARAMETER xsi:type="tsJobParameter">
            <NAME xsi:type="string">SeparationTime</NAME>
            <EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">0</VALUE>
            </EXPRESSION>
        </JOB-PARAMETER>
        """
        expression = None
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            name = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        if elem.find("./ns:EXPRESSION", namespaces= self.ns) is not None:
            expression = self.value(elem.find("./ns:EXPRESSION", namespaces= self.ns))
        return {name: expression}




################################Tool Description####################################
    def _job_descriptor(self,elem):
        """
        <JOB format-rev="2" xsi:type="jobDescriptor">
            <NAME xsi:type="string">InitializeHardware</NAME>
            <PARAMETERS xsi:type="parameterDescriptorSet">
                <PARAM xsi:type="propertyDescriptor">
                    
                </PARAM>
            </PARAMETERS>
            <DESCRIPTION xsi:type="string">Initialize hardware</DESCRIPTION>
            <RETURN xsi:type="propertyDescriptor">
                
            </RETURN>
            <INVALID-AT xsi:type="string"/>
            <DEPRECATION-MESSAGE xsi:type="string"/>
        </JOB>
        """
        job = Job()
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            job.name = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        for parameter_elem in elem.findall("./ns:PARAMETERS/ns:PARAM", namespaces= self.ns):
            job.parameters.append(self.value(parameter_elem))
        if elem.find("./ns:DESCRIPTION", namespaces= self.ns) is not None:
            job.description = self.value(elem.find("./ns:DESCRIPTION", namespaces= self.ns))
        if elem.find("./ns:RETURN", namespaces= self.ns) is not None:
            job.job_return = self.value(elem.find("./ns:RETURN", namespaces= self.ns))
        if elem.find("./ns:INVALID-AT", namespaces= self.ns) is not None:
            job.invalid_at = self.value(elem.find("./ns:INVALID-AT", namespaces= self.ns))
        if elem.find("./ns:DEPRECATION-MESSAGE", namespaces= self.ns) is not None:
            job.deprecation_message = self.value(elem.find("./ns:DEPRECATION-MESSAGE", namespaces= self.ns))
        return job 


    def _port_impl_info(self,elem):
        """
        <PORT-TYPE xsi:type="portImplInfo">
            <PORT-TYPE-ID format-rev="2" xsi:type="toolcaps">
                <NAME xsi:type="string">APPLICATION</NAME>
            </PORT-TYPE-ID>
            <IMPL-TYPE xsi:type="implTypeDescriptor">
                <IMPL-TYPE-ID xsi:type="string">Standard</IMPL-TYPE-ID>
            </IMPL-TYPE>
            <IMPL-TYPE xsi:type="implTypeDescriptor">
                <IMPL-TYPE-ID xsi:type="string">Simulation</IMPL-TYPE-ID>
            </IMPL-TYPE>
        </PORT-TYPE>
        """
        port_type = Port_Type()
        if elem.find("./ns:PORT-TYPE-ID", namespaces= self.ns) is not None:
            port_type.id = self.value(elem.find("./ns:PORT-TYPE-ID", namespaces= self.ns))
        for impl_type_elem in elem.findall("./ns:IMPL-TYPE", namespaces= self.ns):
            port_type.impl_type_id.append(self.value(impl_type_elem))
        return port_type

    def _port_type_id(self,elem):
        """
        <PORT-TYPE-ID format-rev="2" xsi:type="toolcaps">
            <NAME xsi:type="string">APPLICATION</NAME>
        </PORT-TYPE-ID>
        """
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            return self.value(elem.find("./ns:NAME", namespaces= self.ns))
        return None


    def _impl_type_descriptor(self,elem):
        """
        <IMPL-TYPE xsi:type="implTypeDescriptor">
            <IMPL-TYPE-ID xsi:type="string">Simulation</IMPL-TYPE-ID>
        </IMPL-TYPE>
        """
        if elem.find("./ns:IMPL-TYPE-ID", namespaces= self.ns) is not None:
            return self.value(elem.find("./ns:IMPL-TYPE-ID", namespaces= self.ns))
        return None

    def _property_descriptor(self,elem):
        """
        <PROP xsi:type="propertyDescriptor">
            <NAME xsi:type="string">db</NAME>
            <DISPLAY-NAME xsi:type="string">Database</DISPLAY-NAME>
            <DISPLAY-LEVEL xsi:type="integer">0</DISPLAY-LEVEL>
            <DESCRIPTION xsi:type="string">Name of the database to use. Ignored if a Database template is used</DESCRIPTION>
            <TYPE xsi:type="string">string</TYPE>
            <DEFAULT xsi:type="string">ECU-TEST</DEFAULT>
            <READONLY xsi:type="boolean">False</READONLY>
            <INVALID-AT xsi:type="string"/>
            <DEPRECATION-MESSAGE xsi:type="string"/>
        </PROP>
        """
        property_descriptor = Property()
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            property_descriptor.name = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        if elem.find("./ns:DISPLAY-NAME", namespaces= self.ns) is not None:
            property_descriptor.display_name = self.value(elem.find("./ns:DISPLAY-NAME", namespaces= self.ns))
        if elem.find("./ns:DISPLAY-LEVEL", namespaces= self.ns) is not None:
            property_descriptor.display_level = self.value(elem.find("./ns:DISPLAY-LEVEL", namespaces= self.ns))
        if elem.find("./ns:DESCRIPTION", namespaces= self.ns) is not None:
            property_descriptor.description = self.value(elem.find("./ns:DESCRIPTION", namespaces= self.ns))
        if elem.find("./ns:TYPE", namespaces= self.ns) is not None:
            property_descriptor.type = self.value(elem.find("./ns:TYPE", namespaces= self.ns))
        if elem.find("./ns:DOMAIN", namespaces= self.ns) is not None:
            for element in elem.findall("./ns:DOMAIN/ns:ELEMENT", namespaces= self.ns):
                property_descriptor.domain.append(self.value(element))
        if elem.find("./ns:DEFAULT", namespaces= self.ns) is not None:
            property_descriptor.default = self.value(elem.find("./ns:DEFAULT", namespaces= self.ns))
        if elem.find("./ns:READONLY", namespaces= self.ns) is not None:
            property_descriptor.readonly = self.value(elem.find("./ns:READONLY", namespaces= self.ns))
        if elem.find("./ns:INVALID-AT", namespaces= self.ns) is not None:
            property_descriptor.invalid_at = self.value(elem.find("./ns:INVALID-AT", namespaces= self.ns))
        if elem.find("./ns:DEPRECATION-MESSAGE", namespaces= self.ns) is not None:
            property_descriptor.deprecation_message = self.value(elem.find("./ns:DEPRECATION-MESSAGE", namespaces= self.ns))
        return property_descriptor
    
    def _signal_manipulation_params(self,elem):
        """
        <MANIPULATION xsi:type="signalManipulationParams">
            <DURATION style="message-count" xsi:type="manipulationDuration">
                <VALUE xsi:type="integer">0</VALUE>
            </DURATION>
        </MANIPULATION>
        """
        manipulation = None
        if elem.find("./ns:DURATION", namespaces= self.ns) is not None:
            manipulation = self.value(elem.find("./ns:DURATION", namespaces= self.ns))
        return manipulation
    
    def _manipulation_duration(self, elem):
        """
        <DURATION style="message-count" xsi:type="manipulationDuration">
            <VALUE xsi:type="integer">0</VALUE>
        </DURATION>
        """
        if elem.find("./ns:VALUE", namespaces= self.ns) is not None:
            return self.value(elem.find("./ns:VALUE", namespaces= self.ns))
        return None

    ################################    Prj    ####################################

    def _test_management_info(self, elem):
        """
        <TM-INFO format-rev="1" xsi:type="testManagementInfo">
            <TESTCASE-ID xsi:type="string">ActvnOfIndcr_LampCANFD.pkg</TESTCASE-ID>
        </TM-INFO>
        """

        if elem.find("./ns:TESTCASE-ID", namespaces= self.ns) is not None:
            testcase_id = self.value(elem.find("./ns:TESTCASE-ID", namespaces= self.ns))
            return testcase_id
        return None
    
    def _parameter_entry(self, elem):
        """
        <PARAMETER xsi:type="parameterEntry">
            <NAME xsi:type="string">String</NAME>
            <VALUE format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="string">str1</VALUE>
            </VALUE>
        </PARAMETER>
        """
        parameter = {}
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            name = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        if elem.find("./ns:VALUE", namespaces= self.ns) is not None:
            parameter[name] = self.value(elem.find("./ns:VALUE", namespaces= self.ns))
            
        return parameter
    
    def _limit_settings(self, elem):
        """
        <LIMIT-SETTINGS xsi:type="limitSettings">
            <LIMIT xsi:type="integer">14000</LIMIT>
        </LIMIT-SETTINGS>
        """
        if elem.find("./ns:LIMIT", namespaces= self.ns) is not None:
            return self.value(elem.find("./ns:LIMIT", namespaces= self.ns))
        return None
    
    def _list(self, elem):
        """
        <DVALUE xsi:type="list">
            <ELEMENT xsi:type="string">&quot;'str1'&quot;</ELEMENT>
            <ELEMENT xsi:type="string">String</ELEMENT>
        </DVALUE>
        """
        list_str = ''
        # for sub_elem in elem.findall("./ns:ELEMENT", namespaces= self.ns):
        #     list.append(self.value(sub_elem))
        list_str = self.value(elem.find("./ns:ELEMENT", namespaces= self.ns))
        return "["+list_str+"]"
    
    def _project_ref(self, elem):
        """
        <PROJECT-REF xsi:type="projectRef">
            <PROJECT-PATH xsi:type="string">Interface_0625/CANTest_LZCU.prj</PROJECT-PATH>
        </PROJECT-REF>
        """
        if elem.find("./ns:PROJECT-PATH", namespaces= self.ns) is not None:
            return self.value(elem.find("./ns:PROJECT-PATH", namespaces= self.ns))
        return None
    
    def _touch_input_action(self, elem):
        """
        <TOUCH-INPUT-ACTION xsi:type="swipeInputAction">
            <POS-X xsi:type="expressionQuantity">
                <VALUE format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">7</VALUE>
                </VALUE>
                <UNIT xsi:type="string">%</UNIT>
            </POS-X>
            <POS-Y xsi:type="expressionQuantity">
                <VALUE format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">25</VALUE>
                </VALUE>
                <UNIT xsi:type="string">%</UNIT>
            </POS-Y>
            <SWIPED-POS-X xsi:type="expressionQuantity">
                <VALUE format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">7</VALUE>
                </VALUE>
                <UNIT xsi:type="string">%</UNIT>
            </SWIPED-POS-X>
            <SWIPED-POS-Y xsi:type="expressionQuantity">
                <VALUE format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">74</VALUE>
                </VALUE>
                <UNIT xsi:type="string">%</UNIT>
            </SWIPED-POS-Y>
            <SWIPE-DURATION xsi:type="expressionQuantity">
                <VALUE format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">500</VALUE>
                </VALUE>
                <UNIT xsi:type="string">ms</UNIT>
            </SWIPE-DURATION>
        </TOUCH-INPUT-ACTION>
        """
        touch_input_action = TouchInputAction()
        if elem.find("./ns:POS-X", namespaces= self.ns) is not None:
            touch_input_action.pos_x = self.value(elem.find("./ns:POS-X", namespaces= self.ns))
            touch_input_action.pos_x_unit = self.value(elem.find("./ns:POS-X/ns:UNIT", namespaces= self.ns))
        if elem.find("./ns:POS-Y", namespaces= self.ns) is not None:
            touch_input_action.pos_y = self.value(elem.find("./ns:POS-Y", namespaces= self.ns))
            touch_input_action.pos_y_unit = self.value(elem.find("./ns:POS-Y/ns:UNIT", namespaces= self.ns))
        if elem.find("./ns:SWIPED-POS-X", namespaces= self.ns) is not None:
            touch_input_action.swiped_x = self.value(elem.find("./ns:SWIPED-POS-X", namespaces= self.ns))
            touch_input_action.swiped_x_unit = self.value(elem.find("./ns:SWIPED-POS-X/ns:UNIT", namespaces= self.ns))
        if elem.find("./ns:SWIPED-POS-Y", namespaces= self.ns) is not None:
            touch_input_action.swiped_y = self.value(elem.find("./ns:SWIPED-POS-Y", namespaces= self.ns))
            touch_input_action.swiped_y_unit = self.value(elem.find("./ns:SWIPED-POS-Y/ns:UNIT", namespaces= self.ns))
        if elem.find("./ns:SWIPE-DURATION", namespaces= self.ns) is not None:
            touch_input_action.duration = self.value(elem.find("./ns:SWIPE-DURATION", namespaces= self.ns))
            touch_input_action.duration_unit = self.value(elem.find("./ns:SWIPE-DURATION/ns:UNIT", namespaces= self.ns))
        if elem.find("./ns:HOLD-DURATION", namespaces= self.ns) is not None:
            touch_input_action.duration = self.value(elem.find("./ns:HOLD-DURATION", namespaces= self.ns))
            touch_input_action.duration_unit = self.value(elem.find("./ns:HOLD-DURATION/ns:UNIT", namespaces= self.ns))
        return touch_input_action
        
    def _expression_quantity(self, elem):
        """
        <VALUE format-rev="2" xsi:type="valueBaseExpression">
            <VALUE xsi:type="integer">7</VALUE>
        </VALUE>
        """
        if elem.find("./ns:VALUE", namespaces= self.ns) is not None:
            return self.value(elem.find("./ns:VALUE", namespaces= self.ns))
        if elem.find("./ns:UNIT", namespaces= self.ns) is not None:
            return f"{self.value(elem.find('./ns:UNIT', namespaces= self.ns))}"
        return None
        
        
    def _local_artifact_reference(self, elem):
        """
        <DATABASE xsi:type="localArtifactReference">
            <PATH xsi:type="string">E:/04_CANDBC/02_MX11/MX11_DBC/MX11_1.5_ZCUCANFD_240302.dbc</PATH>
        </DATABASE>
        """
        if elem.find("./ns:PATH", namespaces= self.ns) is not None:
            return self.value(elem.find("./ns:PATH", namespaces= self.ns))
        return None
    
    
    def _image_filters(self, elem):
        """
        <FILTERS xsi:type="imageFilters">
            <ELEMENT xsi:type="imageFilterReference">
                <NAME xsi:type="string">Black / White Filter</NAME>
            </ELEMENT>
        </FILTERS>
        """
        image_filters = []
        for elem in elem.findall("./ns:ELEMENT", namespaces= self.ns):
            image_filters.append(self._image_filter_reference(elem))
        return image_filters
    
    def _image_filter_reference(self, elem):
        """
        <ELEMENT xsi:type="imageFilterReference">
            <NAME xsi:type="string">Black / White Filter</NAME>
            <ID xsi:type="string">565448ce-fea9-4636-8a91-5f5ab2e1ce36</ID>
            <ARGUMENTS xsi:type="imageFilterArguments">
                <ARGUMENTS>
                    <ELEMENT xsi:type="imageFilterArgument">
                        <NAME xsi:type="string">Threshold</NAME>
                        <VALUE format-rev="2" xsi:type="valueBaseExpression">
                            <VALUE xsi:type="integer">150</VALUE>
                        </VALUE>
                        <DESCRIPTION xsi:type="string">Threshold value. (Range from 0 - 255, use -1 for Otsu algorithm)</DESCRIPTION>
                    </ELEMENT>
                </ARGUMENTS>
            </ARGUMENTS>
        </ELEMENT>
        """
        image_filter_reference = {}
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            image_filter_reference["name"] = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        if elem.find("./ns:ID", namespaces= self.ns) is not None:
            image_filter_reference["id"] = self.value(elem.find("./ns:ID", namespaces= self.ns))
        if elem.find("./ns:ARGUMENTS", namespaces= self.ns) is not None:
            image_filter_reference["arguments"] = self._image_filter_arguments(elem.find("./ns:ARGUMENTS", namespaces= self.ns))
        return image_filter_reference
    
    def _image_filter_arguments(self, elem):
        """
        <ARGUMENTS xsi:type="imageFilterArguments">
            <ARGUMENTS>
                <ELEMENT xsi:type="imageFilterArgument">
                    <NAME xsi:type="string">Threshold</NAME>
                    <VALUE format-rev="2" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="integer">150</VALUE>
                    </VALUE>
                    <DESCRIPTION xsi:type="string">Threshold value. (Range from 0 - 255, use -1 for Otsu algorithm)</DESCRIPTION>
                </ELEMENT>
            </ARGUMENTS>
        </ARGUMENTS>
        """
        image_filter_arguments = {}
        if elem.find("./ns:ARGUMENTS", namespaces= self.ns) is not None:
            image_filter_arguments["arguments"] = self._image_filter_argument(elem.find("./ns:ARGUMENTS/ns:ELEMENT", namespaces= self.ns))
        return image_filter_arguments
    
    def _image_filter_argument(self, elem): 
        """
        <ELEMENT xsi:type="imageFilterArgument">
            <NAME xsi:type="string">Threshold</NAME>
            <VALUE format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">150</VALUE>
            </VALUE>
        </ELEMENT>
        """
        image_filter_argument = {}
        if elem.find("./ns:NAME", namespaces= self.ns) is not None:
            image_filter_argument["name"] = self.value(elem.find("./ns:NAME", namespaces= self.ns))
        if elem.find("./ns:VALUE", namespaces= self.ns) is not None:
            image_filter_argument["value"] = self.value(elem.find("./ns:VALUE", namespaces= self.ns))
        if elem.find("./ns:DESCRIPTION", namespaces= self.ns) is not None:
            image_filter_argument["description"] = self.value(elem.find("./ns:DESCRIPTION", namespaces= self.ns))
        return image_filter_argument
    ################################    trace    ####################################
    
   
    
    
    
        
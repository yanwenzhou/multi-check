import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))
from .ValueExpression import ValueExpression 
from .evaluation import Evaluation
from .mapping import Mapping
import xml.etree.ElementTree as ET
from ..model.ts import TS

ns = {"ns": "http://www.tracetronic.de/xml/ecu-test", "xsi": "http://www.w3.org/2001/XMLSchema-instance"}

class PkgStep():  

    def __init__(self) -> None:
        self.ve = ValueExpression()
        self.Eva = Evaluation()
        self.pkg_path = ''

    def parse_steps(self,xml_filename):

        self.pkg_path = xml_filename
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        test_steps = []

        # 只遍历最上层的step
        for test_step_elem in root.findall("./ns:TESTSTEPS/ns:TESTSTEP", namespaces=ns):
            self.teststep(test_step_elem,test_steps,'ts','True',None)

        return test_steps


    def teststep(self,teststep_elem,step_msg,pos,enable,parent_id):
        # 获取步骤类型和关键参数
        teststep_type = teststep_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        
        msg = None
        substep_tags = ["ns:TESTSTEP"]

        # 通用属性
        ts = TS.creat_ts(teststep_type)
        ts.id = teststep_elem.get("id")
        ts.parent_id = parent_id

        if ts.id == "1a0d3f56-1d27-4dc4-b8b6-9cda56c8cea7":
            a = 1
        if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
            ts.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))
        if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
            ts.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        match teststep_type:
            case "utility-2752ad1e-4fef-11dc-81d4-0013728784ee":
                msg = self.step_block(teststep_elem, ts)

            case "utility-fd32d18b-c16d-45ca-9934-f8bffe11fcc3":
                msg = self.step_block(teststep_elem, ts)

            case "utility-0d2ac4dc-1d8f-4182-81d1-a5d5ca74a44f":
                msg = self.step_postcondblock(teststep_elem, ts)

            case "utility-4115fa00-5f3c-11df-8a53-001c233b3528":
                msg = self.step_calculation(teststep_elem, ts)

            case "utility-3609c41e-4fef-11dc-899a-0013728784ee":
                msg = self.step_if(teststep_elem, ts)
                substep_tags.append("ns:THEN")
                substep_tags.append("ns:ELSE")

            case "utility-3da58cf0-4fef-11dc-be56-0013728784ee":
                msg = self.step_loop(teststep_elem, ts)

            case "utility-2fb63e30-6816-11e5-bfd3-4851b798ee63":
                msg = self.step_mutlcheck(teststep_elem, ts)

            case "utility-62d5a961-4fef-11dc-9944-0013728784ee":
                msg = self.step_wait(teststep_elem, ts)

            case "utility-1f4de951-4fef-11dc-969a-0013728784ee":
                msg = self.step_comment(teststep_elem, ts)

            case "utility-4f3c5500-f0f5-11dc-b88f-001b24fa84be":
                msg = self.step_tsreturn(teststep_elem, ts)

            case "utility-11b0144f-4e4f-11e0-b968-1c659df540cc":
                msg = self.step_tsbreak(teststep_elem, ts)

            case "utility-76450221-6872-11e1-8167-8e9c3c2867f2":
                msg = self.step_tscontinue(teststep_elem, ts)

            case "utility-c6aa4f70-f037-11dc-9d16-001b24fa84be":
                msg = self.step_tsexit(teststep_elem, ts)

            case "utility-83517ac0-9f53-11dd-9c62-001b24fa84be":
                msg = self.step_tsswitchcase(teststep_elem, ts)

            case "utility-07b0bf30-f329-11e4-9d66-3402860ed21e":
                msg = self.step_tsswitchdefcase(teststep_elem, ts)

            case "utility-f9f253f0-0ad6-11dd-890b-001a6bc47c7f":
                msg = self.step_tsifdef(teststep_elem, ts)

            case "utility-83517ac0-9f53-11dd-9c62-001b24fa84bf":
                msg = self.step_tsreacton(teststep_elem, ts)

            case "utility-6e48fb4f-c07b-11dd-9499-001a6bc47c7f":
                msg = self.step_tsbitextract(teststep_elem, ts)
            
            case "utility-62d5a961-4fef-11dc-9944-0013728784ef":
                msg = self.step_tswaitforuser(teststep_elem, ts)

            case "tsRead":
                msg = self.step_read(teststep_elem, ts)

            case "tsWrite":
                msg = self.step_write(teststep_elem, ts)

            case "tsPackage":
                msg = self.step_package(teststep_elem, ts)
            
            case "tsPackageCall":
                msg = self.step_tsPackageCall(teststep_elem, ts)

            case "TsPackage":
                msg = self.step_package(teststep_elem, ts)
                
            case "caseNode":
                msg = self.step_caseNode(teststep_elem, ts)

            case "caseDefNode":
                msg = self.step_caseDefNode(teststep_elem, ts)
            
            case "ifThenElseNode":
                msg = self.step_ifthenelse_node(teststep_elem, ts)

            case "tsXaCallIOControlReturnControlToECU":
                msg = self.step_xaCallRead(teststep_elem, ts)

            case "tsXaCallIOControlShortTermAdjustment":
                msg = self.step_xaCallRead(teststep_elem, ts)

            case "tsXaCallRead":
                msg = self.step_xaCallRead(teststep_elem, ts)

            case "tsXaCall":
                msg = self.step_xaCallRead(teststep_elem, ts)
            
            case "tsJob":
                msg = self.step_tsJob(teststep_elem, ts)
                
            case "tsTouchInput":
                msg = self.step_tsTouchInput(teststep_elem, ts)
            
            case "tsReadImage":
                msg = self.step_tsReadImage(teststep_elem, ts)
            
            case _:
                print(f'出现未解析的step：{teststep_type}')

        if msg is not None:
            step_msg.append(msg)
        else:
            step_msg.append(ts)

        parent_id = ts.id
        # 递归处理子步骤
        for substep_tag in substep_tags:
            for substep_elem in teststep_elem.findall(substep_tag, namespaces=ns):
                self.teststep(substep_elem, step_msg, pos, enable, parent_id)
                

    def step_block(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="3" id="13ef3869-03b2-46cf-bfc8-57babc31be87" name="TsBlock" xsi:type="utility-2752ad1e-4fef-11dc-81d4-0013728784ee">
			<ACTION xsi:type="I18NItem">
				<MULTILANGDATA>
					<ELEMENT dkey="en_US">
						<DVALUE xsi:type="string">first block</DVALUE>
					</ELEMENT>
				</MULTILANGDATA>
				<INITIAL-LANGUAGE xsi:type="string">en_US</INITIAL-LANGUAGE>
			</ACTION>
		</TESTSTEP>
        """

        # block  = pstore.TsBlock()
        # block.parent_id = ts.parent_id
        # block.id = teststep_elem.get("id")
        # # 是否存在断点 <BREAKPOINT xsi:type="boolean">True</BREAKPOINT>
        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     block.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     block.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:ACTION", namespaces=ns) is not None:
            ts.action = self.ve.value(teststep_elem.find("./ns:ACTION", namespaces=ns))

        if teststep_elem.find("./ns:PARAMETER", namespaces=ns) is not None:
            ts.parameter = self.ve.value(teststep_elem.find("./ns:PARAMETER", namespaces=ns))

        if teststep_elem.find("./ns:EXPECTATION-VALUE", namespaces=ns) is not None:
            ts.expection_value = self.ve.value(teststep_elem.find("./ns:EXPECTATION-VALUE", namespaces=ns))

        return ts


    def step_postcondblock(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="2" id="652bd2d0-ea73-4c28-894b-a787cc800694" name="TsPostcondBlock" xsi:type="utility-0d2ac4dc-1d8f-4182-81d1-a5d5ca74a44f">
			<ACTION xsi:type="I18NItem">
				<MULTILANGDATA>
					<ELEMENT dkey="de_DE">
						<DVALUE xsi:type="string">Postcondition</DVALUE>
					</ELEMENT>
					<ELEMENT dkey="en_US">
						<DVALUE xsi:type="string">Postcondition</DVALUE>
					</ELEMENT>
				</MULTILANGDATA>
				<INITIAL-LANGUAGE xsi:type="string">en_US</INITIAL-LANGUAGE>
			</ACTION>
			<EFFECT-TEST-RESULT xsi:type="boolean">False</EFFECT-TEST-RESULT>
		</TESTSTEP>
        """
        # block  = pstore.TsPostcondBlock()
        # block.parent_id = ts.parent_id
        # block.id = teststep_elem.get("id")
        # # 是否存在断点 <BREAKPOINT xsi:type="boolean">True</BREAKPOINT>
        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     block.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))
        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     block.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:ACTION", namespaces=ns) is not None:
            ts.action = self.ve.value(teststep_elem.find("./ns:ACTION", namespaces=ns))
        
        if teststep_elem.find("./ns:EFFECT-TEST-RESULT", namespaces=ns) is not None:
            ts.effect_test_result = self.ve.value(teststep_elem.find("./ns:EFFECT-TEST-RESULT", namespaces=ns))
        
        return ts


    def step_calculation(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="3" id="3d96494a-f967-4f03-8539-ea20f3ba9703" name="TsCalculation" xsi:type="utility-4115fa00-5f3c-11df-8a53-001c233b3528">
			<FORMULA xsi:type="binaryOpBaseExpression">
				<NAME xsi:type="string">BINARY_ADD</NAME>
				<FIRST-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="integer">5</VALUE>
				</FIRST-COMPONENT>
				<SECOND-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="integer">5</VALUE>
				</SECOND-COMPONENT>
			</FORMULA>
			<EXPECTATION-OPTION xsi:type="timelessOption">
				<EXPRESSION xsi:type="builtNumericExpression">
					<RELATION xsi:type="string">&lt;=</RELATION>
					<VALUE format-rev="2" xsi:type="valueBaseExpression">
						<VALUE xsi:type="integer">20</VALUE>
					</VALUE>
				</EXPRESSION>
			</EXPECTATION-OPTION>
		</TESTSTEP>
        """

        # calculation = pstore.TsCalculation()
        # calculation.parent_id = ts.parent_id
        # calculation.id = teststep_elem.get("id")
        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     calculation.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     calculation.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            """
            <VARIABLE-REFS>
				<VARIABLE-NAME dkey="default">
					<DVALUE xsi:type="string">setValue</DVALUE>
				</VARIABLE-NAME>
			</VARIABLE-REFS>
            """
            ts.variable_refs = self.ve.value(teststep_elem.find("./ns:VARIABLE-REFS/ns:VARIABLE-NAME/ns:DVALUE", namespaces=ns))
        
        if teststep_elem.find("./ns:FORMULA", namespaces=ns) is not None:
            ts.formula = str(self.ve.value(teststep_elem.find("./ns:FORMULA", namespaces=ns)))
        
        if teststep_elem.find("./ns:EXPECTATION-OPTION", namespaces=ns) is not None:
            ts.expection = self.Eva.time_option(teststep_elem.find("./ns:EXPECTATION-OPTION", namespaces=ns))

        if teststep_elem.find("./ns:INSTANCE-NAME", namespaces=ns) is not None:
            ts.instance_name = self.ve.value(teststep_elem.find("./ns:INSTANCE-NAME", namespaces=ns))

        if teststep_elem.find("./ns:SUCCESS-COMMENT", namespaces=ns) is not None:
            ts.success_comment = self.ve.value(teststep_elem.find("./ns:SUCCESS-COMMENT", namespaces=ns))

        if teststep_elem.find("./ns:FAILED-COMMENT", namespaces=ns) is not None:
            ts.failed_comment = self.ve.value(teststep_elem.find("./ns:FAILED-COMMENT", namespaces=ns))

        return ts
                

    def step_if(self, teststep_elem, ts):
        """
        <TESTSTEP id="7e6eb06c-51c1-4078-80c6-e7cd644d7672" name="TsIfThenElse" xsi:type="utility-3609c41e-4fef-11dc-899a-0013728784ee">
			<CONDITION format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="boolean">True</VALUE>
			</CONDITION>
        </TESTSTEP>
        """

        # ifthenelse = pstore.TsIfThenElse()
        # ifthenelse.parent_id = ts.parent_id
        # ifthenelse.id = teststep_elem.get("id")
        # ifthenelse.ts_type = teststep_elem.get('name')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     ifthenelse.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     ifthenelse.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:CONDITION", namespaces=ns) is not None:
            ts.condition = str(self.ve.value(teststep_elem.find("./ns:CONDITION", namespaces=ns)))

        return ts


    def step_ifthenelse_node(self, teststep_elem, ts):
        """
        <THEN id="0b63e2ad-eaf8-412f-9e48-86596b9996cf" xsi:type="ifThenElseNode">

        </THEN>
        """
        # ifthenelse = pstore.TsIfThenElse()
        # ifthenelse.parent_id = ts.parent_id
        # ifthenelse.id = teststep_elem.get("id")
        ts.ts_type = 'IfThenElseNode'
        ts.condition = 'then'

        if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
            ts.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
            ts.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.tag == "{http://www.tracetronic.de/xml/ecu-test}ELSE":
            ts.condition = 'else'

        return ts


    def step_loop(self, teststep_elem, ts):
        """
        <TESTSTEP id="5a1fc682-01c5-458c-811f-686d80064d9e" name="TsLoop" xsi:type="utility-3da58cf0-4fef-11dc-be56-0013728784ee">
			<VARIABLE-REFS>
				<VARIABLE-NAME dkey="default">
					<DVALUE xsi:type="string">loopCounter</DVALUE>
				</VARIABLE-NAME>
			</VARIABLE-REFS>
			<LOOP-COUNT format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">8</VALUE>
			</LOOP-COUNT>
			<START-VALUE format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">2</VALUE>
			</START-VALUE>
			<STEP-SIZE format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">1</VALUE>
			</STEP-SIZE>
			<START-CONDITION xsi:type="compareOpBaseExpression">
				<NAME xsi:type="string">&lt;</NAME>
				<FIRST-COMPONENT xsi:type="varBaseExpression">
					<NAME xsi:type="string">loopCounter</NAME>
				</FIRST-COMPONENT>
				<SECOND-COMPONENT format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="integer">4</VALUE>
				</SECOND-COMPONENT>
			</START-CONDITION>
		</TESTSTEP>
        """

        # loop = pstore.TsLoop()
        # loop.parent_id = ts.parent_id
        # loop.id = teststep_elem.get("id")

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     loop.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     loop.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        variable_ref_elem = teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns)
        if variable_ref_elem is not None:
            ts.variable_ref = variable_ref_elem.find("./ns:VARIABLE-NAME/ns:DVALUE", namespaces=ns).text

        if teststep_elem.find("./ns:LOOP-COUNT", namespaces=ns) is not None:
            loop_count_elem = teststep_elem.find("./ns:LOOP-COUNT", namespaces=ns)
            ts.loop_count = str(self.ve.value(loop_count_elem))

        if teststep_elem.find("./ns:START-VALUE", namespaces=ns) is not None:
            start_value_elem = teststep_elem.find("./ns:START-VALUE", namespaces=ns)
            ts.start_value = str(self.ve.value(start_value_elem))
        
        if teststep_elem.find("./ns:STEP-SIZE", namespaces=ns) is not None:
            step_size_elem = teststep_elem.find("./ns:STEP-SIZE", namespaces=ns)
            ts.step_size = str(self.ve.value(step_size_elem))

        if teststep_elem.find("./ns:STOP-CONDITION", namespaces=ns) is not None:
            stop_condition_elem = teststep_elem.find("./ns:STOP-CONDITION", namespaces=ns)
            ts.condition = 'stop'
            ts.condition_value = str(self.ve.value(stop_condition_elem))

        elif teststep_elem.find("./ns:START-CONDITION", namespaces=ns) is not None:
            start_condition_elem = teststep_elem.find("./ns:START-CONDITION", namespaces=ns)
            ts.condition = 'start'
            ts.condition_value = str(self.ve.value(start_condition_elem))
            
        return ts


    def step_mutlcheck(self, teststep_elem, ts):
        """
        <TESTSTEP id="687639aa-a4f7-4a9d-9f24-0aa5ca7a30a7" name="TsMultiCheck" xsi:type="utility-2fb63e30-6816-11e5-bfd3-4851b798ee63">
			<MATCHALL xsi:type="boolean">True</MATCHALL>
			<TIME-OPTION xsi:type="timelessOption">
				<EXPRESSION xsi:type="manualExpression">
					<BASE-EXPRESSION xsi:type="varBaseExpression">
						<NAME xsi:type="string">value</NAME>
					</BASE-EXPRESSION>
				</EXPRESSION>
			</TIME-OPTION>
		</TESTSTEP>
        """
        # mutlcheck = pstore.TsMultiCheck()
        # mutlcheck.parent_id = ts.parent_id
        # mutlcheck.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     mutlcheck.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     mutlcheck.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:MATCHALL", namespaces=ns) is not None:
            ts.matchall = self.ve.value(teststep_elem.find("./ns:MATCHALL", namespaces=ns))

        return ts


    def step_wait(self, teststep_elem, ts):
        """
        <TESTSTEP id="added52b-34a5-4305-8e12-59861eba3554" name="TsWait" xsi:type="utility-62d5a961-4fef-11dc-9944-0013728784ee">
			<TIME format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">333</VALUE>
			</TIME>
			<UNIT xsi:type="string">s</UNIT>
		</TESTSTEP>
        """

        # wait = pstore.TsWait()
        # wait.parent_id = ts.parent_id
        # wait.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     wait.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     wait.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:TIME", namespaces=ns) is not None:
            ts.time = str(self.ve.value(teststep_elem.find("./ns:TIME", namespaces=ns)))
            
        if teststep_elem.find("./ns:UNIT", namespaces=ns) is not None:
            ts.unit = self.ve.value(teststep_elem.find("./ns:UNIT", namespaces=ns))
            
        return ts


    def step_comment(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="1" id="31d65e86-f86f-4a30-93e6-15a283f7c5ec" name="TsComment" xsi:type="utility-1f4de951-4fef-11dc-969a-0013728784ee">
            <COMMENT-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="string">1</VALUE>
            </COMMENT-EXPRESSION>
            <COMMENT-VERDICT xsi:type="string">SUCCESS</COMMENT-VERDICT>
        </TESTSTEP>
        """
        
        # comment = pstore.TsComment()
        # comment.parent_id = ts.parent_id
        # comment.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     comment.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     comment.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:COMMENT-EXPRESSION", namespaces=ns) is not None:
            ts.comment_expression = self.ve.value(teststep_elem.find("./ns:COMMENT-EXPRESSION", namespaces=ns))
            
        if teststep_elem.find("./ns:COMMENT-VERDICT", namespaces=ns) is not None:
            ts.comment_verdict = self.ve.value(teststep_elem.find("./ns:COMMENT-VERDICT", namespaces=ns))

        return ts


    def step_tsreturn(self, teststep_elem, ts):
        """
        <TESTSTEP id="38eef737-8cfb-4c4a-a293-b5b2c8897ce4" name="TsReturn" xsi:type="utility-4f3c5500-f0f5-11dc-b88f-001b24fa84be">
            <BREAKPOINT xsi:type="boolean">True</BREAKPOINT>
            <RETURN-RESULT xsi:type="string">NONE</RETURN-RESULT>
		</TESTSTEP>
        """
        # tsreturn = pstore.TsReturn()
        # tsreturn.parent_id = ts.parent_id
        # tsreturn.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     tsreturn.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     tsreturn.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        # tsreturn.return_result = "false"
        if teststep_elem.find("./ns:RETURN-RESULT", namespaces=ns) is not None:
            ts.return_result = self.ve.value(teststep_elem.find("./ns:RETURN-RESULT", namespaces=ns))
            # to do
            # ts.return_result=return_result.replace('NONE','None').replace('SUCCESS','True').replace('FAILD','False').replace('ERROR','False').replace('INCONCLUSIVE','None')
        return ts


    def step_tsbreak(self, teststep_elem, ts):
        """
        <TESTSTEP id="8792679a-4e5a-4fab-82a0-38cd4e83be03" name="TsBreak" xsi:type="utility-11b0144f-4e4f-11e0-b968-1c659df540cc"/>
        """
        # tsbreak = pstore.TsBreakContinue()
        # tsbreak.parent_id = ts.parent_id
        # tsbreak.id = teststep_elem.get('id')
        # tsbreak.ts_type = teststep_elem.get('name')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     tsbreak.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     tsbreak.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        return ts


    def step_tscontinue(self, teststep_elem, ts):
        """
        <TESTSTEP id="53128207-90ca-4f7a-a3d9-b2b7e72469f8" name="TsContinue" xsi:type="utility-76450221-6872-11e1-8167-8e9c3c2867f2"/>
        """
        # tscontinue = pstore.TsBreakContinue()
        # tscontinue.parent_id = ts.parent_id
        # tscontinue.id = teststep_elem.get('id')
        # tscontinue.ts_type = teststep_elem.get('name')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     tscontinue.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     tscontinue.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        return ts


    def step_tsexit(self, teststep_elem, ts):
        """
        结束测试 - TsExit

        exit_type [end,abort]
        exit_result [none success inconclusive false error]
        comment_expr [end_test abort_test cancelled_error cancelled_swc cancelled_hw no_run_precondition failed passed N/A]
        end_project [true false]

        end test:测试停止
        abort test:中止测试
        cancelled error:由于错误取消
        cancelled sw:由于软件问题取消
        cancelled hw:硬件问题取消
        no run precondition:没有运行预条件然后取消
        """
        # tsexit = pstore.TsExit()
        # tsexit.parent_id = ts.parent_id
        # tsexit.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     tsexit.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     tsexit.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:EXIT-RESULT", namespaces=ns) is not None:
            ts.exit_result = self.ve.value(teststep_elem.find("./ns:EXIT-RESULT", namespaces=ns))
        if teststep_elem.find("./ns:END-PROJECT", namespaces=ns) is not None:
            ts.end_project = self.ve.value(teststep_elem.find("./ns:END-PROJECT", namespaces=ns))
        if teststep_elem.find("./ns:ABORT", namespaces=ns) is not None:
            ts.exit_type = self.ve.value(teststep_elem.find("./ns:ABORT", namespaces=ns))
        if teststep_elem.find("./ns:COMMENT-EXPR/ns:VALUE", namespaces=ns) is not None:
            ts.comment_expr = self.ve.value(teststep_elem.find("./ns:COMMENT-EXPR/ns:VALUE", namespaces=ns))

        return ts


    def step_tsswitchcase(self, teststep_elem, ts):
        """
        <TESTSTEP id="11b109c2-0b4b-474d-8b0c-b6eb79fac3ca" name="TsSwitchCase" xsi:type="utility-83517ac0-9f53-11dd-9c62-001b24fa84be">
			<SWITCH-VALUE xsi:type="functionBaseExpression">
				<COMPONENT xsi:type="varBaseExpression">
					<NAME xsi:type="string">int</NAME>
				</COMPONENT>
				<ARGUMENTS>
					<ARGUMENT xsi:type="varBaseExpression">
						<NAME xsi:type="string">first_num</NAME>
					</ARGUMENT>
				</ARGUMENTS>
			</SWITCH-VALUE>
		</TESTSTEP>
        """
        # switchcase = pstore.TsSwitchCase()
        # switchcase.parent_id = ts.parent_id
        # switchcase.id = teststep_elem.get('id')
        # switchcase.ts_type = 'TsSwitchCase'

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     switchcase.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     switchcase.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:SWITCH-VALUE", namespaces=ns) is not None:
            ts.switch_value = str(self.ve.value(teststep_elem.find("./ns:SWITCH-VALUE", namespaces=ns)))

        return ts


    def step_tsswitchdefcase(self, teststep_elem, ts):
        """
        跳转 - TsSwitchDefCase
        """
        # switchdefcase = pstore.TsSwitchCase()
        # switchdefcase.parent_id = ts.parent_id
        # switchdefcase.id = teststep_elem.get('id')
        # switchdefcase.ts_type = 'TsSwitchDefCase'

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     switchdefcase.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     switchdefcase.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:SWITCH-VALUE", namespaces=ns) is not None:
            ts.switch_value = str(self.ve.value(teststep_elem.find("./ns:SWITCH-VALUE", namespaces=ns)))

        return ts


    def step_tsreacton(self, teststep_elem, ts):
        """
         - TsReactOn
        """


    def step_tsifdef(self, teststep_elem, ts):
        """
         - TsIfDef
        """
        # ifdef = pstore.TsIfThenElse()
        # ifdef.parent_id = ts.parent_id
        # ifdef.id = teststep_elem.get('id')
        # ifdef.ts_type = 'TsIfDef'

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     ifdef.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     ifdef.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:CONDITION", namespaces=ns) is not None:
            ts.condition = str(self.ve.value(teststep_elem.find("./ns:CONDITION", namespaces=ns)))

        return ts


    def step_read(self, teststep_elem, ts):
        """
        <TESTSTEP id="27f70266-4ecf-4926-8f5f-7c08ca07f466" xsi:type="tsRead">
			<MAPPING-REF xsi:type="string">ACUWarnLampSts_ADASCANFD</MAPPING-REF>
            <VARIABLE-REFS>
                <VARIABLE-NAME dkey="default">
                    <DVALUE xsi:type="string">PWMOUT32_DO32</DVALUE>
                </VARIABLE-NAME>
            </VARIABLE-REFS>
			<EXPECTATION xsi:type="timelessOption">
				<EXPRESSION xsi:type="builtStringExpression">
					<CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
					<BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
						<VALUE xsi:type="string">Blinking</VALUE>
					</BASE-EXPRESSION>
				</EXPRESSION>
			</EXPECTATION>
			<METRIC format-rev="1" xsi:type="metricInfo">
				<VALUE-TYPE xsi:type="string">TEXT</VALUE-TYPE>
				<DATA-TYPE xsi:type="string">VALUE</DATA-TYPE>
			</METRIC>
		</TESTSTEP>
        数据写入 - tsRead
        """
        # tsread = pstore.TsRead()
        # tsread.parent_id = ts.parent_id
        # tsread.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     tsread.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     tsread.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:MAPPING-REF", namespaces=ns) is not None:
            ts.mapping_ref = self.ve.value(teststep_elem.find("./ns:MAPPING-REF", namespaces=ns))

        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            ts.variable_refs  = self.ve.value(teststep_elem.find("./ns:VARIABLE-REFS/ns:VARIABLE-NAME/ns:DVALUE", namespaces=ns))

        if teststep_elem.find("./ns:EXPECTATION", namespaces=ns) is not None:
            ts.expection = self.ve.value(teststep_elem.find("./ns:EXPECTATION", namespaces=ns))

        if teststep_elem.find("./ns:METRIC", namespaces=ns) is not None:
            ts.metric = self.ve.value(teststep_elem.find("./ns:METRIC", namespaces=ns))

        return ts


    def step_write(self, teststep_elem, ts):
        """
        <TESTSTEP id="9755369e-9b27-4181-9860-cf160350af10" xsi:type="tsWrite">
			<MAPPING-REF xsi:type="string">I_A_FrontRightBlowFaceTemp</MAPPING-REF>
			<VALUE xsi:type="expressionValue">
				<DATA format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="float">0.0</VALUE>
				</DATA>
			</VALUE>
			<METRIC format-rev="1" xsi:type="metricInfo">
				<VALUE-TYPE xsi:type="string">BITS</VALUE-TYPE>
				<DATA-TYPE xsi:type="string">VALUE</DATA-TYPE>
			</METRIC>
		</TESTSTEP>
        数据写入 - tsWrite
        """
        # tswrite = pstore.TsWrite()
        # tswrite.parent_id = ts.parent_id
        # tswrite.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     tswrite.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     tswrite.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:MAPPING-REF", namespaces=ns) is not None:
            ts.mapping_ref = self.ve.value(teststep_elem.find("./ns:MAPPING-REF", namespaces=ns))

        if teststep_elem.find("./ns:VALUE", namespaces=ns) is not None:
            ts.value = self.ve.value(teststep_elem.find("./ns:VALUE", namespaces=ns))
        
        if teststep_elem.find("./ns:METRIC", namespaces=ns) is not None:
            ts.metric = self.ve.value(teststep_elem.find("./ns:METRIC", namespaces=ns))

        return ts
    

    def step_package(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="3" id="deedc195-01d2-483b-b7e9-2b3320e20650" xsi:type="tsPackage">
            <VARIABLE-REFS>
				<VARIABLE-NAME dkey="c">
					<DVALUE xsi:type="string">a</DVALUE>
				</VARIABLE-NAME>
				<VARIABLE-NAME dkey="d">
					<DVALUE xsi:type="string">w</DVALUE>
				</VARIABLE-NAME>
			</VARIABLE-REFS>
            <PACKAGE-REFERENCE xsi:type="expressionref">
                <PATH-EXPRESSION format-rev="1" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="string">PwrModSts_Set.pkg</VALUE>
                </PATH-EXPRESSION>
            </PACKAGE-REFERENCE>
            <PARAM-ASSIGNMENTS>
                <ASSIGNMENT dkey="PwrModSts_Check">
                    <DVALUE format-rev="1" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="string">Enum_PwrModSts_RUN</VALUE>
                    </DVALUE>
                </ASSIGNMENT>
                <ASSIGNMENT dkey="PwrModSts_Enable">
                    ...
                </ASSIGNMENT>
            </PARAM-ASSIGNMENTS>
            <ALTERNATIVE-MAPPING-SPACE format-rev="1" xsi:type="mappingSpace">
                <MAPPING-ITEM format-rev="2" xsi:type="mappingItem">
                    <ID xsi:type="string">PwrModSts</ID>
                    <XACCESS xsi:type="xaReadWriteValueVariable">
                        <MAPPING-ENUM xsi:type="vtabInfoEmpty"/>
                    </XACCESS>
                    <AUTO-GENERATED xsi:type="boolean">False</AUTO-GENERATED>
                    <CATEGORY xsi:type="string">Signal_CANFD</CATEGORY>
                </MAPPING-ITEM>
                <MAPPING-ITEM format-rev="2" xsi:type="mappingItem">
                    ...
                </MAPPING-ITEM>
            </ALTERNATIVE-MAPPING-SPACE>
        </TESTSTEP>
        
        导入其他pkg步骤 - tsPackage
        """
        # package = pstore.TsPackage()
        # package.parent_id = ts.parent_id
        # package.id = teststep_elem.get('id')

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     package.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     package.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))
        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            for var_elem in teststep_elem.findall("./ns:VARIABLE-REFS/ns:VARIABLE-NAME", namespaces=ns):
                ts.var[var_elem.get('dkey')] = self.ve.value(var_elem.find("./ns:DVALUE",namespaces=ns))

        if teststep_elem.find("./ns:PACKAGE-REFERENCE", namespaces=ns) is not None:
            path = self.ve.value(teststep_elem.find("./ns:PACKAGE-REFERENCE", namespaces=ns))
            path = path.replace("'",'')
            ts.path = path+'.json'

        if teststep_elem.find("./ns:PARAM-ASSIGNMENTS", namespaces=ns) is not None:
            assigment_elems = teststep_elem.findall("./ns:PARAM-ASSIGNMENTS/ns:ASSIGNMENT", namespaces=ns)
            for assigment_elem in assigment_elems:
                ts.params[assigment_elem.get('dkey')] = self.ve.value(assigment_elem.find("./ns:DVALUE",namespaces=ns))

        if teststep_elem.find("./ns:ALTERNATIVE-MAPPING-SPACE", namespaces=ns) is not None:
            mapping_elems = teststep_elem.findall("./ns:ALTERNATIVE-MAPPING-SPACE/ns:MAPPING-ITEM", namespaces=ns)
            for mapping_elem in mapping_elems:
                mapping_item = Mapping().parse_mapping_item(mapping_elem)
                ts.mapping_items[mapping_item.id] = mapping_item.to_dict()

        return ts

    def step_tsPackageCall(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="3" id="deedc195-01d2-483b-b7e9-2b3320e20650" xsi:type="tsPackage">
            <VARIABLE-REFS>
				<VARIABLE-NAME dkey="c">
					<DVALUE xsi:type="string">a</DVALUE>
				</VARIABLE-NAME>
				<VARIABLE-NAME dkey="d">
					<DVALUE xsi:type="string">w</DVALUE>
				</VARIABLE-NAME>
			</VARIABLE-REFS>
            <MAPPING-REF xsi:type="string">四门两盖关闭</MAPPING-REF>
            <PARAM-ASSIGNMENTS>
                <ASSIGNMENT dkey="PwrModSts_Check">
                    <DVALUE format-rev="1" xsi:type="valueBaseExpression">
                        <VALUE xsi:type="string">Enum_PwrModSts_RUN</VALUE>
                    </DVALUE>
                </ASSIGNMENT>
                <ASSIGNMENT dkey="PwrModSts_Enable">
                    ...
                </ASSIGNMENT>
            </PARAM-ASSIGNMENTS>
            <ALTERNATIVE-MAPPING-SPACE format-rev="1" xsi:type="mappingSpace">
                <MAPPING-ITEM format-rev="2" xsi:type="mappingItem">
                    <ID xsi:type="string">PwrModSts</ID>
                    <XACCESS xsi:type="xaReadWriteValueVariable">
                        <MAPPING-ENUM xsi:type="vtabInfoEmpty"/>
                    </XACCESS>
                    <AUTO-GENERATED xsi:type="boolean">False</AUTO-GENERATED>
                    <CATEGORY xsi:type="string">Signal_CANFD</CATEGORY>
                </MAPPING-ITEM>
                <MAPPING-ITEM format-rev="2" xsi:type="mappingItem">
                    ...
                </MAPPING-ITEM>
            </ALTERNATIVE-MAPPING-SPACE>
        </TESTSTEP>
        
        导入其他pkg步骤 - tsPackage
        """
        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            for var_elem in teststep_elem.findall("./ns:VARIABLE-REFS/ns:VARIABLE-NAME", namespaces=ns):
                ts.var[var_elem.get('dkey')] = self.ve.value(var_elem.find("./ns:DVALUE",namespaces=ns))

        if teststep_elem.find("./ns:MAPPING-REF", namespaces=ns) is not None:
            path = self.ve.value(teststep_elem.find("./ns:MAPPING-REF", namespaces=ns))
            # path = path.replace("'",'')
            ts.mapping_ref = path

        if teststep_elem.find("./ns:PARAM-ASSIGNMENTS", namespaces=ns) is not None:
            assigment_elems = teststep_elem.findall("./ns:PARAM-ASSIGNMENTS/ns:ASSIGNMENT", namespaces=ns)
            for assigment_elem in assigment_elems:
                ts.params[assigment_elem.get('dkey')] = self.ve.value(assigment_elem.find("./ns:DVALUE",namespaces=ns))

        if teststep_elem.find("./ns:ALTERNATIVE-MAPPING-SPACE", namespaces=ns) is not None:
            mapping_elems = teststep_elem.findall("./ns:ALTERNATIVE-MAPPING-SPACE/ns:MAPPING-ITEM", namespaces=ns)
            for mapping_elem in mapping_elems:
                mapping_item = Mapping().parse_mapping_item(mapping_elem)
                ts.mapping_items[mapping_item.id] = mapping_item.to_dict()

        return ts
    

    def step_caseNode(self, teststep_elem, ts):
        """
        <TESTSTEP id="14855bd4-89a2-439e-a007-b899030f3993" xsi:type="caseNode">
            <CASE-VALUE format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">0</VALUE>
            </CASE-VALUE>
            <IS-DEFAULT xsi:type="boolean">True</IS-DEFAULT>
        </TESTSTEP>
        """
        # casenode = pstore.caseNode()
        # casenode.parent_id = ts.parent_id
        # casenode.id = teststep_elem.get('id')
        # casenode.ts_type = 'caseNode'

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     casenode.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     casenode.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:CASE-VALUE", namespaces=ns) is not None:
            ts.case_value = self.ve.value(teststep_elem.find("./ns:CASE-VALUE", namespaces=ns))

        if teststep_elem.find("./ns:IS-DEFAULT", namespaces=ns) is not None:
            ts.isdefault = self.ve.value(teststep_elem.find(".//ns:IS-DEFAULT", namespaces=ns))

        return ts


    def step_caseDefNode(self, teststep_elem, ts):
        """
        - caseDefNode
        """
        # casedefnode = pstore.caseNode()
        # casedefnode.parent_id = ts.parent_id
        # casedefnode.id = teststep_elem.get('id')
        # casedefnode.ts_type = 'caseDefNode'

        # if teststep_elem.find("./ns:BREAKPOINT", namespaces=ns) is not None:
        #     casedefnode.breakpoint = self.ve.value(teststep_elem.find("./ns:BREAKPOINT", namespaces=ns))

        # if teststep_elem.find("./ns:ENABLED", namespaces=ns) is not None:
        #     casedefnode.enable = self.ve.value(teststep_elem.find("./ns:ENABLED", namespaces=ns))

        if teststep_elem.find("./ns:CASE-VALUE", namespaces=ns) is not None:
            ts.case_value = self.ve.value(teststep_elem.find("./ns:CASE-VALUE", namespaces=ns))

        if teststep_elem.find("./ns:IS-DEFAULT", namespaces=ns) is not None:
            ts.isdefault = self.ve.value(teststep_elem.find("./ns:IS-DEFAULT", namespaces=ns))

        return ts    

    
    def step_xaCallRead(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="1" id="4ac52fcc-007d-4114-b455-c1a026d4945d" xsi:type="tsXaCallRead">
            <MAPPING-REF xsi:type="string">FunctionalECU/Power_Mode_D002</MAPPING-REF>
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
            <RETURN xsi:type="callReturn">
                <NAME xsi:type="string">Power_ModePwrModSts_D002</NAME>
                <METRIC format-rev="1" xsi:type="metricInfo">
                    <Z-UNIT xsi:type="string">u_none</Z-UNIT>
                    <VALUE-TYPE xsi:type="string">TEXT</VALUE-TYPE>
                    <DATA-TYPE xsi:type="string">VALUE</DATA-TYPE>
                </METRIC>
                <SAVE-IN xsi:type="varBaseExpression">
                    <NAME xsi:type="string">Power_ModePwrModSts_D002</NAME>
                </SAVE-IN>
                <EXPECTATION xsi:type="readOnlyExpression"/>
            </RETURN>
        </TESTSTEP>
        """
        # xacallread = pstore.TsXaCallRead()
        # xacallread.parent_id = ts.parent_id
        # xacallread.id = teststep_elem.get('id')
        # xacallread.ts_type = teststep_elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        if teststep_elem.find("./ns:MAPPING-REF", namespaces=ns) is not None:
            ts.mapping_ref = self.ve.value(teststep_elem.find("./ns:MAPPING-REF", namespaces=ns))
        
        if teststep_elem.find("./ns:RETURN", namespaces=ns) is not None:
            ts.call_return = self.ve._call_return(teststep_elem.find("./ns:RETURN", namespaces=ns))
        
        if teststep_elem.find("./ns:PARAMETER", namespaces=ns) is not None:
            ts.parameter = self.ve._call_parameter(teststep_elem.find("./ns:PARAMETER", namespaces=ns))
        
        return ts
    

    def step_tsbitextract(self, teststep_elem, ts):
        """
        <TESTSTEP id="75e4c019-35ee-4e58-89d8-8c3ee8c52260" name="TsBitExtract" xsi:type="utility-6e48fb4f-c07b-11dd-9499-001a6bc47c7f">
            <VARIABLE-REFS>
                <VARIABLE-NAME dkey="default">
                    <DVALUE xsi:type="string">BLEM2VCCDForLocn17</DVALUE>
                </VARIABLE-NAME>
            </VARIABLE-REFS>
            <DATA xsi:type="sliceBaseExpression">
                <COMPONENT xsi:type="varBaseExpression">
                    <NAME xsi:type="string">Dummy2</NAME>
                </COMPONENT>
                <START format-rev="1" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">4</VALUE>
                </START>
                <STOP format-rev="1" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">12</VALUE>
                </STOP>
            </DATA>
            <START-BIT xsi:type="integer">24</START-BIT>
            <BIT-LENGTH xsi:type="integer">32</BIT-LENGTH>
            <BYTE-ORDER xsi:type="string">Motorola</BYTE-ORDER>
        </TESTSTEP>
        """
        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            ts.variable_ref  = self.ve.value(teststep_elem.find("./ns:VARIABLE-REFS/ns:VARIABLE-NAME/ns:DVALUE", namespaces=ns))
        
        if teststep_elem.find("./ns:DATA", namespaces=ns) is not None:
            ts.data = self.ve.value(teststep_elem.find("./ns:DATA", namespaces=ns))
        
        if teststep_elem.find("./ns:START-BIT", namespaces=ns) is not None:
            ts.start_bit = self.ve.value(teststep_elem.find("./ns:START-BIT", namespaces=ns))
        
        if teststep_elem.find("./ns:BIT-LENGTH", namespaces=ns) is not None:
            ts.bit_length = self.ve.value(teststep_elem.find("./ns:BIT-LENGTH", namespaces=ns))
        
        if teststep_elem.find("./ns:BYTE-ORDER", namespaces=ns) is not None:
            ts.byte_order = self.ve.value(teststep_elem.find("./ns:BYTE-ORDER", namespaces=ns))
        
        return ts


    def step_tswaitforuser(self, teststep_elem, ts):
        """
        <TESTSTEP id="657bcd4c-bbb4-40b7-b97f-4212b83118eb" name="TsWaitForUser" xsi:type="utility-62d5a961-4fef-11dc-9944-0013728784ef">
            <MAX-WAIT-TIME format-rev="1" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">600000</VALUE>
            </MAX-WAIT-TIME>
            <QUERY-EVALUATION xsi:type="boolean">True</QUERY-EVALUATION>
            <INFO-TEXT format-rev="1" xsi:type="valueBaseExpression">
                <VALUE xsi:type="string">用户检查是否报出DTC：AABE9E，信号是否变为0x3-Err。</VALUE>
            </INFO-TEXT>
            <VARIABLE-REFS>
                <VARIABLE-NAME dkey="default">
                    <DVALUE xsi:type="string">input3</DVALUE>
                </VARIABLE-NAME>
            </VARIABLE-REFS>
        </TESTSTEP>
        """
        if teststep_elem.find("./ns:MAX-WAIT-TIME",namespaces=ns) is not None:
            ts.max_wait_time = self.ve.value(teststep_elem.find("./ns:MAX-WAIT-TIME", namespaces=ns))
        
        if teststep_elem.find("./ns:QUERY-EVALUATION", namespaces=ns) is not None:
            ts.query_evaluation = self.ve.value(teststep_elem.find("./ns:QUERY-EVALUATION", namespaces=ns))
        
        if teststep_elem.find("./ns:INFO-TEXT", namespaces=ns) is not None:
            ts.info_text = self.ve.value(teststep_elem.find("./ns:INFO-TEXT", namespaces=ns))
        
        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            ts.variable_ref = self.ve.value(teststep_elem.find("./ns:VARIABLE-REFS/ns:VARIABLE-NAME/ns:DVALUE", namespaces=ns))
        
        return ts


    def step_tsJob(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="4" id="1c4e89ec-4580-434a-b65c-e11834d3cca8" xsi:type="tsJob">
        <MAPPING-REF xsi:type="string">OpenKwp2000overIsoTpSession</MAPPING-REF>
        <VARIABLE-REFS>
            <VARIABLE-NAME dkey="default">
                <DVALUE xsi:type="string">SessionID</DVALUE>
            </VARIABLE-NAME>
        </VARIABLE-REFS>
        <JOB-PARAMETER xsi:type="tsJobParameter">
            <NAME xsi:type="string">AddressMode</NAME>
            <EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
                <VALUE xsi:type="integer">0</VALUE>
            </EXPRESSION>
        </JOB-PARAMETER>
        ...
        <EXPECTATION-OPTION xsi:type="timelessOption">
            <EXPRESSION xsi:type="builtNumericExpression">
                <RELATION xsi:type="string">==</RELATION>
                <VALUE format-rev="2" xsi:type="valueBaseExpression">
                    <VALUE xsi:type="integer">0</VALUE>
                </VALUE>
            </EXPRESSION>
        </EXPECTATION-OPTION>
        """
        # tsjob = pstore.TsJob()
        # tsjob.parent_id = ts.parent_id
        # tsjob.id = teststep_elem.get('id')
        # tsjob.ts_type = "tsJob"
        if teststep_elem.find("./ns:MAPPING-REF", namespaces=ns) is not None:
            ts.mapping_ref = self.ve.value(teststep_elem.find("./ns:MAPPING-REF", namespaces=ns))
        
        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            ts.variable_ref  = self.ve.value(teststep_elem.find("./ns:VARIABLE-REFS/ns:VARIABLE-NAME/ns:DVALUE", namespaces=ns))
        
        for job_param_elem in teststep_elem.findall("./ns:JOB-PARAMETER", namespaces=ns):
            ts.job_parameters.update(self.ve._job_parameter(job_param_elem))
        
        if teststep_elem.find("./ns:EXPECTATION-OPTION", namespaces=ns) is not None:
            ts.expection = self.ve._time_option(teststep_elem.find("./ns:EXPECTATION-OPTION", namespaces=ns))
        return ts

    def step_tsTouchInput(self, teststep_elem, ts):
        """
        <TESTSTEP id="93109929-d400-4810-bf13-2d90a3cd7f16" xsi:type="tsTouchInput">
            <MAPPING-REF xsi:type="string">CID/Image</MAPPING-REF>
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
        </TESTSTEP>
        """
        if teststep_elem.find("./ns:MAPPING-REF", namespaces=ns) is not None:
            ts.mapping_ref = self.ve.value(teststep_elem.find("./ns:MAPPING-REF", namespaces=ns))
        
        if teststep_elem.find("./ns:TOUCH-INPUT-ACTION", namespaces=ns) is not None:
            ts.action_type = teststep_elem.find("./ns:TOUCH-INPUT-ACTION", namespaces=ns).get("{http://www.w3.org/2001/XMLSchema-instance}type")
            ts.touch_input_action = self.ve._touch_input_action(teststep_elem.find("./ns:TOUCH-INPUT-ACTION", namespaces=ns))
        
        ts.name = ts.action_type.replace("swipeInputAction","Swipe").replace("tapInputAction","Tap").replace("holdInputAction","Hold") + ":" +ts.mapping_ref
        return ts


    def step_tsReadImage(self, teststep_elem, ts):
        """
        <TESTSTEP format-rev="1" id="80ab1db5-40fa-4113-a6e8-5137cca4ebb2" xsi:type="tsReadImage">
            <MAPPING-REF xsi:type="string">CID/Image</MAPPING-REF>
            <VARIABLE-REFS>
                <VARIABLE-NAME dkey="default">
                    <DVALUE xsi:type="string">pic1</DVALUE>
                </VARIABLE-NAME>
            </VARIABLE-REFS>
            <FILTERS>
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
                ...
            </FILTERS>
        </TESTSTEP>
        """
        if teststep_elem.find("./ns:MAPPING-REF", namespaces=ns) is not None:
            ts.mapping_ref = self.ve.value(teststep_elem.find("./ns:MAPPING-REF", namespaces=ns))
        
        if teststep_elem.find("./ns:VARIABLE-REFS", namespaces=ns) is not None:
            ts.variable_ref = self.ve.value(teststep_elem.find("./ns:VARIABLE-REFS/ns:VARIABLE-NAME/ns:DVALUE", namespaces=ns))
            
        if teststep_elem.find("./ns:FILTERS", namespaces=ns) is not None:
            ts.filters = self.ve._image_filters(teststep_elem.find("./ns:FILTERS", namespaces=ns))
            
        
        return ts
        
        


# def absolute_path(path1, path2):
#     abs_path1 = os.path.abspath(path1)
#     folder_path = os.path.dirname(abs_path1)
#     absolute_paths = folder_path.split('\\')
#     path2 = path2.replace("'","")
#     relative_paths = path2.split("/")
#     for relative_path in relative_paths:
#         if relative_path == "..":
#             absolute_paths.pop()
#         else:
#             absolute_paths.append(relative_path)
#     absolute_path2 = os.path.join(*absolute_paths).replace(":",":\\") + '.json'
#     return absolute_path2

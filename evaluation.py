import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import xml.etree.ElementTree as ET
from .ValueExpression import ValueExpression
from ..model.metric import Metric
from ..model.timeoption import TimeOption

ns = {"ns": "http://www.tracetronic.de/xml/ecu-test"}

class Evaluation():


    def __init__(self) -> None:
        self.ve = ValueExpression()

    def metric(self,elem):
        """
		<METRIC format-rev="1" xsi:type="metricInfo">
			<Z-UNIT xsi:type="string">u_none</Z-UNIT>
			<VALUE-TYPE xsi:type="string">PHYS</VALUE-TYPE>
			<DATA-TYPE xsi:type="string">VALUE</DATA-TYPE>
		</METRIC>
		"""
        metric_value = Metric()
        if elem.find("./ns:Z-UNIT", namespaces=ns) is not None:
            metric_value.unit = self.ve.value(elem.find("./ns:Z-UNIT", namespaces=ns))
        if elem.find("./ns:VALUE-TYPE", namespaces=ns) is not None:
            metric_value.value_type = self.ve.value(elem.find("./ns:VALUE-TYPE", namespaces=ns))
        if elem.find("./ns:DATA-TYPE", namespaces=ns) is not None:
            metric_value.data_type = self.ve.value(elem.find("./ns:DATA-TYPE", namespaces=ns))
        return metric_value


    def time_option(self,elem):
        type = elem.get("{http://www.w3.org/2001/XMLSchema-instance}type")
        time_option = TimeOption()

        time_option.time_type = type
        if elem.find("./ns:EXPRESSION", namespaces=ns) is not None:
            time_option.expression = self.ve.value(elem.find("./ns:EXPRESSION", namespaces=ns))
            
        
        if elem.find("./ns:POLLING-CYCLE", namespaces=ns) is not None:
            time_option.Polling_cycle = self.ve.value(elem.find("./ns:POLLING-CYCLE", namespaces=ns))

        if elem.find("./ns:POLLING-CYCLE-UNIT", namespaces=ns) is not None:
            time_option.Polling_cycle_unit = self.ve.value(elem.find("./ns:POLLING-CYCLE-UNIT", namespaces=ns))
        
        if elem.find("./ns:TIME", namespaces=ns) is not None:
            time_option.time = self.ve.value(elem.find("./ns:TIME", namespaces=ns))

        if elem.find("./ns:TIME-UNIT", namespaces=ns) is not None:
            time_option.time_unit = self.ve.value(elem.find("./ns:TIME-UNIT", namespaces=ns))

        if elem.find("./ns:TIMEOUT", namespaces=ns) is not None:
            time_option.Timeout = self.ve.value(elem.find("./ns:TIMEOUT", namespaces=ns))
            
        if elem.find("./ns:TIMEOUT-UNIT", namespaces=ns) is not None:
            time_option.Timeout_unit = self.ve.value(elem.find("./ns:TIMEOUT-UNIT", namespaces=ns))

        if elem.find("./ns:MINDURATION", namespaces=ns) is not None:
            time_option.Minimum_duration = self.ve.value(elem.find("./ns:MINDURATION", namespaces=ns))
        
        if elem.find("./ns:MINDURATION-UNIT", namespaces=ns) is not None:
            time_option.Minimum_duration_unit = self.ve.value(elem.find("./ns:MINDURATION-UNIT", namespaces=ns))

        return time_option
        # match type:
        #     case "timelessOption":
        #         return self.timeless_option(elem)
        #     case "finallyTrueOption":
        #         return self.finally_true_option(elem)
        #     case "generallyTrueOption":
        #         return self.generally_true_option(elem)
        #     case "trueForWithinOption":
        #         return self.true_for_with_in_option(elem)
        #     case "syncOnlyOption":
        #         return self.sync_only_option(elem)

    def timeless_option(self,elem):
        """
        <EXPECTATION-OPTION xsi:type="timelessOption">
            <EXPRESSION xsi:type="builtNumericExpression">
                <RELATION xsi:type="string">==</RELATION>
                <VALUE format-rev="2" xsi:type="valueBaseExpression">
                     <VALUE xsi:type="boolean">True</VALUE>
                </VALUE>
            </EXPRESSION>
        </EXPECTATION-OPTION>
        """

        if elem.find("./ns:EXPRESSION", namespaces=ns) is not None:
            return self.ve.value(elem.find("./ns:EXPRESSION", namespaces=ns))
    


    def finally_true_option(self,elem):
        """
        <EXPECTATION xsi:type="finallyTrueOption">
			<EXPRESSION xsi:type="builtStringExpression">
				<CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
				<BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="string">Blinking</VALUE>
				</BASE-EXPRESSION>
			</EXPRESSION>
            <POLLING-CYCLE format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">12</VALUE>
			</POLLING-CYCLE>
			<POLLING-CYCLE-UNIT xsi:type="string">s</POLLING-CYCLE-UNIT>
			<TIME format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">100</VALUE>
			</TIME>
            <TIME-UNIT xsi:type="string">ms</TIME-UNIT>
		</EXPECTATION>
        """
        


    def generally_true_option(self,elem):
        """
        <EXPECTATION xsi:type="generallyTrueOption">
			<EXPRESSION xsi:type="builtStringExpression">
				<CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
				<BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="string">Blinking</VALUE>
				</BASE-EXPRESSION>
			</EXPRESSION>
			<TIME format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">10</VALUE>
			</TIME>
            <TIME-UNIT xsi:type="string">ms</TIME-UNIT>
		</EXPECTATION>
        """


    def true_for_with_in_option(self,elem):
        """
        <EXPECTATION xsi:type="trueForWithinOption">
			<EXPRESSION xsi:type="builtStringExpression">
				<CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
				<BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="string">Blinking</VALUE>
				</BASE-EXPRESSION>
			</EXPRESSION>
			<TIMEOUT format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">1000</VALUE>
			</TIMEOUT>
			<MINDURATION format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">10</VALUE>
			</MINDURATION>
            <TIMEOUT-UNIT xsi:type="string">h</TIMEOUT-UNIT>
			<MINDURATION-UNIT xsi:type="string">min</MINDURATION-UNIT>
		</EXPECTATION>
        """


    def sync_only_option(self,elem):
        """
        <EXPECTATION xsi:type="syncOnlyOption">
			<EXPRESSION xsi:type="builtStringExpression">
				<CASE-SENSITIVE xsi:type="boolean">False</CASE-SENSITIVE>
				<BASE-EXPRESSION format-rev="2" xsi:type="valueBaseExpression">
					<VALUE xsi:type="string">Blinking</VALUE>
				</BASE-EXPRESSION>
			</EXPRESSION>
			<TIME format-rev="2" xsi:type="valueBaseExpression">
				<VALUE xsi:type="integer">1000</VALUE>
			</TIME>
		</EXPECTATION>
        """


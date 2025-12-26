import sys
import os
import json
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))

from .mapping import Mapping 
from .variables import Variables
from .pkgstep import PkgStep
from .project import Project
from .config import ConfigurationFile
from ..model.pkg import rewrite_node

class Teststep:
    def __init__(self,xml_filepath) -> None:
        self.xml_filepath = xml_filepath
        self.variables =  Variables().parse_vars(xml_filepath)
        self.mapping_items = Mapping().parse_mappings(xml_filepath)
        self.test_steps = PkgStep().parse_steps(xml_filepath)


    def json(self,filename= None):
        program = []
        vars = []
        mapping_items = []
        for step in self.test_steps:
            program.append(step.to_dict())
        for name,var_info in self.variables.items():
            vars.append(var_info.to_dict())
        for name,mapping_info in self.mapping_items.items():
            mapping_items.append(mapping_info.to_dict())
        dict_list = {
            "program":self.tree(program),
            "vars":vars,
            "mapping_items":mapping_items
        }
        # 重写
        for node in dict_list['program']:
            rewrite_node(node,dict_list['mapping_items'])
        if filename is None:  # filename 带路径的文件名
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(dict_list, f, ensure_ascii=False, indent=4)
        else:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(dict_list, f, ensure_ascii=False, indent=4)

        

    def tree(self,program):
        tree = []
        node_map = {block['id']: block for block in program}
        
        for block in program:
            block_id = block['id']
            parent_id = block['parent_id']
            if parent_id is None:
                tree.append(block)
            elif node_map[parent_id]['is'] == 'If': # 跳过then和else节点,他们的父节点一定是If
                continue
            else:
                parent_block = node_map.get(parent_id)
                if parent_block is not None:
                    if parent_block['is'].lower() != 'ifthenelsenode':
                        if 'body' not in parent_block:
                            parent_block['body'] = []
                        parent_block['body'].append(block)
                    else:
                        grandparent_block = node_map.get(parent_block['parent_id'])
                        if parent_block['test'] == 'then':
                            body = 'consequentBody'
                        else:
                            body = 'alternateBody'
                        if body not in grandparent_block:
                            grandparent_block[body] = []
                        grandparent_block[body].append(block)
        return tree
    

def parse_pkg(xml_filepath):
    print(xml_filepath)
    teststep_info = Teststep(xml_filepath)
    # data.json
    # teststep_info.json(r"D:\data\ECU-TEST_223\Packages\nest\Package.pkg.json")
    name = xml_filepath + '.json'
    # print(name)
    # teststep_info.json(name)
    try:
        teststep_info.json(name)
        return name+" parse success!"
    except Exception as e:
        return name+" parse failed!"

def parse_prj(xml_filepath):
    # 解析xml
    # json
    prj = Project()
    try:
        data = prj.parse_prj(xml_filepath)
        with open(xml_filepath+'.json', 'w',encoding="utf-8") as f:
            json.dump(data.to_dict(), f,ensure_ascii=False, indent=4)
        return xml_filepath+".json parse success!"
    except Exception:
        return xml_filepath+".json parse failed!"

def parse_tbc(xml_filepath):
    cfg = ConfigurationFile()
    try:
        data = cfg.parse_tbc(xml_filepath)
        with open(xml_filepath+'.json', 'w',encoding="utf-8") as f:
            json.dump(data.to_dict(), f,ensure_ascii=False, indent=4)
        return xml_filepath+".json parse success!"
    except Exception:
        return xml_filepath+".json parse failed!"
    
def parse_tcf(xml_filepath):
    cfg = ConfigurationFile()
    try:
        data = cfg.parse_tcf(xml_filepath)
        with open(xml_filepath+'.json', 'w',encoding="utf-8") as f:
            json.dump(data.to_dict(), f,ensure_ascii=False, indent=4)
        return xml_filepath+".json parse success!"
    except Exception:
        return xml_filepath+".json parse failed!"


def list_files_in_folder(folder_path):
    files = []
    # 使用 os.listdir() 函数列出文件夹中的所有文件和子文件夹
    for file_name in os.listdir(folder_path):
        # 使用 os.path.join() 函数将文件名与文件夹路径拼接，得到完整的文件路径
        file_path = os.path.join(folder_path, file_name)
        # 判断文件路径是否为文件（而不是子文件夹）
        if os.path.isfile(file_path) and not file_path.endswith('.json'):
            # 将文件路径添加到数组中
            files.append(file_path)
        elif os.path.isdir(file_path):
            # 如果是目录，则递归调用 list_files_in_folder() 函数，获取该目录下的全部 .xml 文件
            files.extend(list_files_in_folder(file_path))
    return files

def parse_tc(folder_path):
    res =[]
    xml_files = list_files_in_folder(folder_path)
    for xml_file in xml_files:
        if xml_file.endswith(".pkg"):
            res.append(parse_pkg(xml_file))
        elif xml_file.endswith(".prj"):
            res.append(parse_prj(xml_file))  
    return res


def parse_cfg(folder_path):
    res =[]
    xml_files = list_files_in_folder(folder_path)
    for xml_file in xml_files:
        if xml_file.endswith(".tbc"):
            res.append(parse_tbc(xml_file))
        elif xml_file.endswith(".tcf"):
            res.append(parse_tcf(xml_file))  
    return res

if __name__ == "__main__":
    # folder_path = r"D:\data\ECU-TEST_223\Packages"
    folder_path = r"C:\Users\lsl27\Desktop\workspaces\Packages\usertest\成哲\VCU\00_冒烟测试\VCU冒烟测试_0001_整车高压上电流程.pkg"
    # folder_path = r"D:\data\ECU-TEST_223\Packages\Interface_0625"
    # folder_path = r"D:\data\ECU-TEST_223\Packages\func-test"
    parse_pkg(folder_path)
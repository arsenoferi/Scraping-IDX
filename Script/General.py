import os
import pandas as pd
from lxml import html
import numpy as np

class General:
    
    def __init__(self):
        pass

    def get_folder(self,x):
        current_folder = os.getcwd()
        get_folder = os.path.join(current_folder,'Data',x['Company'],str(x['Tahun_Buku']))
        return get_folder
    
    def add_folder_columns(self):
        combine_list = pd.read_csv('combine list.csv')
        combine_list['folder_path']=combine_list.apply(lambda x: self.get_folder(x),axis=1)
        return combine_list
    
    def get_data(self,folder_path,file_name,contex,tag):
        file_path = os.path.join(folder_path,file_name)
        with open(f'{file_path}', 'r', encoding='utf-8') as file:
            html_content = file.read()
            bytes_content = html_content.encode('utf-8')

        multiplier = 1
        try:
            xpath_expression_multiplier = f"//tr[td[normalize-space()='{k}']]/td[@class='valueCell']/*[@contextref='{contex}']/@sign"
            tree_multiplier = html.fromstring(bytes_content)
            results_multiplier = tree_multiplier.xpath(xpath_expression_multiplier)[0]
            if results_multiplier == '-':
                multiplier = -1
        except:
            pass
        
        xpath_expression = f"//tr[td[normalize-space()='{tag}']]/td[@class='valueCell']/*[@contextref='{contex}']/text()"
        tree = html.fromstring(bytes_content)
        result = tree.xpath(xpath_expression)
        result = result[0].strip()
        result = result.replace(',','')
        result = result.replace('(','-')
        result = result.replace(')','')
        result = result.strip()
        result = float(result) if result else 0
        result = result * multiplier
        return result

    def get_multiple_data(self,folder_path,file_name,contex,tag:list):
        file_path = os.path.join(folder_path,file_name)
        
        with open(f'{file_path}', 'r', encoding='utf-8') as file:
            html_content = file.read()
            bytes_content = html_content.encode('utf-8')
       
        value_total = []
        for k in tag:
            multiplier = 1
            try:
                xpath_expression_multiplier = f"//tr[td[normalize-space()='{k}']]/td[@class='valueCell']/*[@contextref='{contex}']/@sign"
                tree_multiplier = html.fromstring(bytes_content)
                results_multiplier = tree_multiplier.xpath(xpath_expression_multiplier)[0]
                if results_multiplier == '-':
                    multiplier = -1
            except:
                pass

            xpath_expression = f"//tr[td[normalize-space()='{k}']]/td[@class='valueCell']/*[@contextref='{contex}']/text()"
            tree = html.fromstring(bytes_content)
            results = tree.xpath(xpath_expression)
            try:
                results = results[0].strip()
                results = results.replace(',','')
                results = results.replace('(','-')
                results = results.replace(')','')
                results = results.strip()
                results = float(results) if results else 0
                results = results * multiplier
                value_total.append(float(results))
            except:
                pass
        
        result = sum(value_total)

        if result == 0:
            raise ValueError("x must not be equal to 0.")

        return result
    
    def execution(self,file_name):
        folder_path = self.get_folder(file_name)

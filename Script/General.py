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
        
        xpath_expression = f"//tr[td[normalize-space()='{tag}']]/td[@class='valueCell']/*[@contextref='{contex}']/text()"
        tree = html.fromstring(bytes_content)
        result = tree.xpath(xpath_expression)
        result = result[0].strip()
        return result

    
    def execution(self,file_name):
        folder_path = self.get_folder(file_name)

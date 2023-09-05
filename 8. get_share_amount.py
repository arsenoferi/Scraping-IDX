import os
import concurrent.futures
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def execute_selenium_task(company):
    #options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')  # Set headless mode using add_argument

    driver = webdriver.Firefox()
    try:
        data = []
        vars = {}
        driver.get(f"https://www.idx.co.id/id/perusahaan-tercatat/profil-perusahaan-tercatat/{company}")
        print(f'--saving {company}--')
        vars["Company"] = company
        driver.set_window_size(1440, 801)
        try:
            WebDriverWait(driver, 100).until(expected_conditions.text_to_be_present_in_element((By.XPATH, "//div[@id=\'app\']/div[2]/main/div[2]/div/nav/button[3]"), "Pencatatan Saham"))
            WebDriverWait(driver, 100).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@id=\'app\']/div[2]/main/div[2]/div/nav/button[3]")))
            WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@id=\'app\']/div[2]/main/div[2]/div/nav/button[3]")))
            WebDriverWait(driver, 100).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".mr-24:nth-child(3)")))
            driver.find_element(By.CSS_SELECTOR, ".mr-24:nth-child(3)").click()
            WebDriverWait(driver, 100).until(expected_conditions.visibility_of_element_located((By.XPATH, "//table[@id=\'vgt-table\']/tbody/tr/td/span")))
            WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id=\'vgt-table\']/tbody/tr/td/span")))
            WebDriverWait(driver, 100).until(expected_conditions.visibility_of_element_located((By.XPATH, "//table[@id='vgt-table']/tbody/tr/td[4]/div")))
            WebDriverWait(driver, 100).until(expected_conditions.presence_of_element_located((By.XPATH, "//table[@id='vgt-table']/tbody/tr/td[4]/div")))
            
        except:
            vars["Tanggal"] = "Tidak ada data"
            vars["Saham"] = "Tidak ada data"
            data.append(vars.copy())
       
        condition = True
        i = 1
        while condition:
            try:
                if i == 1:
                    
                    try:
                        vars["Tanggal"] = driver.find_element(By.XPATH, "//table[@id=\'vgt-table\']/tbody/tr/td/span").text
                        vars["Saham"] = driver.find_element(By.XPATH, "//table[@id=\'vgt-table\']/tbody/tr/td[4]/div").text
                    except:
                        vars["Tanggal"] = driver.find_element(By.XPATH, f"//table[@id=\'vgt-table\']/tbody/tr[{i}]/td/span").text
                        vars["Saham"] = driver.find_element(By.XPATH, f"//table[@id=\'vgt-table\']/tbody/tr[{i}]/td[4]/div").text
                else:
                    vars["Tanggal"] = driver.find_element(By.XPATH, f"//table[@id=\'vgt-table\']/tbody/tr[{i}]/td/span").text
                    vars["Saham"] = driver.find_element(By.XPATH, f"//table[@id=\'vgt-table\']/tbody/tr[{i}]/td[4]/div").text
                    
                data.append(vars.copy())
                i += 1
            except:
                condition = False
                driver.quit()
    except:
        data = []
        vars = {}
        vars["Company"] = company 
        vars["Tanggal"] = "Tidak ada data"
        vars["Saham"] = "Tidak ada data"
        data.append(vars.copy())
    
    

    return data

def main():
    def companies():
        data = pd.read_csv("data_olahan.csv")
        data = data.drop_duplicates(subset=['Company'])
        data = data['Company'].tolist()
        return data
    
    def flatten_list(nested_list):
        flattened_list = [item for sublist in nested_list for item in sublist]
        return flattened_list

    companies_list = companies()  # Replace with actual company names
    #num_cpus = os.cpu_count()  # Get the number of available CPU cores
    num_cpus = 5

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cpus) as executor:
        tasks = [executor.submit(execute_selenium_task, company) for company in companies_list]
        results = [task.result() for task in tasks]
        
    results = flatten_list(results)
    results = pd.DataFrame(results)
    results.to_csv("jumlah_saham.csv", index=False)
    print(results)

if __name__ == "__main__":
    print("Running main()")
    main()
    print("Done running main()")

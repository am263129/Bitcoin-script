from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import threading
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os
import os.path
from progress.spinner import PixelSpinner
# An error box

def get_urls(file_path):
    url_file = open(file_path,"r")
    urls = url_file.readlines()
    if(len(urls) == 0):
        messagebox.showerror("Error","Empty URLs")
        return
    if (len(urls) > 1 and scrap_mode == False):
        messagebox.showwarning("Wanning","Showing mode. there are more than one urls on this file.")
    global url_list
    for i in urls:
        url_list.append(i)

def upgrade_status(status):
    print(status)
    T.insert(END, status +  "\n")
    T.see("end")
    root.update_idletasks()

def upgrade_progress(value):
    new_progress = value
    global old_progress
    current = old_progress
    for _ in range(new_progress - current):
        BarVolSyringe1["value"] = current + _
        root.update_idletasks()
        time.sleep(0.1)
    old_progress = new_progress
def Create_driver():

    # capabilities['proxy']['socksUsername'] = proxy['username']
    # capabilities['proxy']['socksPassword'] = proxy['password']
    options = Options()
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowing-disable-auto-update", "disable-client-side-phishing-detection"])
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=default')
    options.add_argument('--incognito')
    options.add_argument('--disable-plugin-discovery')
    options.add_argument('--start-maximized')
    options.add_argument("--enable-automation")
    options.add_argument("--test-type=browser")
    driver = webdriver.Chrome(executable_path="./chromedriver", options = options)
    # desired_capabilities=capabilities  
    return driver


def OpenFile():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    print (name)
    Entry_URLfile_path.delete(0,END)
    Entry_URLfile_path.insert(0,name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'r') as UseFile:
            print(UseFile.read())
    except:
        print("No file exists")
def start():
    global scrap_mode
    if(v.get() == 1):
        scrap_mode = True
        upgrade_status("Scraping mode. Only scrap data")
        print("mode 1")
    else:
        upgrade_status("Showing mode. scrap and show data (for one url)")
        scrap_mode = False
        print("mode 2")

    if(Entry_URLfile_path.get() == ""):
        messagebox.showerror("Error","Please import URL file")
        return
    disable_buttons()
    threading.Thread(target=main).start()
def start_server():
    os.system('app.py')

def disable_buttons():
    Btn_import["state"] = "disabled"
    Btn_start["state"] = "disabled"

def enable_buttons():
    Btn_import["state"] = "normal"
    Btn_start["state"] = "normal"

def main():
    get_urls(Entry_URLfile_path.get())
    columns = [
        "Hash",
        "Received Time",
        "Included Block",
        "Total Input",
        "Total Output",
        "Value when transacted",
    ]

    node_columns = [
        "Account",
        "CustomerName",
        "Type"
    ]
    edge_columns = [
        "TransactionAmt",
        "Source",
        "Target",
        "Date"
    ]
    node_df = pd.DataFrame(columns=node_columns)
    node_df = node_df.fillna(0)
    edge_df = pd.DataFrame(columns=edge_columns)
    edge_df = edge_df.fillna(0)


    Total_data = pd.DataFrame(columns=columns)
    Total_data = Total_data.fillna(0)
    for index in range(len(url_list)):
        
        # url = 'https://www.blockchain.com/btc/tx/273377b238decc1759f12139b0962043582ef13512fb33487f072334361a11d5'
        url = url_list[index]
        response = get(url)

        chrome_options = Options()  
        chrome_options.add_argument("--headless") # Opens the browser up in background

        with Chrome(options=chrome_options) as browser:
             browser.get(url)
             time.sleep(2)
             response = browser.page_source
        # print(response)
        html_soup = BeautifulSoup(response, 'html.parser')
        # html_soup = BeautifulSoup(response.text, 'html.parser')

        try:
            if(html_soup.find('h1', class_ = "Text__TitleLarge-sc-1fwf07x-1 dePAvX").text == "Oops!"):
                # messagebox.showerror("Wanning","Wroing URL")
                upgrade_status(url + ": Wrong URL")
                continue
        except:
            pass
        type(html_soup)
        hash_data = url.split("/")[-1].strip()

        # try:
        Time = ""
        Included_block = ""
        T_input = ""
        T_output = ""
        value_trans = ""
        Fees = ""
        input_address = []
        output_address = []
        # datas = html_soup.find_all('span', class_ = 'sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk')
        # for i in range(1,len(datas)):
        #     data = datas[i]
        #     print(data.text)
        #     if (data.text == hash_data):
        #         Time = datas[i + 1].text
        #         T_input = datas[i + 5].text
        #         T_output = datas[i + 6].text
        #         value_trans = datas[i + 10].text
        #         break
        # print(len(html_soup.find_all('div', class_ = 'sc-1mp2xeh-0 hHMifg')))
        data_body = html_soup.find('div', class_ = "jzbgk8-0 krJCys")
        data_items = data_body.find_all('div', class_ = "sc-1enh6xt-0 jteUtu")
        for i in range(len(data_items)):
            data_item = data_items[i]
            label = data_item.find('span', class_ = "sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh sc-1n72lkw-0 bKaZjn").text
            if label == "Received Time":
                Time = data_item.find('span', class_ = "sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk").text
            if label == "Total Input":
                T_input = data_item.find('span', class_ = "sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk").text
            if label == "Total Output":
                T_output = data_item.find('span', class_ = "sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk").text
            if label == "Value when transacted":
                value_trans = data_item.find('span', class_ = "sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk").text
            if label == "Fees":
                Fees = data_item.find('span', class_ = "sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk").text
                
        Included_Block = data_body.find('a').text
        input_address_data = html_soup.find_all('div', class_ = 'sc-1mp2xeh-0 hHMifg')[0].find_all("a")
        for i in range(len(input_address_data)):
            if len(input_address_data[i].text) > 10:
                input_address.append(input_address_data[i].text)
        output_address_data = html_soup.find_all('div', class_ = 'sc-1567cm0-0 gLOdsG')[0].find_all("a")
        for i in range(len(output_address_data)):
            if len(output_address_data[i].text) > 10:
                output_address.append(output_address_data[i].text)
        print(hash_data)
        print(Time)
        print(T_input)
        print(T_output)
        print(Included_Block)
        print(value_trans)
        print(input_address)
        print(output_address)
        print(Fees)
        # datetime = datas[2].find('div', class_ = "sc-1ryi78w-0 bFGdFC sc-16b9dsl-1 iIOvXh u3ufsr-0 gXDEBk").text
        # print(datetime)
        data_item = pd.DataFrame(columns=columns)
        node_item = pd.DataFrame(columns = node_columns)
        edge_item = pd.DataFrame(columns = edge_columns)
        data_item = data_item.fillna(0)
        data_item.at['0',"Hash" ] = hash_data
        data_item.at['0',"Received Time" ] = Time
        data_item.at['0',"Included Block" ] = Included_Block
        data_item.at['0',"Total Input" ] = T_input
        data_item.at['0',"Total Output" ] = T_output
        data_item.at['0',"Fees" ] = Fees
        data_item.at['0',"Value when transacted" ] = value_trans
        trans_center_flag = True

        input_block = html_soup.find('div', class_ = "sc-1mp2xeh-0 hHMifg")
        datas_input = input_block.find_all('div', class_ = "sc-1fp9csv-0 gkLWFf")

        output_block = html_soup.find('div', class_ = "sc-1567cm0-0 gLOdsG")
        datas_output = output_block.find_all('div', class_ = "sc-1fp9csv-0 gkLWFf")

        for i in range(len(datas_input)):
            length = len(datas_input[i].find_all('a'))-1
            if (datas_input[i].find_all('a')[length].text == ""):
                continue
            address = datas_input[i].find_all('a')[length].text
            span_data = datas_input[i].find_all("span")
            amount = ""
            for _ in range(len(span_data)):
                if("BTC" in span_data[_].text):
                    amount = span_data[_].text

            data_item.at['0',"Input_address%s"%(i+1) ] = address
            node_item.at['0',"Account" ] = address
            node_item.at['0',"CustomerName" ] = ""
            node_item.at['0',"Type" ] = "input"
            node_df = node_df.append(node_item, ignore_index=True, sort=False)
            if trans_center_flag:
                node_item.at['0',"Account" ] = "Transaction%s"%index
                node_item.at['0',"CustomerName" ] = ""
                node_item.at['0',"Type" ] = "transaction-center"
                node_df = node_df.append(node_item, ignore_index=True, sort=False)
                trans_center_flag = False
            range_ = len(amount.replace("BTC", "").strip())
            temp = amount.replace("BTC", "").strip()
            edge_item.at['0',"TransactionAmt" ] = temp
            edge_item.at['0',"Source" ] = address
            edge_item.at['0',"Target" ] = "Transaction%s"%index
            edge_item.at['0',"Date" ] = Time.split(" ")[0].replace("-","/")
            edge_df = edge_df.append(edge_item, ignore_index=True, sort=False)

        for i in range(len(datas_output)):
            length = len(datas_output[i].find_all('a'))-1
            if (datas_output[i].find_all('a')[length].text == ""):
                continue
            address = datas_output[i].find_all('a')[length].text
            amount = ""
            span_data = datas_output[i].find_all("span")
            for _ in range(len(span_data)):
                if("BTC" in span_data[_].text):
                    amount = span_data[_].text
            if trans_center_flag:
                node_item.at['0',"Account" ] = "Transaction%s"%index
                node_item.at['0',"CustomerName" ] = ""
                node_item.at['0',"Type" ] = "transaction-center"
                node_df = node_df.append(node_item, ignore_index=True, sort=False)
                trans_center_flag = False
            data_item.at['0',"Output_address%s"%(i+1) ] = address
            node_item.at['0',"Account" ] = address
            node_item.at['0',"CustomerName" ] = ""
            node_item.at['0',"Type" ] = "output"
            node_df = node_df.append(node_item, ignore_index=True, sort=False)
            temp = amount.replace("BTC", "").strip()
            edge_item.at['0',"TransactionAmt" ] = temp
            edge_item.at['0',"Source" ] = "Transaction%s"%index
            edge_item.at['0',"Target" ] = address
            edge_item.at['0',"Date" ] = Time.split(" ")[0].replace("-","/")
            edge_df = edge_df.append(edge_item, ignore_index=True, sort=False)


        # for i in range(len(input_address)):
        #     data_item.at['0',"Input_address%s"%(i+1) ] = input_address[i]
        #     node_item.at['0',"Account" ] = input_address[i]
        #     node_item.at['0',"CustomerName" ] = ""
        #     node_item.at['0',"Type" ] = "input"
        #     node_df = node_df.append(node_item, ignore_index=True, sort=False)
        #     if trans_center_flag:
        #         node_item.at['0',"Account" ] = "Transaction%s"%index
        #         node_item.at['0',"CustomerName" ] = ""
        #         node_item.at['0',"Type" ] = "transaction-center"
        #         node_df = node_df.append(node_item, ignore_index=True, sort=False)
        #         trans_center_flag = False
        #     edge_item.at['0',"TransactionAmt" ] = 500
        #     edge_item.at['0',"Source" ] = input_address[i]
        #     edge_item.at['0',"Target" ] = "Transaction%s"%index
        #     edge_item.at['0',"Date" ] = Time.split(" ")[0].replace("-","/")
        #     edge_df = edge_df.append(edge_item, ignore_index=True, sort=False)
        # for i in range(len(output_address)):
        #     if trans_center_flag:
        #         node_item.at['0',"Account" ] = "Transaction%s"%index
        #         node_item.at['0',"CustomerName" ] = ""
        #         node_item.at['0',"Type" ] = "transaction-center"
        #         node_df = node_df.append(node_item, ignore_index=True, sort=False)
        #         trans_center_flag = False
        #     data_item.at['0',"Output_address%s"%(i+1) ] = output_address[i]
        #     node_item.at['0',"Account" ] = output_address[i]
        #     node_item.at['0',"CustomerName" ] = ""
        #     node_item.at['0',"Type" ] = "output"
        #     node_df = node_df.append(node_item, ignore_index=True, sort=False)
        #     edge_item.at['0',"TransactionAmt" ] = 400
        #     edge_item.at['0',"Source" ] = "Transaction%s"%index
        #     edge_item.at['0',"Target" ] = output_address[i]
        #     edge_item.at['0',"Date" ] = Time.split(" ")[0].replace("-","/")
        #     edge_df = edge_df.append(edge_item, ignore_index=True, sort=False)
        
        sub_data = data_item.copy()
        data_item.drop(data_item.index, inplace=True)
        Total_data = Total_data.append(sub_data, ignore_index=True, sort=False)
        upgrade_status(hash_data + ": completed")
        progress = int(((index+1)/len(url_list) * 100))
        threading.Thread(target=upgrade_progress,args=[progress]).start()
        # except:
        #     upgrade_status(hash_data + ": Error")
    if len(Total_data) !=0:
        Total_data.to_csv("result.csv", sep=',', encoding='utf-8')
    if scrap_mode == False:
        if len(node_df) !=0:
            node_df.to_csv("node1.csv", sep=',', encoding='utf-8',index=False)
        if len(edge_df) !=0:
            edge_df.to_csv("edge1.csv", sep=',', encoding='utf-8',index=False)

        if os.path.isfile("node1.csv") and os.path.isfile("edge1.csv"):
            threading.Thread(target=start_server).start()
            time.sleep(5)
            driver = Create_driver()
            driver.get("http://127.0.0.1:8050/")
    enable_buttons()


if __name__ == '__main__':
    url_list = []
    
    scrap_mode = True
    root = Tk() 
    old_progress = 0
    root.geometry("700x290")
    root.title("Bitcoin ")
    root.wm_attributes("-topmost", 1)


    root.grid_columnconfigure(0, weight = 1)
    root.grid_columnconfigure(1, weight = 3)
    root.grid_columnconfigure(2, weight = 1)


    v = IntVar()

    Option1 = Radiobutton(root, text="Scraping mode", variable=v, value=1)
    Option1.grid(row = 0, column = 0 ,sticky = E)

    Option2 = Radiobutton(root, text="Showing mode", variable=v, value=2)
    Option2.grid(row= 0, column = 1, sticky = W)

    Label_number_account =  Label(root, text="URL file path", width = 20)
    Label_number_account.grid(row = 1, column = 0 , sticky = E)
    Entry_URLfile_path =  Entry(root, bd =2, width = 30)
    Entry_URLfile_path.grid(row = 1, column = 1)


    Btn_import = Button(root, width = 20, text = "Import", command = lambda: OpenFile() )
    Btn_import.grid( row = 1, column = 2, sticky = W + E)
    Btn_import.grid(padx=30, pady=5)
    Btn_start = Button(root, width = 20, text = "Start", command = lambda: start() )
    Btn_start.grid( row = 2, column = 2, sticky = W + E)
    Btn_start.grid(padx=30, pady=5)
    Label_status =  Label(root, text="Current status", width = 20)
    Label_status.grid(row = 2, column = 0 , sticky = E)

    output_status = Frame(root,width = 700,height = 10, background = "pink")
    output_status.grid(columnspan = 5, row = 5,rowspan = 8, sticky = W+E,padx=20, pady=5)

    S = Scrollbar(output_status)
    T = Text(output_status, height=10, width=700, state="normal")
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=TOP, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    BarVolSyringe1 = ttk.Progressbar(root, orient='horizontal',length = 300, mode='determinate', value = 0)
    BarVolSyringe1.grid(row = 4, columnspan = 3,sticky = E+W)

    v.set(1)
    mainloop()
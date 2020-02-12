# Bitcoin-script
Bitcoin script
User Guide
1.	Folder Structure
bitcoin.py, app.py, chromedriver.exe, requirement.txt
•	bitcoin.py : script which scrap data from website and save as result.csv.
•	app.py : script which make node and edge of scraped data and show.
•	chromedriver.exe : chrome webdriver, download from https://chromedriver.chromium.org/downloads
(the version of chromedriver should be same as chrome browser on com. 
ex: if chrome version is 79.0….. you should download chromedriver – version 79)
•	requirement.txt : txt file which include name of using python packages.
	Help/About Google Chrome 
  
https://chromedriver.chromium.org/downloads
 






2.	Environment 
Python(3.7 or higher)
•	Installing python : https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/python.html
•	Installing pip : (This is python package installer which download and install python packages.)
https://pip.pypa.io/en/stable/installing/
•	Install python packages
After install python and pip. You can check if you installed python and pip correctly on cmd (terminal in Linux or Mac).

python --version
pip --version 
 
If all are perfect.
Move to current script folder on cmd and 
pip install -r requirement.txt –user
 










3.	Run script
On current script folder in cmd 
python bitcoin.py
 
This UI will opened
 
There are two radio buttons on the top.
 
This is for select mode – scraping mode and showing mode.
•	Scraping mode: This mode is for scraping data from many urls – just for getting csv result file.
•	Showing mode: This mode is for make visual data – just for one url.
There is one input box under radio buttons
 
Here is path of url file. You can input manually or just press Import button on the right.
After that just select your url file on the file open dialog.
(url file should be txt file.)

url.txt(you can use any name you like)
 
(Important: when you select second mode, your url file should have one url)
After input the file path, press start button
 
The script will run!
When finish, you can see result.csv file on the script folder.
 
If second mode , this will be shown at the end of script.
 












4.	Error Handling 
•	Please import URL file : 
When you press start button without input url file path.
 
•	Empty URL :
When your url file is empty.
 
•	Wanning  your file have more than one urls :
When showing mode and url file has more than one urls
 
For other bugs, please report to 


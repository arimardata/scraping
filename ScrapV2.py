#Importing packages
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html
import requests
import json
import csv
import unidecode
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By





def every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)






url='https://sodipress.com/Maroc/accueil.html#'


chromeOptions = webdriver.ChromeOptions()
desired_caps = {'prefs': {'download': {'default_directory': 'C://Users/Jarvis/Desktop/Scrapping_Module/Data'}}}







options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
prefs = {"profile.default_content_settings.popups": 0,
"download.default_directory": r"C:\Users\Jarvis\Desktop\Scrapping_Module\Data\\", # IMPORTANT - ENDING SLASH V IMPORTANT
"directory_upgrade": True}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=r'Drivers/chromedriver.exe',chrome_options=options)
driver.get(url)

driver.find_element_by_xpath('//*[@id="collapsing"]/ul/li[1]/a ').click()
driver.find_element_by_xpath('//*[@id="login-form:username"]').send_keys('gecomar')
driver.find_element_by_xpath('//*[@id="login-form:password"]').send_keys('GECO2018Y')
driver.find_element_by_xpath('//*[@id="login-form"]/input[2]').click()
driver.find_element_by_xpath('//*[@id="favoris"]').click()

soup = BeautifulSoup(driver.page_source,'html.parser')


AOs =soup.find_all('div',{'class':'single-head coloriz even'})
x=0
Dict = [] 
for AO in AOs:
	print('Appel doffre numero:', x)
	chef_ouvrage=AO.find('a',{'class':'ui-commandlink ui-widget'}).text.strip()
	details=AO.find_all('div',{'class':'coll'})
	detail1=details[0]
	str1=detail1.find_all("strong")
	detail2=details[1]
	str2=detail2.find_all("strong")
	detail3=details[2]
	str3=detail3.find_all("strong")
	Num_AO=str1[0].text.strip()
	Num_Ordre=str1[1].text.strip()
	Caution=str1[2].text.strip()
	Mise_en_ligne=str2[0].text.strip()
	Date_Limite=str2[1].text.strip()
	Type=str3[0].text.strip()
	Ville=str3[1].text.strip()
	Estimation=str3[2].text.strip()
	#
	Autres_details=AO.find('p').text
	#
	print('chef_ouvrage: ', chef_ouvrage)
	print('Num_AO: ', Num_AO)
	print('Num dordre: ', Num_Ordre)
	print('Caution', Caution)
	print('Mise en ligne: ', Mise_en_ligne)
	print('Date limite: ', Date_Limite)
	print('Type: ', Type)
	print('Ville: ', Ville)
	print('Estimation: ', Estimation)
	print('Autre_details: ', Autres_details)
	Dict.append({
	'chef_ouvrage':chef_ouvrage,
	'Num_AO':Num_AO,
	'Num_Ordre':Num_Ordre,
	'Caution':unidecode.unidecode(Caution),
	'Mise en ligne':Mise_en_ligne,
	'Date Limite': Date_Limite,
	'Type':Type,
	'Ville':Ville,
	'Estimation':unidecode.unidecode(Estimation),
	'Autres_details':Autres_details,
	'etat':"Favoris"
	#
	})
	x=x+1
print(Dict)
with open('Appels.txt', 'w') as json_file:
	json.dump(Dict, json_file)
client = MongoClient('localhost', 27017)
db = client['Projet']
#client = MongoClient('ds145895.mlab.com:45895',username='ArmiraDATA',password='ArmiraDATA1',authSource='armira',authMechanism='SCRAM-SHA-1')
#uri = "mongodb://ArmiraDATA:ArmiraDATA1@ds145895.mlab.com:45895/armira"
#client = MongoClient(uri)
#db = client['armira']
for index in range(len(Dict)):
	try:
		print('===========1===========')
		wait1 = WebDriverWait(driver,20)
		print('===========2===========')
		item1=wait1.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dataTabletpublist:'+str(index)+':j_idt157"]')))
		print('===========3===========')
		item1.click()
		try:
			print('===========4===========')
			wait2 = WebDriverWait(driver,20)
			print('===========5===========')
			item2=wait2.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="detaipiecejoint:0:downloadLink"]')))
			print('==========6============')
			db['AppelOffre'].insert(Dict[index])
			print('===========7===========')
			item2.click()
			print('===========8===========')
			driver.find_element_by_xpath('//*[@id="pdfBtntdet"]').click()
			print('===========9===========')
			driver.find_element_by_xpath('//*[@id="dialog"]/div[1]/a/span').click()
		except:
			print('ERROR')
			print('===========9===========')
			driver.find_element_by_xpath('//*[@id="dialog"]/div[1]/a/span').click()	
	except:
		print('ERROR')
	driver.refresh()
print('insert {len}'.format(len=len(Dict)))



# waits for all the files to be completed and returns the paths
paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
print(paths)
driver.quit()

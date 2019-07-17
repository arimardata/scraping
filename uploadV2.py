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
import gridfs


#uri = "mongodb://ArmiraDATA:ArmiraDATA1@ds145895.mlab.com:45895/armira"
#client = MongoClient(uri)
#db = client['armira']
client = MongoClient('localhost', 27017)
db = client['Projet']
mycol = db['AppelOffre']
Dict=[]
for x in mycol.find():
	Dict.append(x)

for index in range(len(Dict)):
	try:
		print('1')
		fs = gridfs.GridFS( db )
		print('2')
		fileID = fs.put( open( 'C://Users/Jarvis/Desktop/Scrapping_Module/Data/Sodipress'+str(Dict[index]['Num_Ordre'] )+'.rar', 'rb'),filename=str(Dict[index]['Num_Ordre'] ) )
		print('3')
		myquery = { "Num_Ordre": str(Dict[index]['Num_Ordre'] ) }
		print('4')
		newvalues = { "$set": { "Files": fileID } }
		print('5')
		db['AppelOffre'].update(myquery, newvalues)

		print('6')
		fileID2 = fs.put( open( 'C://Users/Jarvis/Desktop/Scrapping_Module/Data/Sodipress'+str(Dict[index]['Num_Ordre'] )+'.pdf', 'rb'),filename='PDF'+str(Dict[index]['Num_Ordre'] ) )
		newvalues2 = { "$set": { "PDFs": fileID2 } }
		print('7')
		db['AppelOffre'].update(myquery, newvalues2)
	except:
		print('ERROR update')

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

# 1 - Pegar conteúdo HTML a partir de uma URL
url = "https://www.nba.com/stats/players/traditional/?sort=PTS&dir=-1"

driver = webdriver.Chrome()

driver.get(url) #Abrindo Chrome com Selenium
time.sleep(10) #Depois de 10 segundos, será executado o quit() para fechar o navegador

# Executando o click no th que é clicável
driver.find_element_by_xpath("//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click()

#Obtendo uma tabela
element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')

# 2 - Converter o conteúdo HTML em um DataFrame - BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# 3 - Estruturar o conteúdo em um DataFrame - Pandas
df_full = pd.read_html(str(table))[0].head(10) #Top 10 jogadores NBA por pontos marcados
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']] #Selecionando algumas colunas necessárias para análise de dados
df.columns = ['pos', 'player', 'team', 'total'] #Renomeando as colunas do dataframe

# 4 - Transformar os dados em um dicionário de dados próprio
top10Ranking = {}
top10Ranking['points'] = df.to_dict('records')

# 5 - Converter e salvar em um arquivo JSON
js = json.dumps(top10Ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()

driver.quit()
 

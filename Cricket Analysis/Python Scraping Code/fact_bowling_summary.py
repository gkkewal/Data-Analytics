import requests
import xlsxwriter
from bs4 import BeautifulSoup

url = "https://www.espncricinfo.com/records/season/team-match-results/2022to23-2022to23?trophy=89"
# url = "https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2022-23-1298134/namibia-vs-sri-lanka-1st-match-first-round-group-a-1298135/full-scorecard"
r = requests.get(url)
s = BeautifulSoup(r.content,'html5lib')
urls = []
data = []
ids = []
maintable = s.find('tbody',attrs = {'class': ''})
tr = maintable.find_all('tr',attrs={'class': ''})
# tr2 = maintable.find_all('tr',attrs={'class': 'ds-bg-ui-fill-translucent'})
# tr += tr2 
# tr.append(tr2)

def collection(match,id,table,bolteam):
  tbody = table.find_all('tr',attrs={'class':''})
  for row in tbody:
   bowler = row.find('td',attrs={'class':'ds-items-center'})
   cols = row.find_all('td',attrs={'class':'ds-w-0'})
   cols = [ele.text.strip() for ele in cols]
   if bowler != None:
    bowler = bowler.text.strip()
    cols.insert(0,bowler)
   if cols != []:
    cols.insert(0,match)
    cols.insert(1,bolteam)
    cols.append(id)
    data.append(cols)
    # print(cols) 



def building(url,id):
 i = url
 r = requests.get(i)
 s = BeautifulSoup(r.content,'html5lib')
 #Fetch TeamName
 team = s.find_all('span',attrs={'class':'ds-capitalize'})
 match = team[0].text.strip() +" vs "+ team[1].text.strip() 
 table1 = s.find_all('table')[1]
 table2 = s.find_all('table')[3]
 for n in range(0,2):
  if n == 0:
   bolteam = team[n+1].text.strip()
   collection(match,id,table1,bolteam)
  else:
   bolteam = team[n-2].text.strip()
   collection(match,id,table2,bolteam)


   ##Fatch Out
  
  


for td in tr:
 # row = td.find_all('a',attrs={'class':'ds-inline-flex ds-items-start ds-leading-none'})
 ##Fetch Url
 row = td.find_all('a')[1]
 urls.append("https://www.espncricinfo.com/"+row['href'])
 url = "https://www.espncricinfo.com/"+row['href']
 ##Fetch MatchID
 id = row['title']
 ids.append(id)
 building(url,id)

print(data)


def insert_data(data):
  wb = xlsxwriter.Workbook("excel3.xlsx")
  ws = wb.add_worksheet()
  row = 0
  col = 0
  for list in data:
    for items in list:
      ws.write(row,col,items)
      col += 1
    row += 1
    col = 0
  wb.close()
insert_data(data)
  
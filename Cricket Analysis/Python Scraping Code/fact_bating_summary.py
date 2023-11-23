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
tr2 = maintable.find_all('tr',attrs={'class': 'ds-bg-ui-fill-translucent'})
# tr += tr2 
# tr.append(tr2)
def collection(match,id,table,team,teamnum):
  batteam = team[teamnum].text.strip()
  tbody = table.find_all('tr',attrs={'class':''})
  outs = table.find_all('td',attrs={'class':'!ds-pl-[100px]'})
  outs = [ele.text.strip() for ele in outs]
  for i, ele in enumerate(outs):
    if 'not out' in ele:
        outs[i] = 'not out'
    else:
        outs[i] = 'out'
  num = 0
  for row in tbody:
   cols = row.find_all('td',attrs={'class':'ds-w-0'})
   cols = [ele.text.strip() for ele in cols]
   if cols != []:
    cols.insert(0,match)
    cols.insert(1,batteam)
    cols.insert(2,num+1)
    cols.extend(outs[num:num+1])
    cols.append(id)
    data.append(cols)
    # print(cols) 
    num +=1



def building(url,id):
 i = url
 r = requests.get(i)
 s = BeautifulSoup(r.content,'html5lib')
 
 #Fetch TeamName
 team = s.find_all('span',attrs={'class':'ds-capitalize'})
 match = team[0].text.strip() +" vs "+ team[1].text.strip()
 tables = s.find_all('table',attrs={'class':'ci-scorecard-table'})
 teamnum = 0
 for table in tables:
  collection(match,id,table,team,teamnum)
  teamnum += 1


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
  wb = xlsxwriter.Workbook("excel2.xlsx")
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
  
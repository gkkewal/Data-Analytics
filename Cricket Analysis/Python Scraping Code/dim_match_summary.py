import requests
import xlsxwriter
from bs4 import BeautifulSoup
url = "https://www.espncricinfo.com/records/season/team-match-results/2022to23-2022to23?trophy=89"
r = requests.get(url)
s = BeautifulSoup(r.content,'html5lib')
n = 1
q2 = []
q = []
#table = s.find('section',attrs = {'id': 'main-container'})
#table = s.find('table',attrs = {'class': 'ds-w-full ds-table ds-table-xs ds-table-auto ds-w-full ds-overflow-scroll ds-scrollbar-hide'})
table1 = s.find('thead',attrs = {'class': 'ds-bg-fill-content-alternate ds-text-left'})
#table = s.find_all('span',attrs = {'class': 'ds-cursor-pointer'})
table2 = s.find('tbody',attrs = {'class': ''})


def thead(table):
  rows = table.find_all('tr', attrs = {'class':''})
  for row in rows:
    cols = row.find_all("td", attrs={'class':'ds-min-w-max'})
    #print(cols)
    cols = [ele.text.strip() for ele in cols]
    q.append([ele for ele in cols])
thead(table1)
thead(table2)
print(q)
def insert_data(listdata):
    wb = xlsxwriter.Workbook("Excel111.xlsx")
    ws = wb.add_worksheet()
    row = 0
    col = 0
    for line in listdata:
        for item in line:
            ws.write(row, col, item)
            col += 1
        row += 1
        col = 0
    wb.close()
insert_data(q)
# os.system("Excel1.xlsx")

# for row in table.find_all('td', attrs = {'ds-min-w-max'}):
#     Q = {}
#     Q['Team 1'] = row.span.text;
#     Q['Team 2'] =row.span.text;
#     Q['Winner'] =row.span.text;
#     Q['Margin'] = row.span.text;
#     Q['Ground'] =row.span.a.text;
#     Q['Match Date'] =row.span.text;
#     Q['Scorecard'] = row.span.a.text;
#     q.append(Q)
# print(q)
#print(table)
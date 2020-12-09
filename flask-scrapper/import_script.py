import requests
from app import db, DBTable
from bs4 import BeautifulSoup

# set up your scraping below
# this `main` function should run your scraping when 
# this script is ran.
def main():
    db.drop_all()
    db.create_all()      
    site = requests.get('https://coinranking.com/')
    soup = BeautifulSoup(site.text)
    table = soup.find('table')
    table_rows = table.tbody.findAll('tr')[:10]
    for t_row in table_rows:
        row = t_row.get_text().split()[1:]
        while('$' in row):
            idx = row.index('$')
            row[idx] += ' ' + row[idx + 1]
            del row[idx + 1]
        while('billion' in row):
            idx = row.index('billion')
            row[idx - 1] += ' billion'
            del row[idx]
        if len(row) > 5:
            del row[1]
        db_row = DBTable(name=row[0], symbol=row[1], price=row[2], market_share=row[3], change_24hr=row[4])
        print(db_row)
        db.session.add(db_row)
        db.session.commit()

if __name__ == '__main__':
    main()
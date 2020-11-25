def write_to_csv():
    site = requests.get('https://coinranking.com/')
    soup = BeautifulSoup(site.text)
    table = soup.find('table')
    table_rows = table.tbody.findAll('tr')[:11]
    with open('crypto_data.csv','w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'symbol', 'price', 'market price', '24hr change'])
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
            writer.writerow(row)

if __name__ == '__main__':
    import csv
    import requests
    from bs4 import BeautifulSoup
    write_to_csv()
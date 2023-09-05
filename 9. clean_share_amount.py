import pandas as pd

def clean_share_amount(data):
    data['Saham'] = data['Saham'].str.replace('.', '')
    data = data[data['Saham'] != 'Tidak ada data']
    data['Saham'] = data['Saham'].astype(float)
    return data

def clean_share_month(data):
    replace_month = {
        'Jan' : 'January',
        'Feb' : 'February',
        'Mar' : 'March',
        'Apr' : 'April',
        'Mei' : 'May',
        'Jun' : 'June',
        'Jul' : 'July',
        'Agt' : 'August',
        'Sep' : 'September',
        'Okt' : 'October',
        'Nov' : 'November',
        'Des' : 'December',
    }

    for key, value in replace_month.items():
        data['Tanggal'] = data['Tanggal'].str.replace(key, value)
    
    data['Tanggal'] = pd.to_datetime(data['Tanggal'], format='%d %B %Y')
    return data

if __name__ == "__main__":
    data = pd.read_csv("jumlah_saham.csv")
    data = clean_share_amount(data) 
    data = clean_share_month(data)
    data.to_csv("jumlah_saham_clean.csv", index=False)
    print(data)
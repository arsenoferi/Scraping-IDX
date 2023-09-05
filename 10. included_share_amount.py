import pandas as pd
#share amount
share_amount = pd.read_csv("jumlah_saham_clean.csv")
share_amount = share_amount.sort_values(by=['Company', 'Tanggal'],ascending=[True, False])
share_amount['Tanggal'] = pd.to_datetime(share_amount['Tanggal'], format='%Y-%m-%d')
share_amount['Year'] = share_amount['Tanggal'].dt.year
share_amount['Year'] = share_amount['Year'].astype(int)
share_amount['Company'] = share_amount['Company'].str.strip()

#data olahan
data_olahan = pd.read_csv("data_olahan.csv")
data_olahan['Tahun_Buku'] = data_olahan['Tahun_Buku'].astype(int)
data_olahan['Company'] = data_olahan['Company'].str.strip()



def share_amount_func(x):
    try:
        share_amount_value = share_amount.copy()
        share_amount_value = share_amount[share_amount['Company'] == x['Company']]
        share_amount_value = share_amount_value[share_amount_value['Year'] <= int(x['Tahun_Buku'])]
        share_amount_value = share_amount_value.head(1)
        data = share_amount_value['Saham'].values[0]
    except:
        try:
            share_amount_value = share_amount.copy()
            share_amount_value = share_amount[share_amount['Company'] == x['Company']]
            share_amount_value = share_amount_value.head(1)
            data = share_amount_value['Saham'].values[0]
        except:
            data = 0
    
    return data


# process
if __name__ =="__main__":
   
    # data_olahan = data_olahan[data_olahan['Company']=='ADES']
    data_olahan['share_amount'] = data_olahan.apply(lambda x: share_amount_func(x), axis=1)
    data_olahan.to_csv("data_olahan_2.csv", index=False)
    print(data_olahan)
    
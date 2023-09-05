import pandas as pd
from multiprocessing import Pool
from Script.General import *
import multiprocessing
import math
import time
from datetime import datetime, timedelta
import yfinance as yf

g = General()
register = [
    ['kas','2','CurrentYearInstant','Kas dan setara kas'],
    ['kas','2','CurrentYearInstant','Kas'],  
    ['jumlah_aset_lancar','2','CurrentYearInstant',['Kas dan setara kas',
                                                    'Piutang hasil investasi',
                                                    'Piutang premi',
                                                    'Piutang reasuransi',
                                                    'Piutang lainnya',
                                                    'Aset reasuransi',
                                                    'Investasi dalam deposito berjangka',
                                                    'Investasi pada efek dan reksadana yang diukur pada nilai wajar melalui laba rugi',
                                                    'Investasi pada efek yang tersedia untuk dijual',
                                                    'Penyertaan saham',
                                                    'Biaya dibayar dimuka',
                                                    'Aset pajak tangguhan',
                                                    'Kas',
                                                    'Giro pada bank indonesia',
                                                    'Giro pada bank lain pihak ketiga',
                                                    'Giro pada bank lain pihak berelasi',
                                                    'Cadangan kerugian penurunan nilai pada giro pada bank lain',
                                                    'Penempatan pada bank indonesia dan bank lain pihak ketiga',
                                                    'Penempatan pada bank indonesia dan bank lain pihak berelasi',
                                                    'Cadangan kerugian penurunan nilai pada penempatan pada bank lain',
                                                    'Efek-efek yang diperdagangkan pihak ketiga',
                                                    'Efek-efek yang diperdagangkan pihak berelasi',
                                                    'Cadangan kerugian penurunan nilai pada efek-efek yang diperdagangkan',
                                                    'Wesel ekspor dan tagihan lainnya pihak ketig',
                                                    'Cadangan kerugian penurunan nilai pada wesel ekspor dan tagihan lainnya',
                                                    'Tagihan akseptasi pihak ketiga',
                                                    'Tagihan derivatif pihak berelasi',
                                                    'Pinjaman yang diberikan pihak ketiga',
                                                    'Pinjaman yang diberikan pihak berelasi',
                                                    'Cadangan kerugian penurunan nilai pada pinjaman yang diberikan',
                                                    'Aset keuangan lainnya'  
                                                    ]],
    ['jumlah_aset_lancar','2','CurrentYearInstant','Jumlah aset lancar'],                                                
    ['persediaan','2','CurrentYearInstant',['Efek-efek yang diperdagangkan pihak ketiga',
                                            'Efek-efek yang diperdagangkan pihak berelasi',
                                            'Persediaan lancar lainnya',
                                            'Aset keuangan tersedia untuk dijual',
                                            'Persediaan aset real estat lancar',
                                            'Persediaan lainnya',
                                            ]],                                        
    ['piutang','2','CurrentYearInstant',['Piutang usaha pihak ketiga',
                                        'Piutang usaha pihak berelasi',
                                        'Piutang lainnya pihak ketiga',
                                        'Piutang lainnya pihak berelasi',
                                        'Piutang hasil investasi',
                                        'Piutang premi',
                                        'Piutang reasuransi',
                                        'Piutang lainnya',
                                        'Piutang murabahah pihak ketiga',
                                        'Wesel ekspor dan tagihan lainnya pihak ketiga',
                                        'Cadangan kerugian penurunan nilai pada wesel ekspor dan tagihan lainnya',
                                        'Tagihan akseptasi pihak ketiga',
                                        'Tagihan derivatif pihak berelasi',
                                        'Pinjaman yang diberikan pihak ketiga',
                                        'Pinjaman yang diberikan pihak berelasi',
                                        'Piutang retensi pihak ketiga',
                                        'Biaya dibayar dimuka lancar',
                                        'Uang muka lancar lainnya',
                                        'Piutang ijarah pihak ketiga',
                                        'Piutang ijarah pihak berelasi',
                                        'Piutang pembiayaan konsumen pihak ketiga',
                                        'Piutang pembiayaan konsumen pihak berelasi',
                                        'Piutang nasabah pihak ketiga',
                                        'Piutang murabahah pihak ketiga',
                                        'Cadangan kerugian penurunan nilai pada piutang murabahah',
                                        'Piutang ijarah pihak ketiga',
                                        'Piutang ijarah pihak berelasi',
                                        'Tagihan anjak piutang pihak berelasi']],
    ['jumlah_aset_tidak_lancar','2','CurrentYearInstant',['Properti investasi',
                                                        'Aset tetap',
                                                        'Aset lainnya',
                                                        'Agunan yang diambil alih']],
    ['jumlah_aset_tidak_lancar','2','CurrentYearInstant','Jumlah aset tidak lancar'],                                                    
    ['jumlah_aset','2','CurrentYearInstant','Jumlah aset'],
    ['jumlah_liabilitas_jangka_pendek','2','CurrentYearInstant',['Liabilitas segera',
                                                                'Giro pihak ketiga',
                                                                'Giro pihak berelasi',
                                                                'Tabungan pihak ketiga',
                                                                'Tabungan pihak berelasi',
                                                                'Deposito berjangka pihak ketiga',
                                                                'Deposito berjangka pihak berelasi',
                                                                'Simpanan dari bank lain',
                                                                'Liabilitas derivatif pihak berelasi',
                                                                'Liabilitas akseptasi',
                                                                'Pinjaman yang diterima pihak ketiga',
                                                                'Obligasi',
                                                                'Estimasi kerugian komitmen dan kontinjensi',
                                                                'Utang pajak',
                                                                'Utang reasuransi',
                                                                'Utang komisi',
                                                                'Utang klaim',
                                                                'Utang pajak']],
    ['jumlah_liabilitas_jangka_pendek','2','CurrentYearInstant','Jumlah liabilitas jangka pendek'],                                                                                                                    
    
    ['jumlah_liabilitas_jangka_panjang','2','CurrentYearInstant',['Liabilitas asuransi atas premi yang belum merupakan pendapatan',
                                                                'Liabilitas asuransi atas estimasi liabilitas klaim',
                                                                'Kewajiban imbalan pasca kerja',
                                                                'Liabilitas lainnya',
                                                                'Kewajiban imbalan pasca kerja']],
    ['jumlah_liabilitas_jangka_panjang','2','CurrentYearInstant','Jumlah liabilitas jangka panjang'],                                                                                                                              
    ['jumlah_ekuitas','2','CurrentYearInstant','Jumlah ekuitas'],
    ['jumlah_liabilitas','2','CurrentYearInstant','Jumlah liabilitas'],
    ['jumlah_ekuitas','2','CurrentYearInstant','Jumlah ekuitas'],
    ['pendapatan','3','CurrentYearDuration',['Pendapatan bunga',
                                            'Pendapatan dari premi asuransi',
                                            'Pendapatan bunga dan keuangan',
                                            'Pendapatan dari murabahah dan istishna',
                                            'Pendapatan dari pembiayaan konsumen',
                                            'Pendapatan dari sewa pembiayaan',
                                            'Pendapatan administrasi',
                                            'Pendapatan dari provisi dan komisi',
                                            'Pendapatan dividen',
                                            'Penerimaan kembali aset yang telah dihapusbukukan',
                                            'Keuntungan (kerugian) selisih kurs mata uang asing',
                                            'Keuntungan (kerugian) pelepasan aset tetap',
                                            'Pendapatan pengelolaan dana oleh bank sebagai mudharib',
                                            'Pendapatan keuangan']],
    ['pendapatan','3','CurrentYearDuration','Penjualan dan pendapatan usaha'],                                    
    ['cogs','3','CurrentYearDuration',['Beban bunga','Beban bagi hasil',
                                    'Beban keuangan',
                                    'Pembentukan penyisihan kerugian penurunan nilai',
                                    'Beban penjualan',
                                    'Beban penjualan',
                                    'Beban penjualan',
                                    'Beban umum dan administrasi',
                                    'Beban penyusutan properti investasi, aset sewa, aset tetap, aset yang diambil alih dan aset ijarah',
                                    'Beban klaim',
                                    'Klaim reasuransi',
                                    'Klaim reasuransi',
                                    'Klaim reasuransi',
                                    'Beban underwriting lainnya',
                                    'Beban umum dan administrasi']],
    ['cogs','3','CurrentYearDuration','Beban pokok penjualan dan pendapatan'],
    ['cogs','3','CurrentYearDuration','Beban kerjasama operasi'],                                
    ['laba_bruto','3','CurrentYearDuration','Jumlah laba bruto'],
    ['laba_bruto','3','CurrentYearDuration','Jumlah laba (rugi) sebelum pajak penghasilan'],
    ['laba_rugi','3','CurrentYearDuration','Jumlah laba (rugi)'],
    ['laba_rugi_komprehensif','3','CurrentYearDuration','Jumlah laba rugi komprehensif'],
    ['EPS','3','CurrentYearDuration','Laba (rugi) per saham dasar dari operasi yang dilanjutkan'],
]


def list_cat(x):
    folder_list = os.listdir(x['folder_path'])
    value = np.nan
    for fd in folder_list:
        if "1210000.html" in fd:
            value = "General"
        elif "6220000.html" in fd:
            value = "Insurance"
        elif "1220000.html" in fd:
            value = "General - liquidity"
        elif "2210000.html" in fd:
            value = "Property"
        elif "8220000.html" in fd:
            value = "Finance Industry"
        elif "4220000.html" in fd :
            value = "Financial and Shariah"
        elif "3210000.html" in fd :
            value = "Infrastructure Industry"
        elif "2220000.html" in fd :
            value = "Property"
        elif "5220000.html" in fd :
            value = "Securities Industry"
        elif "3220000.html" in fd :
            value = "Infrastructure Industry - liqudity"
    return value

def data_func(data):
    val={}
    folder_path = data['folder_path']
    val['Company'] = data['Company']
    val['Tahun_Buku'] = data['Tahun_Buku']
    val['Tanggal Rilis'] = data['Date']
    

    for x in register:

        try:
            dire = os.listdir(folder_path)
            for file_name in dire:
                if x[1] in file_name[1]:
                    file_path = file_name
                    
            if type(x[3]) == list:
                val[f'{x[0]}'] = g.get_multiple_data(folder_path,file_path,x[2],x[3])
                    
            else:  
                val[f'{x[0]}'] = g.get_data(folder_path,file_path,x[2],x[3])
            
        except:
            pass

    return val

def avg_seven_day(x):
    company_code = f'{x["Company"]}.JK'
    start_date = x['Tanggal Rilis'].strftime('%Y-%m-%d')
    end_date = x['End of Next Month'].strftime('%Y-%m-%d')

    ticker = yf.Ticker(company_code)
    data = ticker.history(start=start_date, end=end_date)
    value = data['Close'].head(7).mean()
    x['7D_Avg'] = value
    return x

def jumlah_aset_tidak_lancar(data):
    data['jumlah_aset_tidak_lancar'] = data['jumlah_aset'] - data['jumlah_aset_lancar']
    return data

def jumlah_liabilitas_jangka_pendek(data):
    data['jumlah_liabilitas_jangka_pendek'] = data['jumlah_liabilitas'] - data['jumlah_liabilitas_jangka_panjang']
    return data

def pendapatan_cogs(data):
    laba_bruto_null = data.copy()
    laba_bruto_null = laba_bruto_null[laba_bruto_null['laba_bruto'].isnull()]

    laba_bruto = data.copy()
    laba_bruto = laba_bruto[~laba_bruto['laba_bruto'].isnull()]

    laba_bruto_null['laba_bruto'] = laba_bruto_null['pendapatan'] + laba_bruto_null['cogs']
    laba_bruto['cogs'] = laba_bruto['laba_bruto'] - laba_bruto['pendapatan']
    
    data_combine = pd.concat([laba_bruto,laba_bruto_null])
    return data_combine

if __name__ == '__main__':
    start_time = time.time()
    num_cpu = multiprocessing.cpu_count()
    cpu_var = math.floor(num_cpu * 0.75)
    
    print("------------------Loading------------------------")
   
   
    
    folder_list_ori = g.add_folder_columns()
    folder_list_ori['category'] = folder_list_ori.apply(lambda x:list_cat(x),axis=1)
    folder_list_ori.to_csv("category.csv",index=False)

    folder_list = folder_list_ori.to_dict('records')
    
    with Pool(cpu_var) as p:
        data = p.map(data_func,folder_list)
    
    val_list = pd.DataFrame(data)
    

    folder_list_ori['Company']=folder_list_ori[['Company']].astype(str)
    folder_list_ori = folder_list_ori.drop_duplicates(subset=['Company'],keep='first')
    folder_list_ori = folder_list_ori[['Company','category']]
    folder_list_ori = folder_list_ori.set_index('Company')
    val_list = val_list.join(folder_list_ori,on='Company',how='left')

    month_converter = {
        'Januari' : 'January',
        'Februari' : 'February',
        'Maret' : 'March',
        'April' : 'April',
        'Mei' : 'May',
        'Juni' : 'June',
        'Juli' : 'July',
        'Agustus' : 'August',
        'September' : 'September',
        'Oktober' : 'October',
        'November' : 'November',
        'Desember' : 'December'
    }

    for indonesia_month, english_month in month_converter.items():
        val_list['Tanggal Rilis'] = val_list['Tanggal Rilis'].str.replace(indonesia_month, english_month)
    
    date_format = "%d %B %Y | %H:%M"
    val_list['Tanggal Rilis'] = pd.to_datetime(val_list['Tanggal Rilis'],format=date_format)
    val_list['End of Next Month'] = val_list['Tanggal Rilis'] + timedelta(days=60)

    val_list = val_list.to_dict('records')

    with Pool(cpu_var) as p:
        val_list = p.map(avg_seven_day,val_list)
    
    val_list = pd.DataFrame(val_list)
    val_list.drop(['End of Next Month'],axis=1,inplace=True)
    val_list = val_list[val_list['laba_rugi'].notnull()]
    #val_list = jumlah_aset_tidak_lancar(val_list)
    #val_list = jumlah_liabilitas_jangka_pendek(val_list)
    #val_list = pendapatan_cogs(val_list)
    val_list.to_csv("data_raw.csv",index=False)

    print("------------------Done------------------------")
    end_time = time.time()
    execution_time = end_time - start_time

    
    print("Execution time:", execution_time, "seconds")


    


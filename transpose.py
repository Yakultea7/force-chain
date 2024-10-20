import pandas as pd

# 讀取 CSV 檔案
file_path = 'H:\\lab\\24_t=20s_30s.csv' 
chunk=58

for i in range(21):
    df = pd.read_csv(file_path,skiprows=365+(chunk*i)+i*2,nrows=chunk,header=None) #讀取每區塊

    selected_rows = df.iloc[[0,1, 2, 3, 4, 12 , 13] , :] #取得需要的參數

    CF_values = pd.to_numeric(df.iloc[26, 1:]) #取得合力數列
    CF_mean = CF_values.mean() #計算合力平均
    comparison_result = (CF_values > CF_mean).astype(int) #比較

    selected_T = selected_rows.T #轉置
    selected_T['FC_Result'] = comparison_result.T #轉置力鏈判斷加進去

    output_file = f'TIME_{200+i*5}.csv'
    selected_T.to_csv(output_file, index=False)
    
    print(f'Saved: {output_file}')

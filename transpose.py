import pandas as pd
import re
import numpy as np
from pathlib import Path

# 取得目前程序的工作路徑
current_directory = Path.cwd()

# 要存取的檔案名稱
file_name = '24_t=20s_30s.csv'

# 拼接完整的路徑
file_path = current_directory / file_name

chunk = 58
i=0
# 定義清理函數
def clean_string(value):
    if isinstance(value, str):  # 確保處理的數據是字串
        # 刪除 "QXX"、空白字符，並刪除結尾的冒號
        return re.sub(r'Q\d+\s*:\s*|\s+|:$', '', value)
    return value  # 如果不是字串則原樣返回

for i in range(21):

    df = pd.read_csv(file_path, skiprows=365 + (chunk * i) + i * 2, nrows=chunk, header=None)  # 讀取每區塊
    
    # 取得需要的參數
    selected_rows = df.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13], :]
    
    # 取得總力數列-------------------------------------------------------------------------------------------------------------------------
    TF_values = pd.to_numeric(df.iloc[52, 1:])
    TF_mean = TF_values.mean()  # 計算總力平均
    comparisonF_result = (TF_values > TF_mean).astype(int)  # 比較
    comparisonF_result.loc[0] = "FC"  # index 第1列填入 
    # ------------------------------------------------------------------------------------------------------------------------------------
    
    
    
    
    # 取得X速度數列-------------------------------------------------------------------------------------------------------------------------
    Vx_values = pd.to_numeric(df.iloc[2, 1:])
    Vx_mean = Vx_values.mean()  # 計算Vx平均
    comparisonVx_result = (Vx_values > Vx_mean).astype(int)  # 比較
    comparisonVx_result.loc[0] = "VxC"  # index 第1列填入 
    # ------------------------------------------------------------------------------------------------------------------------------------
    
    # 取得Y速度數列-------------------------------------------------------------------------------------------------------------------------
    Vy_values = pd.to_numeric(df.iloc[3, 1:])
    Vy_mean = Vy_values.mean()  # 計算Vy平均
    comparisonVy_result = (Vy_values > Vy_mean).astype(int)  # 比較
    comparisonVy_result.loc[0] = "VyC"  # index 第1列填入 
    # ------------------------------------------------------------------------------------------------------------------------------------
    
    # 取得Z速度數列-------------------------------------------------------------------------------------------------------------------------
    Vz_values = pd.to_numeric(df.iloc[4, 1:])
    Vz_mean = Vz_values.mean()  # 計算Vz平均
    comparisonVz_result = (Vz_values > Vz_mean).astype(int)  # 比較
    comparisonVz_result.loc[0] = "VzC"  # index 第1列填入 
    # ------------------------------------------------------------------------------------------------------------------------------------
    
    
    
    
    
    # 計算體積分率 (Vol%)------------------------------------------------------------------------------------------------------------------
    # 抓取 Position X, Y, Z 資料
    positions = df.loc[9:11,1:].values.T
    positions = positions.astype(float)
         
    n = positions.shape[0]
    radius = 10  # 設定半徑為 10
    neighbor_counts = np.zeros(n)  # 用來儲存每個點的鄰近點數量，根據實際資料點數量初始化
    
    # 計算每個點在半徑範圍內的鄰近點數量
    for i2 in range(n):
    
        # 計算與其他所有點的距離
        distances = np.linalg.norm(positions - positions[i2], axis=1)
        # 計算在半徑內的點數，排除自己
        neighbor_counts[i2] = np.sum((distances <= radius) & (distances > 0))
        

    # 計算公式 vol%  目前使用所有顆粒同樣直徑
    pi = np.pi
    vol_percent = ((4/3) * pi * (radius ** 3) * neighbor_counts) / (2 * radius)
    # 將 vol_percent 插入至 DataFrame 作為第一筆資料
    # 我們需要先將 vol_percent 轉換成 DataFrame，並指定列名為 'vol_percent'
    vol_percent_df = pd.DataFrame(["vol_percent"] + list(vol_percent), columns=['vol_percent'])
    
    #--------------------------------------------------------------------------------------------------------------------------------------
    
    
    
    
    
    # 轉置
    selected_T = selected_rows.T
    
    # 將體積分率&力鏈判斷加進去
    selected_T['vol_percent_df'] = vol_percent_df
    selected_T['comparisonVx'] = comparisonVx_result
    selected_T['comparisonVy'] = comparisonVy_result
    selected_T['comparisonVz'] = comparisonVz_result
    selected_T['FC'] = comparisonF_result
    
    # 對轉置後的第一行進行正規表示式處理
    selected_T.loc[0, :] = selected_T.loc[0, :].apply(clean_string)
    
    # 輸出為 CSV 文件
    output_file = f'TIME_{200 + i * 5}.csv'
    selected_T.to_csv(output_file, index=False, header=False)
    
    print(f'Saved: {output_file}')

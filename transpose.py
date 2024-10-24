import pandas as pd
import re
from pathlib import Path

# 取得目前程序的工作路徑
current_directory = Path.cwd()

# 要存取的檔案名稱
file_name = '24_t=20s_30s.csv'

# 拼接完整的路徑
file_path = current_directory / file_name

chunk = 58

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

    # 取得總力數列
    TF_values = pd.to_numeric(df.iloc[52, 1:])
    TF_mean = TF_values.mean()  # 計算總力平均
    comparison_result = (TF_values > TF_mean).astype(int)  # 比較
    comparison_result.loc[0] = "FC"  # index 第1列填入 FC

    # 轉置
    selected_T = selected_rows.T

    # 將力鏈判斷加進去
    selected_T['comparison_result'] = comparison_result

    # 對轉置後的第一行進行正規表示式處理
    selected_T.loc[0, :] = selected_T.loc[0, :].apply(clean_string)

    # 輸出為 CSV 文件
    output_file = f'TIME_{200 + i * 5}.csv'
    selected_T.to_csv(output_file, index=False, header=False)

    print(f'Saved: {output_file}')

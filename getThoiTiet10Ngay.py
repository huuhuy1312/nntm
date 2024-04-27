import pandas as pd
import numpy as np
# Đọc file CSV
df = pd.read_csv('sensor_data.csv')

# Lọc các hàng có trạng thái là "Da Thu Hoach"
filtered_df = df[df['trang_thai'] == 'Da Thu Hoach']

# Lấy danh sách các chỉ mục và chèn số 0 vào đầu mảng
indices = filtered_df.index.tolist()
indices.insert(0, 0)
print(indices)
# Tính trung bình của 3 hàng cạnh nhau từ các phạm vi đã chọn
result = []
ndo_tb_csv =[]
doam_tb_csv =[]
san_luong_csv =[]
for i in range(len(indices)-1):
    start = indices[i]
    end = indices[i]+120
    san_luong_csv.append(df.iloc[indices[i+1]]["san_luong"])
    print(indices[i])
    khoang_gia_tri = df.iloc[start:end]
    khoang_gia_tri_chia = np.array_split(khoang_gia_tri,40)

    ndo_tb = [round(x["nhiet_do"].mean(),2) for x in khoang_gia_tri_chia]
    doam_tb = [round(x["do_am"].mean(),2) for x in khoang_gia_tri_chia]

    ndo_tb_csv.append(ndo_tb)
    doam_tb_csv.append(doam_tb)

# print(ndo_tb_csv)
# print(doam_tb_csv)
print(san_luong_csv)
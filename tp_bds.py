


import pandas as pd
import time
# Đọc dữ liệu từ file CSV
df = pd.read_csv('sensor_data.csv')
start_time = time.time()
def tim_vi_tri_thoi_gian(df, thoi_gian_bat_dau, thoi_gian_ket_thuc):
    # Lọc dữ liệu theo thời gian bắt đầu và kết thúc
    df_filtered = df[(df['thoi_gian'] == thoi_gian_bat_dau) | (df['thoi_gian'] == thoi_gian_ket_thuc)]

    # Lấy chỉ mục của thời gian bắt đầu và kết thúc
    vi_tri_thoi_gian_bat_dau = df_filtered.index[df_filtered['thoi_gian'] == thoi_gian_bat_dau].tolist()
    vi_tri_thoi_gian_ket_thuc = df_filtered.index[df_filtered['thoi_gian'] == thoi_gian_ket_thuc].tolist()

    return vi_tri_thoi_gian_bat_dau, vi_tri_thoi_gian_ket_thuc

def tinh_trung_binh_nhiet_do(df, vi_tri_thoi_gian_bat_dau, vi_tri_thoi_gian_ket_thuc):
    # Tính số lượng phần tử
    so_luong = abs(vi_tri_thoi_gian_ket_thuc - vi_tri_thoi_gian_bat_dau) + 1
    
    # Chia dữ liệu thành 11 phần
    so_phan_chia = 11
    so_phan_con_lai = so_luong % so_phan_chia
    so_phan = so_luong // so_phan_chia
    print(so_luong)
    print(so_phan)
    # Tính trung bình nhiệt độ cho mỗi phần
    nhiet_do_trung_binh = []
    for i in range(so_phan_chia+1):
        print(i)
        if i < so_phan_chia:
            start = vi_tri_thoi_gian_bat_dau + i * so_phan
            end = start + so_phan
            print(start ,end)
            nhiet_do_trung_binh.append({round(df['nhiet_do'][start:end].mean(),2), df['thoi_gian'][start], df['thoi_gian'][end]})
        else:
            print(vi_tri_thoi_gian_ket_thuc-so_phan_con_lai+1,vi_tri_thoi_gian_ket_thuc+1 )
            nhiet_do_trung_binh.append({round(df['nhiet_do'][vi_tri_thoi_gian_ket_thuc-so_phan_con_lai+1:vi_tri_thoi_gian_ket_thuc+1].mean(),2),df['thoi_gian'][vi_tri_thoi_gian_ket_thuc-so_phan_con_lai+1], df['thoi_gian'][vi_tri_thoi_gian_ket_thuc]})
    return nhiet_do_trung_binh

# Thời gian bắt đầu và kết thúc
thoi_gian_bat_dau = '2024-03-20 10:00:00'
thoi_gian_ket_thuc = '2024-05-10 20:00:00'

# Tìm vị trí của thời gian bắt đầu và kết thúc
vi_tri_thoi_gian_bat_dau, vi_tri_thoi_gian_ket_thuc = tim_vi_tri_thoi_gian(df, thoi_gian_bat_dau, thoi_gian_ket_thuc)

# Tính trung bình nhiệt độ của 12 phần
nhiet_do_trung_binh = tinh_trung_binh_nhiet_do(df, vi_tri_thoi_gian_bat_dau[0], vi_tri_thoi_gian_ket_thuc[0])
end_time = time.time()
print("Trung bình nhiệt độ của 12 phần là:")
print(nhiet_do_trung_binh)
execution_time = end_time - start_time
print(execution_time)

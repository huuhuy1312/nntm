import pandas as pd
import time

# Đọc file CSV vào DataFrame
start_time = time.time()
df = pd.read_csv('sensor_data.csv')

# Chuyển cột 'thoi_gian' thành kiểu datetime
df['thoi_gian'] = pd.to_datetime(df['thoi_gian'])

# Đầu vào là một mảng gồm 10 giá trị, mỗi giá trị gồm {time, nhiet_do, do_am}
input_data = [
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20},
    {'nhiet_do': 22.80, 'do_am': 58.20}
]

# Chuyển đổi đầu vào thành DataFrame
input_df = pd.DataFrame(input_data)

# Tìm vị trí bắt đầu của 10 giá trị liên tiếp cạnh nhau có độ lệch nhỏ nhất
min_diff = float('inf')  # Giá trị độ lệch nhỏ nhất ban đầu
start_index = 0

for i in range(len(df) - len(input_df) + 1):
    sub_df = df.iloc[i:i+len(input_df)].reset_index(drop=True)  # Reset index
    diff = abs((sub_df['nhiet_do'] - input_df['nhiet_do']).sum() +abs(sub_df['do_am'] - input_df['do_am']).sum())
    print(diff)
    if diff < min_diff:
        min_diff = diff
        start_index = i

# Lấy ra 10 giá trị liên tiếp có độ lệch nhỏ nhất
result = df.iloc[start_index:start_index+len(input_df)]
end_time = time.time()

# In kết quả
print(result)
execution_time = end_time - start_time
print("Thời gian đọc file: {:.2f} giây".format(execution_time))
print(min_diff)

# import pandas as pd
# import numpy as np
# import time

# # Đọc file CSV vào DataFrame
# df = pd.read_csv('sensor_data.csv')

# # Chuyển cột 'thoi_gian' thành kiểu datetime
# df['thoi_gian'] = pd.to_datetime(df['thoi_gian'])

# # Đầu vào là một mảng gồm 10 giá trị, mỗi giá trị gồm {thoi_gian, nhiet_do, do_am}
# input_data = [
#     {'thoi_gian': '2024-03-20 10:00:00', 'nhiet_do': 22.80, 'do_am': 58.20},
#     {'thoi_gian': '2024-03-20 11:00:00', 'nhiet_do': 23.10, 'do_am': 57.80},
#     {'thoi_gian': '2024-03-20 12:00:00', 'nhiet_do': 23.40, 'do_am': 57.50},
#     {'thoi_gian': '2024-03-20 13:00:00', 'nhiet_do': 23.70, 'do_am': 57.20},
#     {'thoi_gian': '2024-03-20 14:00:00', 'nhiet_do': 24.00, 'do_am': 56.90},
#     {'thoi_gian': '2024-03-20 15:00:00', 'nhiet_do': 24.30, 'do_am': 56.60},
#     {'thoi_gian': '2024-03-20 16:00:00', 'nhiet_do': 24.60, 'do_am': 56.30},
#     {'thoi_gian': '2024-03-20 17:00:00', 'nhiet_do': 24.90, 'do_am': 56.00},
#     {'thoi_gian': '2024-03-20 18:00:00', 'nhiet_do': 25.20, 'do_am': 55.70},
#     {'thoi_gian': '2024-03-20 19:00:00', 'nhiet_do': 25.50, 'do_am': 55.40}
# ]

# # Chuyển đổi đầu vào thành DataFrame
# input_df = pd.DataFrame(input_data)
# input_df['thoi_gian'] = pd.to_datetime(input_df['thoi_gian'])

# # Tính độ lệch giữa dự đoán và dữ liệu thời tiết trong CSV
# temp_diff = np.abs(df['nhiet_do'].values[:, None] - input_df['nhiet_do'].values)
# humidity_diff = np.abs(df['do_am'].values[:, None] - input_df['do_am'].values)
# print(temp_diff)
# print(humidity_diff.sum(axis=1))
# # Tính tổng độ lệch tại mỗi vị trí
# total_diff = temp_diff + humidity_diff

# # Tìm vị trí bắt đầu của 10 giờ liên tiếp có độ lệch nhỏ nhất
# start_index = total_diff.sum(axis=1).argmin()

# # Lấy ra 10 giờ liên tiếp có độ lệch nhỏ nhất
# result = df.iloc[start_index:start_index+len(input_df)]
# print(result)
# print(total_diff.sum(axis=1).min())
# # Tính tên cây trồng phù hợp dựa trên dữ liệu thời tiết trong khoảng thời gian này
# # Đây chỉ là một ví dụ, bạn có thể áp dụng các quy tắc hoặc mô hình phức tạp hơn
# # ở đây, tôi giả định rằng nhiệt độ và độ ẩm đều quan trọng để quyết định cây trồng phù hợp
# suitable_crop = ""
# if result['nhiet_do'].mean() > 25 and result['do_am'].mean() > 60:
#     suitable_crop = "Cà chua"
# elif result['nhiet_do'].mean() > 20 and result['do_am'].mean() > 50:
#     suitable_crop = "Dưa hấu"
# else:
#     suitable_crop = "Không có cây trồng phù hợp"

# print("Tên cây trồng phù hợp: ", suitable_crop)

# import pandas as pd
# import numpy as np
# import time

# # Đọc file CSV vào DataFrame
# df = pd.read_csv('sensor_data.csv')

# # Chuyển cột 'thoi_gian' thành kiểu datetime
# df['thoi_gian'] = pd.to_datetime(df['thoi_gian'])

# # Đầu vào là một mảng gồm 10 giá trị, mỗi giá trị gồm {nhiet_do, do_am}
# input_data = [
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20},
#     {'nhiet_do': 22.80, 'do_am': 58.20}
# ]

# # Chuyển đổi đầu vào thành DataFrame
# input_df = pd.DataFrame(input_data)

# # Tính toán hiệu của mỗi cặp 10 dòng trong tập tin CSV và 10 dòng dữ liệu đầu vào
# # Bạn có thể sử dụng một vòng lặp để tính hiệu cho từng cặp dòng
# # ở đây là ví dụ về cách tính toán cho cặp đầu tiên
# start_indices = range(len(df) - 9)  # List các chỉ số bắt đầu của các cặp dòng trong tập tin CSV
# differences = []  # Danh sách để lưu trữ các hiệu
# for start_index in start_indices:
#     # Lấy ra 10 dòng từ tập tin CSV
#     subset_df = df.iloc[start_index:start_index+10]
#     # Tính hiệu với 10 dòng từ dữ liệu đầu vào
#     diff = np.abs(subset_df['nhiet_do'].values - input_df['nhiet_do'].values) + \
#            np.abs(subset_df['do_am'].values - input_df['do_am'].values)
#     # Lưu trữ hiệu vào danh sách
#     differences.append(diff.sum())

# # Tìm vị trí của cặp 10 dòng có độ lệch nhỏ nhất
# min_index = np.argmin(differences)
# print(np.min(differences))
# # Lấy ra 10 dòng có độ lệch nhỏ nhất
# result = df.iloc[min_index:min_index+10]

# # In kết quả
# print(result)


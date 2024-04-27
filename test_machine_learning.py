# Import các thư viện cần thiết
import numpy as np
from sklearn.linear_model import LinearRegression
import time

start_time = time.time()

# Dữ liệu mẫu: nhiệt độ và độ ẩm trung bình của các cây trồng
X = np.array([[[20, 21, 22], [21, 22, 24]],
              [[24, 26, 27], [23, 24, 26]],
              [[24, 26, 27], [28, 29, 30]]])

# Chỉ số hiệu suất của các cây trồng tương ứng
y = np.array([0.4, 0.6, 0.5])

X_reshaped = X.reshape(X.shape[0], -1)

model = LinearRegression()
model.fit(X_reshaped, y)
new_data = np.array([[22.6, 26, 27],[23, 24, 26]])
new_data_reshaped = new_data.reshape(1, -1)
predicted_performance = model.predict(new_data_reshaped)

end_time = time.time()
print("Thời gian chạy: ", end_time - start_time)
print("Chỉ số hiệu suất dự đoán:", predicted_performance)



# Import các thư viện cần thiết
# import numpy as np
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import Ridge
# from sklearn.pipeline import make_pipeline
# import time

# start_time = time.time()

# # Dữ liệu mẫu: nhiệt độ và độ ẩm trung bình của các cây trồng
# X = np.array([[22, 60],
#               [24, 65],
#               [23, 70]])

# # Chỉ số hiệu suất của các cây trồng tương ứng
# y = np.array([0.4, 0.6, 0.5])

# # Khởi tạo mô hình hồi quy Ridge
# model = make_pipeline(PolynomialFeatures(degree=2), Ridge(alpha=0.1))

# # Huấn luyện mô hình trên dữ liệu
# model.fit(X, y)

# # Dự đoán chỉ số hiệu suất cho cây trồng mới với nhiệt độ 22.6 và độ ẩm 63.5%
# new_data = np.array([[22.6, 63.5]])
# predicted_performance = model.predict(new_data)

# end_time = time.time()

# print("Thời gian huấn luyện và dự đoán:", end_time-start_time)
# print("Chỉ số hiệu suất dự đoán:", predicted_performance)


# import numpy as np
# from sklearn.linear_model import LinearRegression

# # Dữ liệu đầu vào
# nhiet_do_tuong_lai = np.array([20, 21, 22, 23, 23])
# do_am_tuong_lai = np.array([50, 60, 65, 61, 62.8])
# nhiet_do = np.array([[21, 23, 24, 26, 25], [23, 22, 21, 21.6, 23], [25, 26, 27, 29, 30]])
# do_am = np.array([[60, 65, 64, 63, 61.8], [65, 66, 64.6, 67, 65], [61, 66, 65, 67, 68]])
# chi_so_hieu_suat = np.array([0.1, 0.3, 0.4])

# # Xây dựng ma trận đặc trưng và vector kết quả
# X = np.column_stack((nhiet_do.flatten(), do_am.flatten()))
# y = chi_so_hieu_suat.repeat(5)  # Lặp lại mảng chi_so_hieu_suat để khớp với số lượng mẫu

# # Khởi tạo và huấn luyện mô hình hồi quy tuyến tính
# model = LinearRegression()
# model.fit(X, y)

# # Dự đoán chỉ số hiệu suất cho 30 giờ tương lai
# nhiet_do_tuong_lai_reshape = nhiet_do_tuong_lai.reshape(-1, 1)
# do_am_tuong_lai_reshape = do_am_tuong_lai.reshape(-1, 1)
# X_tuong_lai = np.column_stack((nhiet_do_tuong_lai_reshape, do_am_tuong_lai_reshape))
# chi_so_hieu_suat_tuong_lai = model.predict(X_tuong_lai)

# print("Chỉ số hiệu suất dự đoán cho 30 giờ tương lai:", chi_so_hieu_suat_tuong_lai)





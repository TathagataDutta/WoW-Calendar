# try:
#     x = 1 / 1
#     print(x)
#     x = 1 / 0
#     print(x)
#     x = 1 / 2
#     print(x)
# except:
#     print("Error")

from datetime import datetime, timedelta

data = datetime.now()
# diff = timedelta(hours=2, minutes=30)

# # print(data.hour)
# # print(type(data.hour))

# diff

# # print(diff)
# # print(type(data))
# # a = str(diff)
# # # b = timedelta(a)
# # print(a)
# new = data + diff
# # print(new)

# x = datetime.now() - datetime.now()
# print(type(x))
# print(x)

print(data)
str_data = str(data)
new_data = datetime.strptime(str_data, "%Y-%m-%d %H:%M:%S.%f")
print(new_data)

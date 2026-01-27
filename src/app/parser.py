import json

def mrz_checksum(data):
    weights = [7, 3, 1]
    total = 0

    for i, c in enumerate(data):
        if c.isdigit():
            v = int(c)
        else:
            v = 0
        total += v * weights[i % 3]
    return str(total % 10)

# сравнение даты из запроса и mrz
def compare_date(mrz_data, req_data):
    data = req_data.split('.')
    date = data[2][2:4] + data[1] + data[0]
    return mrz_data == date

with open('request.json', 'r') as f:
    request = json.load(f)

line1, line2 = request['mrz'].splitlines()

# чтение первой строки
doc_type = line1[0:2]
country = line1[2:5]
names = line1[5:44].strip('<').split('<<')
last_name = names[0]
first_name = names[1]
middle_name = names[2]

#чтение второй строки
doc_number = line2[0:9]
doc_check = line2[9]
nationality = line2[10:13]
birth_date = line2[13:19]
birth_date_check = line2[19]
sex = line2[20]
expiry_date = line2[21:27]
expiry_date_check = line2[27]
personal_code = line2[28:42]
personal_code_check = line2[42]
end_check = line2[43]

print(compare_date(birth_date, request['birth_date']))
print(names)


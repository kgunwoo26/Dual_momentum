import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pandas_datareader as pdr

update_period = 6  # 포트폴리오 정비 주기
check_term = 3  # 조사 주기
seed_money = 100
file_name = 'resources/test.csv'
snp_file_name = 'resources/S&P 500 내역.csv'
target_date = datetime(2022, 6, 7)  # 기준 날짜 설정, 최대 22/06/07

start_date = target_date
date_list = list()
snp_data = list()

def date_to_string_month(date: datetime) -> str:  # 날짜 스트링 형태로 변경
    return date.strftime('%y/%m')



def date_to_string(date: datetime) -> str:  # 날짜 스트링 형태로 변경
    return date.strftime('%y/%m/%d')


while '05/06/07' < date_to_string(start_date):  # 기준 날짜와 정비 주기 기준으로 시작 날짜 설정
    date_list.append(date_to_string_month(start_date))
    start_date = start_date + relativedelta(months=-update_period)

temp = date_list[::-1]
date_list =temp
check_date = start_date + relativedelta(months=update_period)


def cal_gap(new_val: float, old_val: float):  # 전 시점 대비 수익률 계산
    if old_val != '' and new_val != '':
            # and type(old_val) is not str and type(new_val) is not str:
        exp = (float(new_val) / float(old_val) - 1) * 100
        return exp
        # (float(new_val) / float(old_val) - 1) * 100 if float(old_val) != '' and float(new_val) != '' else ''
    else:
        return ''


def load_snp_list():
    data = list()
    with open(snp_file_name , 'r') as f:
        reader = csv.reader(f)
        next(reader)  # 종목명 열 패스
        for i in reader:
            rate = i[6].split("%")[0]
            data.append(rate)
    return data


# def get_snp500(start_date: datetime.datetime, end_date: datetime.datetime) -> float:
#     close_datas = pdr.get_data_yahoo('^GSPC', start_date, end_date)['Close']
#
#     ## For check datas from yahoo finance.
#     # for data in close_datas:
#     #     print(data)
#
#     first_value = close_datas[0]
#     last_value = close_datas[close_datas.size - 1]
#
#     print(f'start date\'s value is {first_value} ({start_date})')
#     print(f'last date\'s value is {last_value} ({end_date})')
#
#     revenue = last_value - first_value
#
#     return revenue


def create_compare_list(date, term):
    mcheck_term = term
    check_date= date
    check_date_List = list()
    compare_list = list()
    check_date_string = date_to_string(check_date)
    pre_list = list()
    p_found = c_found = 0
    pre_date = None

    with open(file_name , 'r') as f:
        reader = csv.reader(f)
        next(reader)  # 종목명 열 패스

        for i in reader:
            if i[0] == check_date_string and p_found == 0:  # 날짜를 찾은 경우
                pre_list.append(i)
                check_date = check_date + relativedelta(months=mcheck_term)  # TODO: Assigning values to parameter is awkward.
                check_date_string = date_to_string(check_date)
                p_found = 1
            elif i[0] >= check_date_string and p_found == 0:
                if pre_date != None and len(pre_date) != 0:
                    pre_list.append(pre_date)
                    # TODO: What is different with line 64-66? - 해당 날짜에 없을 경우 (6월 7일 휴장인 경우) 그 이전 데이터 가져오도록 구분했습니다
                    check_date = check_date + relativedelta(months=mcheck_term)
                    check_date_string = date_to_string(check_date)
                    p_found = 1

                    # print(pre_date[0])
            pre_date = i  # 마지막 조회 날짜 저장

            if i[0] == check_date_string and c_found == 0:  # 날짜를 찾은 경우
                check_date_List.append(i)
                break
                # print(check_date_string)
            elif i[0] >= check_date_string and c_found == 0:
                if pre_date != 0:
                    check_date_List.append(pre_date)
                    break
            pre_date = i  # 마지막 조회 날짜 저장

    # print(check_date_List)
    # print(pre_list)
    for num in check_date_List:
        i = 0
        for price in num:
            if len(pre_list) != 0 and i!=0:  # To prevent out of index of `pre_list`.
                compare_list.append(cal_gap(price, pre_list[0][i]))
            i += 1

    return compare_list

def find_stock_name(num):
    with open(file_name , 'r') as f:
        reader = csv.reader(f)
        name_list = next(reader)  # 종목명 열 패스
    return name_list[num]


def cal_highest_stock(date, term ):
    check_date = date
    check_term = term
    best_stock: str

    num_max = -1
    check_date = check_date + relativedelta(months=-check_term)

    compare_list = create_compare_list(check_date,check_term)


    if len(compare_list) != 0:  # max값을 지정
        count_max = 0
        max = -100
        for value in compare_list:
            if value != '' and value > max:
                num_max = count_max
                max = value
            count_max += 1
        best_stock = num_max + 1;
        # print( "win=", find_stock_name(best_stock), "max:", max)
    return num_max +1


result_list = list()

def check_earning(date, period ,count):
    check_date = date
    update_period = period
    check_date_string = date_to_string(check_date)
    list_count = count

    with open(file_name , 'r') as f:
        reader = csv.reader(f)

        next(reader)  # 종목명 열 패스

        pre_price = None
        now_price = None

        for i in reader:

            if i[0] == check_date_string :  # 날짜를 찾은 경우

                check_date = check_date + relativedelta(months=update_period)
                check_date_string = date_to_string(check_date)
                now_price = i[result_list[list_count]]
                if pre_price != None and result_list[list_count] != 0:
                    earn_rate = cal_gap(now_price, pre_price)
                    return earn_rate
                pre_price = now_price

            elif i[0] >= check_date_string :
                if len(pre_date) != 0:
                    now_price = pre_date[result_list[list_count]]
                    check_date = check_date + relativedelta(months=update_period)
                    check_date_string = date_to_string(check_date)

                    if pre_price != None and result_list[list_count] != 0:
                        earn_rate = cal_gap(now_price, pre_price)
                        return earn_rate
                    pre_price = now_price

            pre_date = i



def check_earning_snp(date, term ,count):
    check_date = date
    check_term = term
    check_date_string = date_to_string(check_date)
    list_count = count

    with open(snp_file_name , 'r') as f:
        reader = csv.reader(f)

        next(reader)  # 종목명 열 패스

        pre_price = None
        now_price = None

        for i in reader:

            if i[0] == check_date_string :  # 날짜를 찾은 경우
                check_date = check_date + relativedelta(months=check_term)
                return float(i[6].split("%")[0])

            elif i[0] >= check_date_string :
                if len(pre_date) != 0:
                    now_price = pre_date[6]
                    check_date = check_date + relativedelta(months=check_term)
                    check_date_string = date_to_string(check_date)
                    if pre_price != None and i[6] != 0:
                        return float(i[6].split("%")[0])


            pre_date = i








date = check_date

while date_to_string(date) <= '22/06/07':
    date = date + relativedelta(months=update_period)
    # print("\n\n", "start date:", check_date)
    result_list.append(cal_highest_stock(date, check_term))

money_list = list()
money_list_snp = list()
snp_data = load_snp_list()
date = check_date

money =seed_money

for i in snp_data:
    earing = float(i)
    money = money * (earing + 100) / 100
    money_list_snp.append(money)


list_count =0
money =seed_money

while date_to_string(check_date) <= '22/06/07':
    # print("\n\n", "start date:", check_date)
    check_date = check_date + relativedelta(months=update_period)
    earn_rate =check_earning(check_date,update_period, list_count)

    if type(earn_rate) == float:
        # if float(snp_data[snp_count]) <= earn_rate:
        money = money* (earn_rate + 100 ) /100
        # else:
        #     print("keep money", earn_rate)
    print(money, " ", earn_rate, ":", check_date)
    list_count +=1
    money_list.append(money)

size_of_snp_list = len(money_list_snp)
p_num = int(size_of_snp_list / len(money_list))
snp_list = list()

i=0
for i in range(len(money_list)):
    snp_list.append(money_list_snp[p_num*i])

plt.plot(date_list,money_list, label = 'dual momentum')
plt.plot(date_list,snp_list, label = 's&p')
plt.legend(loc='best', ncol =1, fontsize =10, frameon=True, shadow = True)
plt.xlabel("date")
plt.ylabel("money")
plt.title('earning')
plt.show()


#
# print(money_list)
# print(result_list)
# print(len(result_list))
# print(seed_money)

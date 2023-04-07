from requests import get
from bs4 import BeautifulSoup, CData
import re

# input을 통해 입력받은 값
# main.py에 작성
school_info = {
    # "office_of_education": "서울특별시교육청",
    # "school": "가락고등학교",
}

# 급식 정보
school_meal_info = {
    "KEY": "9da752136d5849b985288deb5036dba1",
    "Type": "xml",
    # 아래는 다 완성되면 지우자
    # 'ATPT_OFCDC_SC_CODE': 'B10', 
    # 'SD_SCHUL_CODE': '7010057',
    # main에서 입력받을 값
    # "MLSV_YMD": 202205
}

# 시간표 정보
school_time_info = {
    "KEY": "9da752136d5849b985288deb5036dba1",
    "Type": "xml",
    # 아래는 다 완성되면 지우자
    "ATPT_OFCDC_SC_CODE": "B10", 
    'SD_SCHUL_CODE': '7010057',
    # main에서 입력받을 값
    "AY": 2023,
    "SEM": 1,
    "ALL_TI_YMD": 202303
}

# URL 정보
school_url = {
    "base_url": "http://open.neis.go.kr/hub/",
    "basic_sub_url": "schoolInfo",
    "meal_sub_url": "mealServiceDietInfo",
    "time_sub_url": "hisTimetable"
}

# 급식 데이터
school_meal = {
    "mealInfo": []
}

# 시간표 데이터
time_table = {
    "timeInfo": []
}

# CData -> get_info = soup.find(text=lambda text: isinstance(text, CData))
# lambda 사용 : https://www.tomordonez.com/python-lambda-beautifulsoup/

# 배열 분할
def list_chunk(_list, n):
    return [_list[i:i+n] for i in range(0, len(_list), n)]

# 정규표현식
def regular_expression(_list) :

    global new_list

    new_list=[]

    for i in _list :
        text = re.sub('[a-zA-Z0-9.()]','',i).strip()
        if (text!="") :
            new_list.append(text)

    return new_list

# main.py로 부터 값을 받음
def get_info(**kwargs) :
    school_info.update(kwargs)

# 교육청 코드 + 학교 코드
def get_data() :

    global office_of_education_code, school_code

    URL = school_url["base_url"] + school_url["basic_sub_url"]

    # == response = get(URL, school_meal_info)
    response = get(f"{URL}?KEY={school_meal_info['KEY']}&Type={school_meal_info['Type']}")

    if response.status_code != 200 :
        print("Can't request website")
        print("This response code is ", response.status_code)
    else :
        print("Sucess!")
        soup = BeautifulSoup(response.text, "html.parser")

        office_of_education_name = soup.find(text=school_info["office_of_education"])
        office_of_education_code = office_of_education_name.find_previous(text=lambda text: isinstance(text, CData))
        school_meal_info.update({"ATPT_OFCDC_SC_CODE": office_of_education_code})
        school_time_info.update({"ATPT_OFCDC_SC_CODE": office_of_education_code})

        school_name = soup.find(text=school_info["school"])
        school_code = school_name.find_previous(text=lambda text: isinstance(text, CData))
        school_meal_info.update({"SD_SCHUL_CODE": school_code})
        school_time_info.update({"SD_SCHUL_CODE": school_code})

        school_meal_info.update({"MLSV_YMD": 202205})


# 급식 식단 정보
# @get_data
def meal_service() :
    global date_list, meal_list

    URL = school_url["base_url"] + school_url["meal_sub_url"]

    response = get(URL, school_meal_info)

    if response.status_code != 200 :
        print("Can't request website")
        print("This response code is ", response.status_code)
    else :
        print("Sucess!")
        soup = BeautifulSoup(response.text, "html.parser")

        total_cnt = int(soup.find("list_total_count").text)

        date_list = soup.find_all("mlsv_ymd")
        meal_list = soup.find_all("ddish_nm")

        for i in range(total_cnt) :
            date_list[i] = date_list[i].get_text()
            meal_list[i] = meal_list[i].get_text()

        meal_list = list_chunk(meal_list, 1)

        for i in range(total_cnt) :
            meal_str = "".join(meal_list[i])
            meal_str = meal_str.split("<br/>")
            meal_list[i] = regular_expression(meal_str)

        for i in range(total_cnt) :
            meal_info = {}
            meal_info.update({"office_of_education": school_info["office_of_education"]})
            meal_info.update({"school": school_info["school"]})
            meal_info.update({"date": date_list[i]})
            meal_info.update({"meal": meal_list[i]})
            school_meal["mealInfo"].append(meal_info)

        print(school_meal)
        return school_meal
       
# 고등학생 시간표 (준비중)
# @get_data
# def time_table(*args, **kwargs) :

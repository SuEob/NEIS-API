from requests import get
from bs4 import BeautifulSoup, CData # bs4은 html, xml들을 웹 크롤링 할때 사용
from datetime import datetime
import re # 정규표현식

# main.py에서 입력받은 값
school_info = {
    # "office_of_education": "서울특별시교육청",
    # "school": "가락고등학교",
}

# 급식 정보
school_meal_info = {
    "KEY": "9da752136d5849b985288deb5036dba1",
    "Type": "xml",
    "SCHUL_KND_SC_NM": "고등학교",

    # 아래는 다 완성되면 지우자
    # 'ATPT_OFCDC_SC_CODE': "B10", 
    # 'SD_SCHUL_CODE': "7010221",

    # # main에서 입력받을 값
    # "MLSV_YMD": "202204"
}

# 시간표 정보
school_time_info = {
    "KEY": "9da752136d5849b985288deb5036dba1",
    "Type": "xml",
    "SCHUL_KND_SC_NM": "고등학교",

    # 아래는 다 완성되면 지우자
    # "ATPT_OFCDC_SC_CODE": "B10", 
    # 'SD_SCHUL_CODE': '7010057',

    # main에서 입력받을 값
    # "AY": "2023",
    # "SEM": "1",
    # "GRADE": "1",
    # "CLASS_NM": "01",

    # 일주일치 날짜 바꿔도 되고 싫으면 말고
    "TI_FROM_YMD": "20230313",
    "TI_TO_YMD": "20230318"
    # "ALL_TI_YMD": "20230315"
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
    "schoolMeals": []
}

# 시간표 데이터
time_table = {
    "Mon": [],
    "Tue": [],
    "Wed": [],
    "Thu": [],
    "Fri": [],
    "Sat": []
}

# CData -> get_info = soup.find(text=lambda text: isinstance(text, CData))
# lambda 사용 : https://www.tomordonez.com/python-lambda-beautifulsoup/

# 배열 분할 -> _list를 원자n개씩 나눔
def list_chunk(_list, n):
    return [_list[i:i+n] for i in range(0, len(_list), n)]

# 정규표현식 -> _list에서 영어, 숫자, () 들을 제거
def regular_expression(_list) :

    global new_list

    new_list=[]

    for i in _list :
        text = re.sub('[a-zA-Z0-9.()]','',i).strip()
        if (text!="") :
            new_list.append(text)

    return new_list

# 요일 -> # 0: 월 ~ 6: 일
def get_day(date) :
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_of_the_week = date.weekday()

    return days[day_of_the_week]

# main.py에 있는 school_info 딕셔너리의 값을 업데이트함
def get_info(**kwargs) :
    school_info.update(kwargs)

# 교육청 코드 + 학교 코드
def get_data() :
    global office_of_education_code, school_code

    URL = school_url["base_url"] + school_url["basic_sub_url"]

    # response = get(URL, school_meal_info) 
    response = get(f"{URL}?KEY={school_meal_info['KEY']}&Type={school_meal_info['Type']}") # 위에껄로 해도 문제 없음

    if response.status_code != 200 : # 정확한 주소 X
        print("Can't request website")
        print("This response code is ", response.status_code)
    else : # 정확한 주소 O
        print("Sucess!")
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 교육청코드를 받아와서 딕셔너리에 업데이트
        office_of_education_name = soup.find(text=school_info["office_of_education"])
        office_of_education_code = office_of_education_name.find_previous(text=lambda text: isinstance(text, CData))
        school_meal_info.update({"ATPT_OFCDC_SC_CODE": office_of_education_code})
        school_time_info.update({"ATPT_OFCDC_SC_CODE": office_of_education_code})

        # 학교코드를 받아와서 딕셔너리에 업데이트
        school_name = soup.find(text=school_info["school"])
        school_code = school_name.find_previous(text=lambda text: isinstance(text, CData))
        school_meal_info.update({"SD_SCHUL_CODE": school_code})
        school_time_info.update({"SD_SCHUL_CODE": school_code})

        school_meal_info.update({"MLSV_YMD": "202204"})

        school_time_info.update({"AY": "2023"})
        school_time_info.update({"SEM": "1"})
        school_time_info.update({"GRADE": "1"})
        school_time_info.update({"CLASS_NM": "1"})


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

        # 총 급식 수
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

        # 딕셔너리에 업데이트
        for i in range(total_cnt) :
            meal_info = {}
            meal_info.update({"office_of_education": school_info["office_of_education"]})
            meal_info.update({"school": school_info["school"]})
            meal_info.update({"date": date_list[i]})
            meal_info.update({"meal": meal_list[i]})
            school_meal["schoolMeals"].append(meal_info)

        return school_meal
       
# 고등학생 시간표 (준비중)
# @get_data
def time_table_service() :

    global perio_list, itrt_cntnt_list

    URL = school_url["base_url"] + school_url["time_sub_url"]

    response = get(URL, school_time_info)
    
    if (response.status_code != 200) :
        print("Can't request website")
        print("This response code is ", response.status_code)
    else :
        print("Sucess!")
        soup = BeautifulSoup(response.text, "html.parser")
        # CLASS_NM="1"이 아니면 CLASS_NM="01"로 다시 찾기
        if (soup.find("code").text == "INFO-200") :
            school_time_info.update({"CLASS_NM": f"{'0'}1"})
            response = get(URL, school_time_info)
            soup = BeautifulSoup(response.text, "html.parser")

        # 총 수업 수
        total_cnt = int(soup.find("list_total_count").text)

        date_list = soup.find_all("all_ti_ymd")
        for i in range(total_cnt) :
            date_list[i] = date_list[i].get_text()

        # 일주일 중 요일마다 수업 수
        day_list_cnt=[]
        _cnt = 0
        for i in range(total_cnt) :
            _cnt += 1

            if (i != total_cnt-1 and date_list[i]!=date_list[i+1]) :
                day_list_cnt.append(_cnt)
                _cnt = 0

        date_list = sorted(list(set(date_list))) # set으로 중복을 줄이면 순서가 변화됨
        day_list_cnt.append(total_cnt - sum(day_list_cnt))

        perio_list = soup.find_all("perio")
        itrt_cntnt_list = soup.find_all("itrt_cntnt")

        for j in range(total_cnt) :
            perio_list[j] = perio_list[j].get_text()
            itrt_cntnt_list[j] = itrt_cntnt_list[j].get_text()

        # 요일 구하기 -> 0: 월 ~ 5: 토
        for i in range(len(day_list_cnt)) :
            date = datetime.strptime(date_list[i], "%Y%m%d")
            year = date.year
            month = date.month
            day = date.day

            day_of_the_week = get_day(datetime(year, month, day))

            # 딕셔너리에 업데이트
            for j in range(day_list_cnt[i]) :
                _sum = sum(day_list_cnt[0:i]) # 값을 누적시킴
                time_info = {}
                time_info.update({"office_of_education": school_info["office_of_education"]})
                time_info.update({"school": school_info["school"]})
                time_info.update({"day": day_of_the_week})
                time_info.update({"semester": school_time_info["SEM"]})
                time_info.update({"grade": school_time_info["GRADE"]})
                time_info.update({"perio": perio_list[_sum+j]})
                time_info.update({"class_name": school_time_info["CLASS_NM"]})
                time_info.update({"class_content": itrt_cntnt_list[_sum+j]})
                time_table[day_of_the_week].append(time_info)

        return time_table
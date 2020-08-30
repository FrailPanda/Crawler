def time_dict(time):
    time = convert_time(time)
    if time is None :
        return None

    dic = {}
    date_list = ["월", "화", "수", "목", "금", "토", "일"]
    dates = []

    temp = [[], [], [], [], [], [], []]

    time = time.split()

    for element in time :
        if element in date_list:
            dates.append(element)
        else :
            start_time = float(element.split('-')[0].split(':')[0]) + float(element.split('-')[0].split(':')[1])/60
            end_time = float(element.split('-')[1].split(':')[0]) + float(element.split('-')[1].split(':')[1]) / 60

            start_time = float(format(start_time, '.2f'))
            end_time = float(format(end_time, '.2f'))

            for d in dates :
                temp[date_list.index(d)].append({"start_time" : start_time, "end_time":end_time})

            dates = []

    for i in range(len(temp)) :
        if temp[i] :
            dic[str(i)] = temp[i]

    return dic


def convert_time(time):
    if time is None:
        return None

    date_list = ["월", "화", "수", "목", "금", "토", "일"]

    time = time.replace("Mon", "월")
    time = time.replace("Tue", "화")
    time = time.replace("Wed", "수")
    time = time.replace("Thu", "목")
    time = time.replace("Fri", "금")
    time = time.replace("Sat", "토")

    time = time.split()

    temp = []

    for element in time :
        if '(' in element :
            continue

        elif ')' in element:
            continue

        elif element not in date_list and ':' not in element:
            continue

        else :
            temp.append(element)

    time = ' '.join(temp)

    return time

def check_null_value(item):
    if item == '':
        return None
    else :
        return item

def translate_major(major):
    majors_ko = [
        ["기독교학과", "국어국문학과", "영어영문학과", "독어독문학과", "불어불문학과", "중어중문학과", "일어일문학과", "철학과", "사학과"],
        ["수학과", "물리학과", "화학과", "정보통계보험수리학과", "의생명시스템학부"],
        ["법학과", "국제법무학과"],
        ["사회복지학부", "행정학부", "정치외교학과", "정보사회학과", "언론홍보학과", "평생교육학과"],
        ["경제학과", "글로벌통상학과", "금융경제학과", "국제무역학과", "통상산업학과(계약학과)"],
        ["경영학부", "벤처중소기업학과", "회계학과", "벤처경영학과(계약학과)", "금융학부"],
        ["화학공학과", "유기신소재파이버공학과", "전기공학부", "기계공학부", "산업정보시스템공학과", "건축학부"],
        ["컴퓨터학부", "전자정보공학부 전자공학전공", "전자정보공학부 IT융합전공", "글로벌미디어학부", "소프트웨어학부", "스마트시스템소프트웨어학과", "미디어경영학과"],
        ["베어드교양대학 행정팀", "교직팀"],
        ["예술창작학부 문예창작전공", "예술창작학부 영화예술전공"],
        ["스포츠학부"],
        ["융합특성화자유전공학부"],
        ["학원선교팀"],
        ["산학협력진흥팀", "창업교육·지원팀"]
    ]

    majors_en = [
        ["Christian Studies", "Korean Language and Literature", "English Language & Literature",
         "German Language and Literature", "French Language and Literature", "Chinese Language and Literature",
         "Japanese Language and Literature", "Philosophy", "History"],
        ["Mathematics", "Physics", "Chemistry", "Statistics and Actuarial Science", "Systems Biomedical Science"],
        ["Law", "Global Law"],
        ["Social Welfare", "Public Administration", "Political Science and International Relations",
         "Information Sociology", "Mass Communication", "Lifelong Education"],
        ["Economics", "Global Commerce", "Financial Economics", "International Trade", "통상산업학과(계약학과)"],
        ["Business Administration", "Entrepreneurship and Small Business", "Accounting", "Venture Management",
         "Finance"],
        ["Chemical Engineering", "Organic Materials and Fiber Engineering", "Electrical Engineering",
         "Mechanical Engineering", "Industrial & Information Systems Engineering", "Architecture"],
        ["Computer Science and Engineering",
         "School of Electronic and Information Engineering, Major in Electronic Engineering",
         "School of Electronic and Information Engineering, Major in IT Convergence", "Global Media",
         "Software Engineering", "Smart System Software", "Media and Management"],
        ["Baird College", "교직팀"],
        ["Faculty of Art creation Major in Creative Writing", "Faculty of Art creation School of Film Arts"],
        ["Division of Sports"],
        ["Convergence Specialization"],
        ["학원선교팀"],
        ["산학협력진흥팀", "창업교육·지원팀"]
    ]

    for i in range(len(majors_ko)):
        for j in range(len(majors_ko[i])):
            if major == majors_ko[i][j]:
                return majors_en[i][j]

def convert_department_ko(major):
    departments = ["College of Humanities", "College of Natural Sciences", "College of Law", "College of Social Sciences",
                   "College of Economics & International Commerce", "College of Business Administration", "College of Engineering",
                   "College of Information Technology", "Baird University College", "School of Creative Arts", "School of Sports",
                   "School of Convergence Specialization", "Graduate School of Christian Studies", "Foundation of University-Industry Cooperation"]

    majors_ko = [
        ["기독교학과", "국어국문학과", "영어영문학과", "독어독문학과", "불어불문학과", "중어중문학과", "일어일문학과", "철학과", "사학과" ],
        ["수학과", "물리학과", "화학과", "정보통계보험수리학과", "의생명시스템학부"],
        ["법학과", "국제법무학과"],
        ["사회복지학부", "행정학부", "정치외교학과", "정보사회학과", "언론홍보학과", "평생교육학과"],
        ["경제학과", "글로벌통상학과", "금융경제학과", "국제무역학과", "통상산업학과(계약학과)"],
        ["경영학부", "벤처중소기업학과", "회계학과", "벤처경영학과(계약학과)", "금융학부"],
        ["화학공학과", "유기신소재파이버공학과", "전기공학부", "기계공학부", "산업정보시스템공학과", "건축학부"],
        ["컴퓨터학부", "전자정보공학부 전자공학전공", "전자정보공학부 IT융합전공", "글로벌미디어학부", "소프트웨어학부", "스마트시스템소프트웨어학과", "미디어경영학과"],
        ["베어드교양대학 행정팀", "교직팀"],
        ["예술창작학부 문예창작전공", "예술창작학부 영화예술전공"],
        ["스포츠학부"],
        ["융합특성화자유전공학부"],
        ["학원선교팀"],
        ["산학협력진흥팀", "창업교육·지원팀"]
    ]

    for i in range(len(majors_ko)):
        if major in majors_ko[i]:
            return departments[i]

def convert_department_en(major):
    departments = ["College of Humanities", "College of Natural Sciences", "College of Law", "College of Social Sciences",
                   "College of Economics & International Commerce", "College of Business Administration", "College of Engineering",
                   "College of Information Technology", "Baird University College", "School of Creative Arts", "School of Sports",
                   "School of Convergence Specialization", "Graduate School of Christian Studies", "Foundation of University-Industry Cooperation"]

    majors_en = [
        ["Christian Studies", "Korean Language and Literature", "English Language & Literature", "German Language and Literature", "French Language and Literature", "Chinese Language and Literature", "Japanese Language and Literature", "Philosophy", "History"],
        ["Mathematics", "Physics", "Chemistry", "Statistics and Actuarial Science", "Systems Biomedical Science"],
        ["Law", "Global Law"],
        ["Social Welfare", "Public Administration", "Political Science and International Relations", "Information Sociology", "Mass Communication", "Lifelong Education"],
        ["Economics", "Global Commerce", "Financial Economics", "International Trade", "통상산업학과(계약학과)"],
        ["Business Administration", "Entrepreneurship and Small Business", "Accounting", "Venture Management", "Finance"],
        ["Chemical Engineering", "Organic Materials and Fiber Engineering", "Electrical Engineering", "Mechanical Engineering", "Industrial & Information Systems Engineering", "Architecture"],
        ["Computer Science and Engineering", "School of Electronic and Information Engineering, Major in Electronic Engineering", "School of Electronic and Information Engineering, Major in IT Convergence", "Global Media", "Software Engineering", "Smart System Software", "Media and Management"],
        ["Baird College", "교직팀"],
        ["Faculty of Art creation Major in Creative Writing", "Faculty of Art creation School of Film Arts"],
        ["Division of Sports"],
        ["Convergence Specialization"],
        ["학원선교팀"],
        ["산학협력진흥팀", "창업교육·지원팀"]
    ]

    for i in range(len(majors_en)):
        if major in majors_en[i]:
            return departments[i]

def convert_year(year):
    if year == '':
        return None
    if year == '전체학년':
        return 'ALL'

    return year[:1]

def convert_location(time_str):
    if time_str == '' or time_str is None:
         return None

    result = ''

    temp = []

    for element in time_str.split():
        if '(' in element :
            temp.append(element[1:-1])

    for element in temp:
        if element.split('-')[0] != '':
            result += element.split('-')[0] + '/'

    if result[:-1] == "":
        return None
    else :
        result = result[:-1].split('/')
        result = list(set(result))
        result.sort()
        return '/'.join(result)
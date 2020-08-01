# 진행 사항
### 크롤링
1. 수강편람 한글 교과목 모든 rows 크롤링 완료 ~~(4920개)~~ (4919개, 2020.07.29 기준 사회과학대학에서 1과목 줄음)
2. 수강편람 영문 교과목 모든 rows 크롤링 완료 ~~(4962개)~~ (4961개, 2020.07.29 기준 사화과학대학에서 1과목 줄음)
3. 교과목 result 개수 맞는지 확인 완료(check_rows_count.py, check_rows_count_eng.py)
4. json 변환 중 자꾸 list index out of range ERROR가 발생해서 확인한 결과, 너무 늦게 크롤링 잘못된 부분을 발견했습니다.
    - (~2018학번) 국제캠퍼스 전공 부분에서 '유의사항'에 href 태그 없이 '※'로 표시되어 있는 부분이 있어서 코드 수정하겠습니다.
    - crawler.py line 151에서 try : result_info.append() 에서 에러
        + -> except : 에서 폐강으로 처리되지 못하여 .append() 안됨
        + -> result_info['유의사항'] 부분 누락
        + -> list index out of range Error 발생
5. korean_crawler.py, english_crawler.py -> split_into_groups.py -> csv2json.py 순으로 컴파일

### json 변환
1. 진행 중
2. ~~음...ㅋㅋㅋㅋ 시간대 formatting이 난감하네요. 이해 다 돼서 작업중이긴 합니다!(01:21 AM)~~ formatting 없이 string으로 json 변환했습니다
3. '학년'을 int형으로 하려다 예외케이스 발견 : '2,3,4' -> string으로 작업했습니다
4. ~~'단위'는 int형으로 했습니다~~ json에서 제외
    - 연세대에서는 졸업을  위해서 전공 및 타 전공을 포함해 3000단위 이상과목을 45학점 이수해야 졸업이 가능하다. 3000단위 이상이란 3,4학년을 대상으로 한 교과목을 뜻한다.
5. ~~'학점'은 string으로 했습니다.~~ float로 처리했습니다
    - float형과 int형을 둘 다 받아야 해서요!
 
### 2020-07-29 AM 3:58
개인적인 감정문제 때문에 힘이 없어서 어제는 하루종일 아무것도 하지 못했습니다.<br>
부득이하게 연락 못드린 점 죄송하다는 말씀 드립니다.<br>
금일 2시에는 꼭 사무실 방문하겠습니다.

<br><br>

# 문제점
### 크롤링
1. 한글 교과목 전체 rows : 4920, 영어 교과목 전체 rows : 4962 로 42개 과목 차이가 발생
2. 확인 결과 영문 수강편람에 'Supplementary Term' 학부가 'College of Nursing'(42개 과목)으로 잘못 중복 기입되어 있어서, 제외하고 json 변환 작업 진행
3. 'Supplementary Term'은 어차피 0개 과목이라, json 작업에서 무시하고 진행할 예정

### json
1. ~~'유의사항' 부분을 { "hyperlink" : "javascript:OpenList5("", "", "");", text : "asdf"}로 해놨는데, 포털사이트부터 쿠키가 걸려있어서 한/영 변환이 자유롭지 못합니다.~~
2. ~~포털사이트에서 쿠키값(index.jsp면 쿠키 lang=0, indexe.jsp면 쿠키 lang=1)을 통해 수강편람 open -> 이 때 쿠키값을 통해 lang 변수에 값이 들어감 -> lang 변수를 통해 모든 콘텐츠가 한글/영문으로 선택되어 보여짐  -> 유의사항도 마찬가지...~~
3. ~~이 부분은 논의해봐야 될 듯합니다.~~ 논의 완료 -> 제외하기로 결정
4. ~~'강의시간'이랑 '강의실'이 없는 경우도 있네요. 수정하겠습니다~~
    - 파이썬에서 return None으로 null값 처리했습니다.

<br><br>

# /python/~~.py 설명
1. korean_crawler.py, english_crawler.py -> split_into_groups.py -> csv2json.py 순으로 컴파일만 해도 데이터는 얻어집니다. <br>
check_~~~.py는 작업이 맞게 되었는지 체크하는 용도
2. check_json_count.py
    - 최종 결과물인 .json 파일의 모든 result 수가 맞는지 출력
3. check_rows_count.py(selenium 모듈 설치 필요)
    - 연세대 한글 수강편람 사이트에서 result 수를 크롤링하여 cnt값을 출력
4. check_rows_count_en.py(selenium 모듈 설치 필요)
    - 연세대 영문 수강편람 사이트에서 result 수를 크롤링하여 cnt값을 출력
5. csv2json.py
    - /csv/korean/group에 있는 파일들을 .json으로 변환하여 /json/korean/에 저장
6. csv2json_en.py
    - /csv/korean/group에 있는 파일들을 .json으로 변환하여 /json/korean/에 저장
    - 요일 변환하는 부분에서 csv2json.py의 코드와 살짝 다름
7. english_crawling.py
    - 설명 생략
8. korean_crawling.py
    - 설명 생략
9. split_csv_into_groups.py
    - 7, 8의 결과물을 단과대학 별로 그룹화
    - english_output.csv 처리할 때, 'Supplementary Term'는 무시했음
import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import pandas as pd
# page = 1

# url부분에서 text가져오기
url = "https://movie.naver.com/movie/bi/mi/review.naver?code=74977"
print(url)
resp = requests.get(url)
resp.text[150:500]
soup = BeautifulSoup(resp.text, 'html.parser')

# print(type(soup))


## 영화 제목
title_tag = soup.find(name='title')

title_text = title_tag.get_text()
# print(title_text)


##리뷰갯수 text
count_tag = soup.find(name='span', attrs={'class':'cnt'})

count_tag = count_tag.find(name='em')

count_text = count_tag.get_text()


##리뷰 목록
review_list_tag = soup.find(name='ul', attrs={'class':'rvw_list_area'})


review_list_tags = review_list_tag.find_all(name='li')
# 제목
review_title = review_list_tags[0].find_all('a')[0].get_text()

# 사용자 id
review_uid = review_list_tags[0].find_all('a')[1].get_text()
# print("사용자:", review_uid, "\n")

# 리뷰 내용
review_content = review_list_tags[0].find_all('a')[2].get_text()


review_nid = review_list_tags[0].find('a').get('onclick')


review_nid = re.findall('\d{7}', review_nid)[0]


# print(review_url)

title_list = []
uid_list = []
url_list = []

for li_tag in review_list_tags:
    
    review_title = li_tag.find_all('a')[0].get_text()
    title_list.append(review_title)
    
    review_uid = li_tag.find_all('a')[1].get_text()
    uid_list.append(review_uid)
    
    review_nid = re.findall('\d{7}', li_tag.find('a').get('onclick'))[0]
    review_url = f"https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={review_nid}&code=81888&order=#tab"
    url_list.append(review_url) 

# 리뷰 상세페이지의 HTML 소스코드를 가져와서 파싱(parsing)
resp_text = requests.get(url_list[0])
soup_text = BeautifulSoup(resp_text.text, 'html.parser')

# 리뷰 본문의 텍스트를 추출합니다. /  <div class="user_tx_area"> )
review_text_tag = soup_text.find(name='div', attrs={'class':'user_tx_area'})

# 텍스트 부분만 추출합니다.
review_text = review_text_tag.get_text()
# print(review_text)

headers='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
text_list = []
for url in url_list:

    # 리뷰 상세페이지의 HTML 소스코드를 가져와서 파싱(parsing)
    resp_text = requests.get(url)
    soup_text = BeautifulSoup(resp_text.text, 'html.parser')

    # 리뷰 본문의 텍스트를 추출합니다. /  <div class="user_tx_area"> )
    review_text_tag = soup_text.find(name='div', attrs={'class':'user_tx_area'})

    # 텍스트 부분만 추출합니다.
    review_text = review_text_tag.get_text()
    text_list.append(review_text)
    
    
    
# 추출된 아이템의 수량
print(len(text_list))

dict_data = {
    'title' : title_list,
    'user' : uid_list,
    'review' : text_list   
}

# 판다스 데이터프레임으로 변환

df_data = pd.DataFrame(dict_data)

# 변환 결과를 확인
df_data.to_csv("naver_review.csv")


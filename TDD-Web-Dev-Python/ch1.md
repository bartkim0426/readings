# 1부 TDD와 Django 개요 

## 1장. 기능 테스트를 이용한 Django 설치

- `TEsting Goat`: 성질 고약하고 비합리적인 스승님ㅋㅋ
- "테스트를 먼저 하라고!"
- TDD에서 가장 먼저 하는 것: "테스트를 작성해라"


### 첫 FT (Function test)

> 이전에 책 설명에 따라서 python3 세팅과 selenium / django를 설치행두어야함

- `fucntoinal_test.py`를 만들고 간단한 Functional test를 작성해보자

```
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title
```

> 맥의 경우 `WebDriverException: Message: 'geckodriver' executable needs to be in PATH.` 에러가 날수도 있음.
> 직접 PATH를 설정해주거나 `brew install geckodriver` 해주면됨


`python3 functional_test.py`로 테스트 실행시 error

```
$python3 functional_test.py
Traceback (most recent call last):
  File "common/tests/utils.py", line 6, in <module>
    assert 'Django' in browser.title
AssertionError
```

### `unittest` 활용해서 테스트

```python
from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    # test 시작전
    def setUp(self):
        self.browser = webdriver.Firefox()

    # test 시작후
    # 테스트 에러 발생되어도 tearDown 실행 (setUp에 exception 있는상황 제외하고)
    def tearDown(self):
        self.browser.quit()

    # test_ 로 시작
    def test_can_start_a_list_and_retriev_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        # 강제적으로 테스트 실패
        self.fail('Finish the test')

# 커멘드라인을 통해 실행될 경우
# unittest 실행자 가동
if __name__ == '__main__':
    unittest.main(warnings='ignore')
```

## 3장. 단위 테스트를 이용한 간단한 홈페이지 테스트

### 단위테스트 vs 기능테스트?

- 기능테스트는 사용자 관점
- 단위 테스트는 개발자 관점 (내부)

1. 기능테스트 작성 => 사용자 관점의 기능성을 정의
2. (실패시) 이를 어떻게 통과할지 개발자의 관점에서 단위테스트
3. 단위테스트를 통과할 최소한의 코드 작성
4. 동작확인


### django에서의 test

- `from django.test import TestCase 사용
- `python manage.py test`로 테스트실행 가능

- django의 프로세느는 다음과같음

1. 특정 URL에 대해 HTTP요청
2. url resolve를 통해서 어떤 뷰 함수를 실행할지 결정
3. 요청을 처리해서 HTTP 응답으로 반환

=> 두가지의 테스트가 필요

- URL이 root를 해석해서 ('/') 뷰 기능이 매칭되는지
- 홀바른 HTML을 반환해서 기능테스트 통과하는지


```python
from django.core.urlresolvers import resolve
from django.test import TestCase
from common.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
```

`python manage.py test` 실행시 당연히 `home_page`를 작성하지 않았기 때문에 `ImportError가 발생한다.`


### 한걸음씩 걸음마

실패 테스트를 해결할 최소한의 수정만

`views.py`에 다음을 추가

```
from django.shortcuts import render

home_page = None
```

아주 느리고 짜증나지만, 이런식으로 진행


유닛테스트를 완료하고 나서 `functional_test`도 테스팅. 완료되는것 확인


=> `functional_test`를 아예 따로 빼놓는 방법론이 상당히 인상적이다. 이렇게 해야 user단의 경험 확인이 가능할듯..!

=> API의 경우에는? api call 하는 상황이 user. 이경우에는 front-end에서 어떤식으로 호출하게 되는지가 더 중요할듯 싶다. 이를 function test로 짜는거구나!


## 4장. 왜 테스트를 하는 것인가?

- "이게 정말 가치가 있을까???"
- "프로그래밍은 어려운 작업이다. 종종 똑똑한 사람들이 성공하는 경우가 있다. TDD는 똑똑하지 못한 우리들을 도와주기 위해 존재한다."
- "TDD는 도르레와 같다."
- 틀을 사용 => 도움이 된다 (개구리수프가 되지 않게 막아준다)

### 리팩토링
- 기능은 바꾸지 않고 코드 자체를 개선하는 작업. 테스트 없이 리팩토링 할 수 없다
- "리팩토링 캣": 앱 코드/테스트 코드를 작은 단계로 나누어 착실하게 작업하자!




템플릿 예시

```html
<html>
  <head>
    <title>To-Do lists</title>
  </head>
  <body>
    <h1>Your To-Do List</h1>
    <input id="id_new_item" placeholder="작업 아이템 입력">
    <table id="id_list_table">
    </table>
      <tr>
        <td></td>
      </tr>
  </body>
</html>
```

## 5장. 사용자 입력 저장하기

### Form 연동
- csrf 관련해서 찾아볼것; Cross-Site Request Forgery
- 추천하는 책; `Security Engineering`(로스 앤더슨) => 번역교재 있나 찾아보기

### 리팩토링 방법: 레드/그린/리팩터 , 삼각법
- 레드/그린/리팩터? 편법이라도 테스트를 통과할 최소 코드 작성 이후 리팩토링 (애매함)
- 삼각법: 테스트가 편법코드를 허융하지 않는다면 다른 테스트를 작성 (ex. 상수같은 경우 상수를 넣지 못하게 다른 상수 테스트를 추가)
- `Three strikes and Refactor`: 중복이 세번 발생하면 리팩토링 한다! (`DIY`)
- 하나 이상의 아이템의 테스트를 처리해주기 위해 필요한게 DB

> `코드 냄새`?? 긴 단위 테스트는 테스트 자체가 복잡하다는 것이므로 테스트를 몇개로 나눌 수 있따는것
> 좋은 다누이 테스트는 각 테스트가 한가지만 테스트하는것

### 작업장
- test 를 만들때 이후 테스트나 특정 작업 (테스트 분할 작업) 등을 적어놓고 하는게 좋음
- 메모장 / todo 앱에 기록하면 좋을듯



## 6장. 최소 동작 사이트 구축

- 앞의 5장에서 발견한 functional_test의 문제 (db가 기록되는 문제)를 해결하기위해 `LiveServerTestCase` 사용


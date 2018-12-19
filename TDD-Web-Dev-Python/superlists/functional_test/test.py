from django.test import LiveServerTestCase
from contextlib import contextmanager
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of


class NewVisitorTest(LiveServerTestCase):
    # test 시작전
    def setUp(self):
        self.browser = webdriver.Firefox()

    # test 시작후
    # 테스트 에러 발생되어도 tearDown 실행 (setUp에 exception 있는상황 제외하고)
    def tearDown(self):
        self.browser.quit()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name("html")
        yield WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    # refactor: 중복되는 함수를 피하기 위한 helper 함수
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # test_ 로 시작
    def test_can_start_a_list_and_retriev_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        # item 추가하기
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )
        
        # 공작깃털 사기 입력
        inputbox.send_keys('공작깃털 사기')

        # 엔터치면 새로운 url로 변경
        # 엔터 치면 1: 공작깃털 사기 입력됨
        inputbox.send_keys(Keys.ENTER)

        with self.wait_for_page_load(timeout=10):
            edith_list_url = self.browser.current_url
            self.assertRegex(edith_list_url, 'lists/.+')
            self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 여분의 텍스트 상자에 다시 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털로 그물만들기')
        inputbox.send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('2: 공작깃털로 그물만들기')
        
        # 새로운 사용자인 프란시스
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # edith의 리스트 안보이는지 확인
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물만들기', page_text)

        # 프란시스의 아이템
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유사기')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스 전용 URL
        with self.wait_for_page_load(timeout=10):
            francis_list_url = self.browser.current_url
            self.assertRegex(francis_list_url, 'lists/.+')
            self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스 흔적 없는지 확인
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유사기', page_text)

        self.fail('Finish the test!')

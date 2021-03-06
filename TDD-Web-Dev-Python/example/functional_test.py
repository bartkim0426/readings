from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

        # 엔터 치면 1: 공작깃털 사기 입력됨
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: 공작깃털 사기' for row in rows),
        #     "신규 작업이 테이블에 표시되지 않는다"
        # )
        self.assertIn('1: 공작깃털 사기', [row.text for row in rows])

        # 여분의 텍스트 상자
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

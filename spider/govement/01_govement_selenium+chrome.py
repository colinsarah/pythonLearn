from selenium import webdriver
import time
import pymysql

class GovementSpider(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.one_url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
        # 创建数据库相关变量
        self.db = pymysql.connect(
            'localhost','root','123456','govdb',charset='utf8'
        )
        self.cursor = self.db.cursor()


    # 获取首页,并提取二级页面链接(虚假链接)
    def get_false_url(self):
        self.browser.get(self.one_url)
        # 提取二级页面链接 + 点击该节点
        td_list = self.browser.find_elements_by_xpath(
            '//td[@class="arlisttd"]/a[contains(@title,"代码")]'
        )
        if td_list:
            # 找节点对象,因为要click()
            two_url_element = td_list[0]
            # 增量爬取,取出链接和数据库version表中做比对
            two_url = two_url_element.get_attribute('href')
            sel = 'select * from version where link=%s'
            self.cursor.execute(sel,[two_url])
            result = self.cursor.fetchall()
            if result:
                print('数据已最新,无需爬取')
            else:
                # 点击
                two_url_element.click()
                time.sleep(3)
                # 切换browser
                all_handles = self.browser.window_handles
                self.browser.switch_to_window(all_handles[1])
                # 数据抓取
                self.get_data()
                # 结束之后把two_url插入到version表中
                ins = 'insert into version values(%s)'
                self.cursor.execute(ins,[two_url])
                self.db.commit()

    # 二级页面中提取行政区划代码
    def get_data(self):
        pass


if __name__ == '__main__':
    spider = GovementSpider()
    spider.get_false_url()

































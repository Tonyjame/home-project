# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import chardet
import pymysql
import time

class Boss(object):

    # 初始化
    def __init__(self):
        # self.downloader(url,id)
        pass
    # 下载器
    def downloader(self,url):

        '''
        :param url: 需要下载的地址
        :param id: 每个页面的主ID
        :return: 页面的html内容
        '''
        cookies = {
            "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a":"1572675448",
            "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a":"1572597994",
            "JSESSIONID":"",
            "__a":"89238384.1572597992.1572597992.1572598039.40.2.39.40",
            "__c":"1572598039",
            "__g":"sem",
            "__l":"r=https%3A%2F%2Fwww.zhipin.com%2Fuser%2Fsem7.html%3Fsid%3Dsem%26qudao%3Dbdpc_baidu-%25E5%258D%258E%25E5%2593%2581%25E5%258D%259A%25E7%259D%25BF02A18KA0679%26plan%3DNew-%25E5%2593%2581%25E7%2589%258C%25E8%25AF%258D%26unit%3D1-%25E5%2593%2581%25E7%2589%258C-%25E6%25A0%25B8%25E5%25BF%2583%25E8%25AF%258D%26keyword%3Dboss%25E6%258B%259B%25E8%2581%2598%26bd_vid%3D12887590226097405121&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fresume%3FjumpUrl%3D%2F&g=%2Fwww.zhipin.com%2Fuser%2Fsem7.html%3Fsid%3Dsem%26qudao%3Dbdpc_baidu-%25E5%258D%258E%25E5%2593%2581%25E5%258D%259A%25E7%259D%25BF02A18KA0679%26plan%3DNew-%25E5%2593%2581%25E7%2589%258C%25E8%25AF%258D%26unit%3D1-%25E5%2593%2581%25E7%2589%258C-%25E6%25A0%25B8%25E5%25BF%2583%25E8%25AF%258D%26keyword%3Dboss%25E6%258B%259B%25E8%2581%2598%26bd_vid%3D12887590226097405121&friend_source=0&friend_source=0",
            "__zp_stoken__":"e8dbQSYwr26pvpDAKbWpzn4tHgmsLBR3P7LscfSZaIzxH179SjY8RdJTHXJzj6Jy6%2Bp4KACkDGM7gyP0CLqDSHVu0w%3D%3D",
            "_bl_uid":"jwk9U2ItfCvws69dmoCCnLjzast8",
            "sid":"sem",
            "t":"VhRUqmW2GhxHTors",
            "toUrl":"/",
            "wt":"VhRUqmW2GhxHTors"
        }
        headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",}
        respon = requests.get(url,headers=headers,cookies=cookies)
        if respon.status_code != 200:
            print("FAILD: " + url )
            return False
        else:
            print("SUCCEED: " + url)
            return respon.text

    # 临时保存到文件中
    def save_count_to_file(self,url,id):
        html_doc = self.downloader(url,id)
        if html_doc != False:
            html_file_dir = "/Users/mac/Desktop/home_project/coding/home-project/boss/html/" + str(id) +".html"
            f = open(html_file_dir,'w')
            f.write(html_doc)
            f.close()

    # 解析器
    def parser(self,html_doc,id,type=1):

        '''
         company_id ：公司ID
         company_name : 公司名称
         area ：区域
         salary : 工资
         edu_type: 学历
         company_type : 公司行业/类型 在线教育
         company_status : 公司现状 C轮
         years : 3-5年
         company_scope : 公司规模 1000以上
         company_detail： 公司详细地址
        '''

        # 解析文档
        soup = BeautifulSoup(html_doc, 'html.parser')
        # 如果当前是概括页面
        if type == 1:
            # 设立字典类型
            job_dict = {}
            job_container = soup.find("div","job-list")
            job_list = job_container.find_all('li')
            for job in job_list:

                job_dict['company_id'] = str(id)
                print(job_dict['company_id'])
                company_desc = job.find("div","company-text")
                # 公司名称
                company_name = company_desc.find('a').get_text()
                job_dict['company_name'] = company_name
                company_detail_list = []
                for company_detail in company_desc.find('p').strings:
                    company_detail_list.append(company_detail)
                list_len = len(company_detail_list)
                if list_len == 3:
                    # 公司类型
                    company_type = company_detail_list[0]
                    job_dict['company_type'] = company_type
                    # 公司状态 以上市
                    company_status = company_detail_list[1]
                    job_dict['company_status'] = company_status
                    # 公司规模
                    company_scope = company_detail_list[2]
                    job_dict['company_scope'] = company_scope
                else:
                    # 公司类型
                    company_type = company_detail_list[0]
                    job_dict['company_type'] = company_type
                    # 公司规模
                    company_scope = company_detail_list[1]
                    job_dict['company_scope'] = company_scope
                    job_dict['company_status'] = "null"
                # 公司工资
                salary = job.find('span',"red")
                job_dict['salary'] = salary.get_text()
                company_desc_list = []
                for company_desc in job.find("div","info-primary").find("p").strings:
                    company_desc_list.append(company_desc)
                # 公司区域
                area = company_desc_list[0]
                areas = area.split(" ")
                if areas[0] == "":
                    areas[0] = "null"
                if areas[1] == "":
                    areas[1] = "null"
                if areas[2] == "":
                    areas[2] = "null"
                area_str = areas[0] + "#" + areas[1] + "#" + areas[2]
                job_dict['area'] = area_str
                # 年限 3-5年
                years = company_desc_list[1]
                job_dict['years'] = years
                # 学历
                edu_type = company_desc_list[2]
                job_dict['edu_type'] = edu_type

                # self.checkDickChardet(job_dict)
                # 发送给输出器
                self.outputer(job_dict)
                # 清空内容
                job_dict.clear()

    # 检查dick的字符编码格式
    def checkDickChardet(self,job_dict):
        for k,v in job_dict.items():
            print(k,chardet.detect(str(v).encode()))

    # 从文件读取内容
    def html_content_read_file(self,id):
        file_path =  "/Users/mac/Desktop/home_project/coding/home-project/boss/html/" + str(id) +".html"
        f = open(file_path,"r")
        return f
    # 输出器
    def outputer(self,job_dict):
        f = open(r'/Users/mac/Desktop/home_project/coding/home-project/boss/words.txt','a',encoding='utf8')
        str = job_dict['company_id'] + "," + job_dict['company_name']+ "," +job_dict['area'] + "," + job_dict['edu_type'] \
              + "," + job_dict['company_type'] + "," + job_dict['company_status'] + "," + job_dict['years'] + "," + \
            job_dict['company_scope'] + "," + job_dict['salary'] + "\n"
        f.write(str)
        f.close()

    # 输出到mysql
    def outputerMysql(self,job_dict):
        db = pymysql.connect(host="localhost",port=3306,user='root',passwd='123',db='menagerie',use_unicode=True
                             ,charset='utf8')
        cursor = db.cursor()
        sql = "insert into boss (company_id,company_name,area,salary,edu_type \
                       ,company_type,company_status,years,company_scope) \
                       values ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            str(job_dict['company_id']),str(job_dict['company_name']),str(job_dict['area']),str(job_dict['salary']),
            job_dict['edu_type'],job_dict['company_type'],job_dict['company_status'],job_dict['years'],
            job_dict['company_scope']
        )
        cursor.execute(sql)
        db.commit()
def main():
    count = 1
    url = "https://www.zhipin.com/c101010100/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88&page={}&ka=page-{}"
    while count <= 10:
        # url = url.format(count,count)
        boss = Boss()
        # 开始下载
        respon = boss.html_content_read_file("boss-" + str(count))
        # with open(r'/Users/mac/Desktop/home_project/coding/home-project/boss/html/' + str(count) + '.html','w') as f:
        #     f.write(respon)
        boss.parser(respon, "boss-" + str(count))
        count += 1
        # time.sleep(30)

if __name__ == "__main__":
    main()

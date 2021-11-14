import requests
from bs4 import BeautifulSoup
import xlwt


def spider(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
    try:
        rep = requests.get(url, headers=headers)
        rep.raise_for_status()
        rep.encoding = rep.apparent_encoding
        txt = rep.text
        return txt
    except:
        print("解析失败")


def jiexi(html, info):
    soup = BeautifulSoup(html, "lxml")
    text = soup.find_all("script", type="text/javascript")[2].string
    data = eval(str(text).split("=", 1)[1])
    for d in data:
        try:
            job_name = d["job_name"].replace("\\", "")  # 岗位名称
        except:
            job_name = " "
        try:
            company_href = d["company_href"].replace("\\", "")  # 招聘网站
        except:
            company_href = " "
        try:
            company_name = d["company_name"].replace("\\", "")  # 公司名称
        except:
            company_name = " "
        try:
            providesalary_text = d["providesalary_text"].replace("\\", "")  # 薪资
        except:
            providesalary_text = " "
        try:
            workarea_text = d["workarea_text"].replace("\\", "")  # 工作地点
        except:
            workarea_text = " "
        info.append([job_name, company_name, workarea_text, providesalary_text, company_href])


def save(data):
    print("save.....")
    workbook = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
    movieBook = workbook.add_sheet("sheet1")  # 创建工作表

    # 输入头标签
    head = ["岗位", "公司名称", "工作地点", "薪资", "招聘网站"]
    for i in range(0, len(head)):
        movieBook.write(0, i, head[i])  # 参数1是行，参数2是列，参数3是值

    # 数据逐行输入
    y = 1
    for a in data:
        print("成功保存：" + str(y))
        for x in range(0, len(a)):
            movieBook.write(y, x, a[x])
        y += 1

    workbook.save("招聘信息.xls")  # 保存数据表


if __name__ == '__main__':
    name = input("请输入岗位名称")
    page = eval(input("请输入爬取页数"))
    info = []
    for i in range(1,page+1):
        url = "https://search.51job.com/list/000000,000000,0000,00,9,99,Java%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
        html = spider(url)
        jiexi(html,info)
    save(info)

import re
import time
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
start_time = time.time()  # 开始时间
f = open('job1.csv', 'w', encoding='utf-8')
# 写入标题
list = ['职位名称', '薪资水平', '公司名称', '公司性质', '所属行业', '职能类别', '地区', '经验要求', '学历要求', '招聘人数','发布日期','职位信息','备注']
for a in list:
    f.write(a)
    f.write(',')
f.write('\n')


for i in range(1, 10):
    print("正在爬取第" + str(i) + "页数据")
    url0 = "https://search.51job.com/list/000000,000000,0000,00,9,99,Java%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,"
    url_end = ".html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare="
    url = url0 + str(i) + url_end
    res = requests.get(url=url, headers=headers)
    res.encoding = 'gbk'
    p = res.text
    ex = r'job_href\":(.*?),'  # 获取text文档后找到网址元素进行正则提取
    p1 = re.findall(ex, p)  # re.findall(匹配规则，所有内容)
    # print(res.text)
    for a in range(len(p1)):
        url = p1[a][1:-1].replace("\\", "")  # 将\\替换消失

        page = requests.get(url=url, headers=headers)
        page.encoding = 'gbk'

        tree = etree.HTML(page.text)  # 解析
        # etree.HTML()可以用来解析字符串格式的HTML文档对象，将传进去的字符串转变成_Element对象。作为_Element对象，可以方便的使用getparent()、remove()、xpath()等方法。
        #  如果想通过xpath获取html源码中的内容，就要先将html源码转换成_Element对象，然后再使用xpath()方法进行解析。
        # 获取岗位标题
        title = tree.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()')[0:1]
        if len(title) != 0:
            f.write(title[0])
        else:
            f.write('NULL')
        f.write(',')
        # 获取薪资水平
        salary = tree.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()')[0:1]
        # print(salary)
        if len(salary) != 0:
            f.write(salary[0])
        else:
            f.write('NULL')
        f.write(',')

        # 获取公司名称
        company = tree.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()')[0:1]
        if len(company) != 0:
            f.write(company[0])
        else:
            f.write('NULL')
        f.write(',')
        # 获取公司性质
        nature = tree.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/text()')[0:1]
        if len(nature) != 0:
            f.write(nature[0])
        else:
            f.write('NULL')
        f.write(',')
        # 获取所属行业
        industry = tree.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[3]/a/text()')[0:1]
        if len(industry) != 0:
            f.write(industry[0])
        else:
            f.write('NULL')
        f.write(',')
        # 获取职能类别
        category = tree.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/div[1]/p[1]/a/text()')[0:1]
        # print(category)
        if len(category) != 0:
            f.write(category[0])
        else:
            f.write('NULL')
        f.write(',')
        # 获取工作地区
        pos = tree.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title')
        # print(pos)
        for a in pos:
            if a is not None:
                # 获取位置
                position = a.split(r'|')[0].replace(u'\xa0', u'')  # 字符串前加u，防止中文乱码
                f.write(position)
                f.write(',')
                # 获取所需经验
                year = a.split(r'|')[1].replace(u'\xa0', u'')
                f.write(year)
                f.write(',')
                # 获取学历要求
                degree = a.split(r'|')[2].replace(u'\xa0', u'')
                f.write(degree)
                f.write(',')
                # 获取招聘人数
                people = a.split(r'|')[-2].replace(u'\xa0', u'')
                f.write(people)
                f.write(',')
                # 获取发布日期
                day = a.split(r'|')[-1].replace(u'\xa0', u'')
                f.write(day)
                f.write(',')


        # 获取岗位描述与任职要求
        lst1 = tree.xpath('//div[@class="bmsg job_msg inbox"]//text()')
        a = []
        for i in lst1:
            de1 = i.replace(u'\xa0', u"")
            if len(de1) != 0:
                a.append(de1)

        work = "".join(a).replace(" ", "").replace(u"\r\n", "，").replace(",", "，")  # 去掉空白、换行和英文逗号
        f.write(work)
        f.write(',')
        if len(pos) != 0:
            f.write(pos[0])
        else:
            f.write('NULL')
        f.write('\n')
    time.sleep(0.5)
f.close()
end_time = time.time()
print("爬取完毕！爬取时长%s秒" % (end_time - start_time))

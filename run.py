from login import login
from scrapy import scrapy
import logging,time,random
from excelread import excelread
from datetime import datetime
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
mdb = conn.maban

def pullDate():
    loginObj = login()
    result = loginObj.saveCookie()

    if not result:
        #app.logger.error('登录失败')
        return '登录失败'

    cookies = loginObj.getCookie()
    if not cookies:
        #app.logger.error('获取登录信息失败')
        return '获取登录信息失败'

    scrapyObj = scrapy(cookies)

    page = 1
    #找出已存在的所有表格
    #批次
    batch = int(time.time())

    while True:

        allList = scrapyObj.getStockAllList(page)

        if not allList.get('success'):
            #app.logger.error('拉取sku列表失败,无法获取AllList, 原因: {}'.format(allList.get('message')))
            print(cookies)

            return '拉取sku列表失败,无法获取AllList, 原因: {}'.format(allList.get('message'))

        pageAll = allList['page']

        skuList = allList['hasPlatformOrderId']

        ############################下载表格###########################

        excels = scrapyObj.doStockExportFile(skuList)

        if not excels['success']:
            #app.logger.error(excels['message'])
            return 'error'

        #处理excel表格

        if not mdb.excels.find({'path':excels.get('gourl')}).count():
            mdb.excels.insert({'path':excels['gourl'],'page':page,'createtime':str(datetime.now()),'status':0,'batch':batch})
        else:
            print('已存在')

        print(excels['gourl'])

        time.sleep(random.randint(1, 3))



        if page == pageAll:
            break
        page += 1

    return excels['gourl']

if __name__ == '__main__':

    starttime = time.time()
    if mdb.excels.find({'status':0}).count() > 0:

        excel = excelread()

        excel.read_excel()

    else:

        pullDate()

    endtime = time.time()
    print('token time : {}'.format(endtime - starttime))
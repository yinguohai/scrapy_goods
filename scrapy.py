from flask import Flask
import config,requests,json,time

class scrapy:
    def __init__(self , cookies):
        self.urls = config.urls
        self.headers = config.common_headers
        self.fields = config.fields
        self.cookies = cookies

    def getStockAllList(self,page):
        url = self.urls['getStockAllList']

        if not isinstance(page , int):
            return {'success':False,'message':'拉取失败'}

        for num in range(1,6):
            try:
                response = requests.post(url,data={'page':page},headers=self.headers,cookies=self.cookies)
                break
            except requests.exceptions.ConnectionError as e:
                if num >= 5:
                    print('已经尝试连接5次了，依然被拒')
                    break
                time.sleep(random.randint(1,5))
        if response.ok:
            return json.loads(response.text)
        else:
            return {'success':False,'message':'拉取失败'}

    def doStockExportFile(self,skuList):
        url = self.urls['doStockExportFile']
        if not skuList or not isinstance(skuList,list):
            return {'success':False,'message':'skuList  错误'}
        fileds = self.fields
        memcacheKey = self.cookies.get('MABANG_ERP_PRO_MEMBERINFO_LOGIN_COOKIE')
        fileds['memcacheKey'] = memcacheKey
        fileds['orderIds'] = '\n'.join(skuList)

        for num in range(1,6):
            try:
                response = requests.post(url,data=fileds,headers=self.headers,cookies=self.cookies)
                if response.ok:
                    return json.loads(response.text)
                else:
                    return {'success': False, 'message': '表格下载失败', 'sku': json.dumps(skuList)}
            except requests.exceptions.ConnectionError as e:
                if num >= 5:
                    print('已经尝试连接5次了，依然被拒')
                    break
                #休息时间
                time.sleep(random.randint(1, 5))
            except Exception as e:
                return {'success':False,'message':'表格下载失败,原因： {}'.format(str(e)),'sku':json.dumps(skuList)}


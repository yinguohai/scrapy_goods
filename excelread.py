from pymongo import MongoClient
from datetime import datetime
import requests,os,config,common,json
from dbdriver import DBdriver
from pymongo import MongoClient
import xlrd

class excelread:
    def __init__(self):
        conn = MongoClient('localhost', 27017)
        self.mdb = conn.maban

    def download_excel(self,url):
        nowdate = datetime.now().strftime('%Y%m%d')
        excel_file_dir = os.path.join(os.path.abspath('.'), 'excels', nowdate)

        if not os.path.isdir(excel_file_dir):
            os.mkdir(excel_file_dir)

        excel_file = requests.get(url, stream=True)

        file_path = os.path.join(excel_file_dir, os.path.basename(url))

        with open(file_path,'wb') as f:
            try:
                for chunk in excel_file.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            except Exception as e:
                return {'status':False,'msg':str(e)}

        if os.path.isfile(file_path):
            return {'status':True,'msg':'success','file_path':file_path}
        else:
            return {'status':False,'msg':'上传失败'}

    def read_excel(self):

        excel_data = self.mdb.excels.find({'status':0})
        ii = 0
        for excel in excel_data:
            ii = ii+1
            excel_file = requests.get(excel['path'],stream=True)
            download = self.download_excel(excel['path'])

            if download['status']:

                workbook = xlrd.open_workbook(download['file_path'])

                table = workbook.sheet_by_index(0)

                fileds = []

                for k,v in enumerate(table.row_values(0)):
                    if v in config.field_map:
                        fileds.append(config.field_map.get(v))

                for index in range(1,table.nrows):
                    print('*'*20,ii,'#',index)

                    new_row = table.row_values(index)

                    if common.empty(new_row):
                       break
                    else:
                        new_data = dict(zip(fileds,new_row))
                        #初始化状态
                        new_data['update_status']=0
                        self.saveData(new_data,excel)

                    del new_data,new_row

                #消费过后变状态
                self.mdb.excels.update({'_id':excel.get('_id')},{'$set':{'status':1}})

            else:

                print(download['msg'])
                pass


    def saveData(self,data,excel):
        db = DBdriver()

        is_exists = db.select(data.get('sku'))

        if not is_exists:
            result = db.insert(data)
        else:
            result = db.update({'sku':data.get('sku')},data)

        if not result.get('status'):
            print(result['msg'])
            self.mdb.excelserr.insert(
                { 'createtime': str(datetime.now()), 'status': 1,'batch':excel['batch'],'url':excel['path'],'page':excel['path'],'msg':result['msg'],'data':json.dumps(data)}
            )
        else:
            #success
            print(result)


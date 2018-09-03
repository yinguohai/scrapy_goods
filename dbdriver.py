import pymysql,config,time
import config as C
from datetime import datetime

class DBdriver:
    dbconn = None
    def __init__(self):
        self.host=C.db ['DB_HOST']
        self.user=C.db['DB_USER']
        self.port=C.db['DB_PORT']
        self.pwd=C.db['DB_PWD']
        self.dbname=C.db['DB_NAME']
        dbconn=self.conn()
        print(dbconn)

    def conn(self):
        try:
            if not DBdriver.dbconn:

                DBdriver.dbconn = pymysql.connect(
                    host = self.host,
                    port = self.port,
                    user = self.user,
                    passwd = self.pwd,
                    db = self.dbname
                )
        except Exception as e:
            print(e)

            return False

        return DBdriver.dbconn
    @staticmethod
    def closedb(self):
        if not DBdriver.dbconn:
            print('关闭数据库')
            DBdriver.dbconn.close()

    def select(self,sku,table='de_product_mb'):

        conn = DBdriver.dbconn if DBdriver.dbconn else self.conn()

        if not conn:

            return {'status':False,'msg':'获取连接失败'}

        cursor = conn.cursor()

        sql = 'select `sku`,`status` from {1} where `sku` ="{0}"'.format(sku,table)

        try:
            cursor.execute(sql)
            result = cursor.fetchone()
        except TypeError as e:
            return {'status':False,'msg':str(e)}
        except pymysql.err.Error as e:
            return {'status': False, 'msg': str(e)}


        if result:
            result = dict(zip(['sku', 'status'], result))
            result['status']=True
        return result

    def update(self,where,data,table='de_product_mb'):
        conn = DBdriver.dbconn if DBdriver.dbconn else self.conn()

        while not conn:
            time.sleep(2)
            conn = DBdriver.dbconn if DBdriver.dbconn else self.conn()

        data['uptime'] = datetime.now().strftime('%Y-%m-%d %H:%I')
        cursor = conn.cursor()

        try:

            #组合条件
            wheresql = []
            if isinstance(where,dict):
                for w in where.items():
                    wheresql.append('{0} = "{1}"'.format(w[0],w[1]))

            wherestr =  '' if not wheresql else ' and '.join(wheresql)

            #组合需要更新的字段
            if isinstance(data,dict):

                setsql = []

                for t in data.items():
                    setsql.append('{0} = "{1}"'.format(t[0],t[1]))

                if not setsql:
                    return {'status':False,'msg':'没有要更新的字段'}

                setstr = '' if not setsql else ' , '.join(setsql)

            #拼接SQL
            sql = 'update {0} set {1} where {2}'.format(table,setstr,wherestr)

            result = cursor.execute(sql)
            conn.commit()
        except TypeError as e:
            return {'status':False,'msg':str(e)}
        except pymysql.err.ProgrammingError as e:
            return {'status': False, 'msg': str(e)}
        except pymysql.err.Error as e:
            return {'status': False, 'msg': str(e)}


        if result == 1:
            print('更新成功 {}'.format(data['sku']))
            return {'status':True,'msg':'success'}
        else:
            return {'status':True,'msg':'无序更新'}


    def insert(self,data,table='de_product_mb'):
        conn = DBdriver.dbconn if DBdriver.dbconn else self.conn()

        while not conn:
            time.sleep(2)
            conn = DBdriver.dbconn if DBdriver.dbconn else self.conn()

        data['uptime'] = datetime.now().strftime('%Y-%m-%d %H:%I')

        if not conn:
            return False

        cursor = conn.cursor()

        try:
            if isinstance(data,dict):
                keys = []
                values = []
                for t in data.items():
                    keys.append('`'+str(t[0])+'` ')
                    values.append('"'+str(t[1])+'"')

                sql = 'insert into {0}({1}) values({2})'.format(table,','.join(keys),','.join(values))

            cursor.execute(sql)
            conn.commit()
        except pymysql.err.IntegrityError as e:
            return {'status': False, 'msg': '数据插入失败 : {}'.format(str(e))}
        except pymysql.err.ProgrammingError as e:
            return {'status': False, 'msg': '数据插入失败:{}'.format(str(e))}
        except pymysql.err.Error as e:
            return {'status': False, 'msg': '数据插入失败:{}'.format(str(e))}

        print('插入成功 {}'.format(data['sku']))
        return {'status':True,'msg':'insert Successd'}
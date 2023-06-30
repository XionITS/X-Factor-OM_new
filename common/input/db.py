import math
import psycopg2
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DataLoadingType = SETTING['MODULE']['DataLoadingType']
DBHost = SETTING['DB']['DBHost']
DBPort = SETTING['DB']['DBPort']
DBName = SETTING['DB']['DBName']
DBUser = SETTING['DB']['DBUser']
DBPwd = SETTING['DB']['DBPwd']
AssetTNM = SETTING['DB']['AssetTNM']
StatisticsTNM = SETTING['DB']['StatisticsTNM']
BS = SETTING['FILE']
DBSettingTime = SETTING['DB']['DBSelectTime']
day = datetime.today().strftime("%Y-%m-%d")
RSU = SETTING['FILE']['RunningService_Except']['USE']


def plug_in(type, threeData=None):
    try:
        FiveMinuteAgo = (datetime.today() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        DBSelectTime = (datetime.today() - timedelta(minutes=DBSettingTime)).strftime("%Y-%m-%d %H:%M:%S")
        halfHourAgo = (datetime.today() - timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S")
        yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
        fiveDay = (datetime.today() - timedelta(5)).strftime("%Y-%m-%d")
        weekDay = (datetime.today() - timedelta(7)).strftime("%Y-%m-%d")
        # monthDay = (datetime.today() - timedelta(30)).strftime("%Y-%m-%d")
        monthDay = (datetime.today() - relativedelta(days=31)).strftime("%Y-%m-%d")

        SDL = []
        Conn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()

        # ------------------------------상단 디스크 사용률 도넛 차트------------------------
        if type == 'disk_donutData':
            query = """
                        select 
                            item_count
                        from
                            minutely_statistics
                        where 
                            item = 'Disk Used Percentage#3'
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                    """
        # -----------------------------상단 메모리 사용률 도넛 차트------------------------------
        elif type == 'memory_donutData':
            query = """
                        select 
                            item_count
                        from
                            minutely_statistics
                        where 
                            item = 'Memory Consumption#2'
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        """
        # -----------------------------상단 씨피유 사용률 도넛 차트------------------------------
        elif type == 'cpu_donutData':
            query = """
                        select 
                            item_count
                        from
                            minutely_statistics
                        where 
                            item = 'CPU Consumption#2'
                            and statistics_collection_date >= '""" + DBSelectTime + """'
            """
        # -----------------------------상단 오에스 파이차트 ------------------------------------
        elif type == 'os_pieData':
            query = """
                        select 
                            item, item_count
                        from
                            minutely_statistics
                        where 
                            classification = 'dashboard_OS Platform'
                            AND item != 'unconfirmed'
                            and NOT item IN ('unconfirmed')
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        order by item_count desc
                    """
        # -----------------------------상단 유/무선(와이어) 파이차트 ------------------------------------
        elif type == 'wire_pieData':
            query = """
                        select 
                            item, item_count
                        from
                            minutely_statistics
                        where 
                            classification = 'dashboard_wired/wireless 2'
                            AND item != 'unconfirmed'
                            and NOT item IN ('unconfirmed')
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        order by item_count desc
                    """
        # -----------------------------상단 물리/가상 파이차트 ------------------------------------
        elif type == 'virtual_pieData':
            query = """
                        select 
                            item, item_count
                        from
                            minutely_statistics
                        where 
                            classification = 'dashboard_Is Virtual#3'
                            AND item != 'unconfirmed'
                            and NOT item IN ('unconfirmed')
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        order by item_count desc
                    """
        # -----------------------------중앙 관리자산 라인차트 ------------------------------------
        elif type == 'allAsset_lineData':
            query = """
                SELECT 
                    TO_CHAR(statistics_collection_date, 'YYYY-MM-DD'),
                    CAST(SUM(CAST(item_count as INTEGER)) as VARCHAR)
                FROM
                    daily_statistics
                WHERE 
                    classification = 'dashboard_OS Platform'
                    AND statistics_collection_date >= '""" + weekDay + """'
                GROUP BY statistics_collection_date
                ORDER BY statistics_collection_date ASC
                    """
        # -----------------------------중앙 미관리자산 라인차트 ------------------------------------
        elif type == 'discover_lineData':
            query = """
                        select 
                            TO_CHAR(statistics_collection_date, 'YYYY-MM-DD'), item_count
                        from
                            daily_statistics
                        where 
                            item = 'unmanagement'
                            and statistics_collection_date >= '""" + weekDay + """'
                        order by statistics_collection_date asc
                    """
        #-----------------------------예상 유휴자산 라인차트 ------------------------------------
        elif type == 'idle_lineData':
            query = """
                        select 
                            TO_CHAR(statistics_collection_date, 'YYYY-MM-DD') ,item_count
                        from
                            daily_statistics
                        where 
                            item = 'collection_date'
                            and statistics_collection_date >= '""" + weekDay + """'
                        order by statistics_collection_date asc
                    """
        # -----------------------------인증서리스트 ------------------------------------
        # elif type == 'cert_listData':
        #     query = """
        #                 select
        #                     crt_name, crt_expire_date, count(computer_name) as item_count
        #                 from
        #                     certificate_asset
        #                 where
        #                     crt_name != 'Root'
        #                 AND
        #                     collection_date >= '""" + yesterday + """'
        #                 group by crt_name, crt_expire_date
        #                 order by
        #                     crt_expire_date ASC, item_count ASC
        #                 LIMIT 7
        #             """
        #--------------인증서 리스트 날짜 지난거 안보이게
        elif type == 'cert_listData':
            query = """
                        SELECT
                            crt_name, crt_expire_date, COUNT(computer_name) AS item_count
                        FROM
                            certificate_asset
                        WHERE
                            crt_name != 'Root'
                            AND TO_DATE(crt_expire_date, 'MM/DD/YYYY HH24') >= DATE '""" + yesterday + """'
                            AND collection_date >= '""" + yesterday + """'
                        GROUP BY crt_name, crt_expire_date
                        ORDER BY TO_DATE(crt_expire_date, 'MM/DD/YYYY HH24') ASC
                        LIMIT 7
                    """
        # -----------------------------인증서리스트 더보기 및 카운트----------------------------
        elif type == 'cert_listDataMore':
            query = """
                        select 
                            computer_name, os, ip, crt_name, crt_expire_date
                        from 
                            certificate_asset 
                        where 
                            crt_name != 'Root'
                        and
                            crt_name = '""" + threeData[3] + """'
                        AND
                            collection_date >= '""" + yesterday + """'    
                        and
                            (computer_name ILIKE '%""" + threeData[2] + """%' or
                            os ILIKE '%""" + threeData[2] + """%' or
                            ip ILIKE '%""" + threeData[2] + """%' or
                            crt_name ILIKE '%""" + threeData[2] + """%' or
                            crt_expire_date ILIKE '%""" + threeData[2] + """%')
                        GROUP BY 
                            crt_name, crt_expire_date, computer_name, os, ip
                        order by 
                            crt_expire_date asc
                        LIMIT """ + threeData[0] + """
                        OFFSET (""" + threeData[1] + """-1) * """ + threeData[0] + """
                    """

        elif type == 'cert_listDataMoreCount':
            query = """
                        select
                            COUNT(*)
                        from 
                            certificate_asset 
                        where 
                            crt_name != 'Root' 
                        and
                            crt_name = '""" + threeData[3] + """'
                        and
                            (crt_name ILIKE '%""" + threeData[2] + """%' or
                            crt_expire_date ILIKE '%""" + threeData[2] + """%' or
                            computer_name ILIKE '%""" + threeData[2] + """%' or
                            os ILIKE '%""" + threeData[2] + """%' or
                            ip ILIKE '%""" + threeData[2] + """%') 
                        and    
                            collection_date >= '""" + yesterday + """'  
                    """

        Cur.execute(query)
        RS = Cur.fetchall()
        for R in RS:
            if type == 'disk_donutData' or type == 'memory_donutData' or type == 'cpu_donutData':
                SDL.append(
                    (
                        ('count', int(R[0]))
                    )
                )
            elif type in ['os_pieData', 'wire_pieData', 'virtual_pieData', 'discover_lineData', 'idle_lineData', 'allAsset_lineData']:
                SDL.append(dict(
                    (
                        ('item', R[0]),
                        ('count', int(R[1]))
                    )
                ))
            elif type == 'cert_listData':
                SDL.append(dict(
                    (
                        ('name', R[0]),
                        ('date', R[1]),
                        ('count', R[2])
                    )
                ))
            elif type == 'cert_listDataMore':
                SDL.append(dict(
                    (
                        ('computer_name', R[0]),
                        ('os', R[1]),
                        ('ip', R[2]),
                        ('crt_name', R[3]),
                        ('crt_expire_date', R[4]),
                    )
                ))
            else:
                SDL.append(R)
        return SDL
    except Exception as e:
        print(str(type) +'Statistics Table connection(Select) Failure _'+ str(e))

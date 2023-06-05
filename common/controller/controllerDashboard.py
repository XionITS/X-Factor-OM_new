import requests
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from common.Input.DB.Tanium.Postgresql.Dashboard import plug_in as PDPI
# from web.model.dashboard_function import DashboardData
# from web.model.dashboard_function import MainData
# from web.model.dashboard_function import AssetData
from django.views.decorators.csrf import csrf_exempt
from common.controller.controllerCommon import MenuSetting
from common.dashboardFunction import Dashboard
import json
from pprint import pprint



menuListDB = MenuSetting()

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
Customer = SETTING['PROJECT']['CUSTOMER']
WorldUse = SETTING['PROJECT']['MAP']['World']
KoreaUse = SETTING['PROJECT']['MAP']['Korea']
AreaUse = SETTING['PROJECT']['MAP']['Area']['use']
AreaType = SETTING['PROJECT']['MAP']['Area']['type']
Login_Method = SETTING['PROJECT']['LOGIN']

def dashboard(request):
    DCDL = Dashboard()
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        disk_donutData = DCDL["disk_donutData"]
        memory_donutData = DCDL["memory_donutData"]
        cpu_donutData = DCDL["cpu_donutData"]
        wire_pieData = DCDL["wire_pieData"]
        os_pieData = DCDL["os_pieData"]
        virtual_pieData = DCDL["virtual_pieData"]
        discover_lineData = DCDL["discover_lineData"]
        cert_listData = DCDL["cert_listData"]
        sbom_listData = DCDL["sbom_listData"]
        report_listData = DCDL["report_listData"]
        idle_lineData = DCDL["idle_lineData"]

        dataList = {'disk_donutData': disk_donutData,
                    'memory_donutData': memory_donutData,
                    'cpu_donutData': cpu_donutData,
                    'wire_pieData': wire_pieData,
                    "os_pieData": os_pieData,
                    "virtual_pieData": virtual_pieData,
                    "discover_lineData": discover_lineData,
                    "cert_listData": cert_listData,
                    "sbom_listData": sbom_listData,
                    "report_listData": report_listData,
                    "idle_lineData": idle_lineData
                     }
        returnData = {'menuList': menuListDB, 'dataList': dataList, 'Login_Method': Login_Method, 'Customer' : Customer}
        #print(returnData)
        return render(request, 'common/dashboard.html', returnData)
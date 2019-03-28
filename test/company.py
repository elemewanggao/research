#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    1:获取所有公司的id, chinese_name, website(官网地址), headquarters(总部地址)
    2:获取excel里面的 中文名，官网地址，总部地址
    3:根据1中的chinese_name找到2中的中文名，用2中的官网地址，总部地址刷新数据库中数据
"""
import sys
from research.model import get_session
from research.utils.exceler import ExcelReader

reload(sys)
sys.setdefaultencoding('utf-8')
session = get_session('up_prd')
company_file_path = '/Users/wanggao/Desktop/final.xlsx'
company_collect_path = '/Users/wanggao/Desktop/info.xlsx'


def get_company_in_database():
    companys = session.execute("select id, chinese_name from company_company").fetchall()
    return {
        company.id: company.chinese_name for company in companys}


def get_company_in_excel():
    excel = ExcelReader(company_file_path)
    companys = excel.read_sheet(0)
    return {
        company[2]: (company[4], company[5]) for company in companys
    }


def update_company_website_headquarter():
    """更新公司官网url和总部地址."""
    companys = get_company_in_database()
    company_infos = get_company_in_excel()
    for company_id, company_name in companys.iteritems():
        if company_infos.get(company_name):
            website = company_infos[company_name][0]
            if not website.startswith('http') and not website:
                website = 'http://' + website
            headquarters = company_infos[company_name][1]
            session.execute("update company_company set website='{}', headquarters = '{}' where id = {}".format(
                website, headquarters, company_id))
    session.commit()


def get_company_collect_in_excel():
    excel = ExcelReader(company_collect_path)
    companys = excel.read_sheet(0)
    return {
        company[0]: (company[1], company[2], company[3], company[4], company[5], company[6], company[7], company[8]) for company in companys
    }


def update_company_collect_info():
    """更新公司官网收集的信息."""
    companys = get_company_in_database()
    company_infos = get_company_collect_in_excel()
    for company_id, company_name in companys.iteritems():
        if company_infos.get(company_name):
            critical = company_infos[company_name][0]
            drop = 1 if company_infos[company_name][1] ==  '是' else 0
            salary = company_infos[company_name][2]
            boon = company_infos[company_name][3]
            work_rank = company_infos[company_name][4]
            grownup = company_infos[company_name][5]
            applylevel = company_infos[company_name][6]
            business_culture = company_infos[company_name][7]
            business_culture = business_culture.replace('\n', '<br>')
            session.execute("update company_company set critical='{}', drop_down = {}, salary = '{}', boon = '{}', work_rank = '{}', grownup = '{}', applylevel = '{}', business_culture = '{}' where id = {}".format(
                critical, drop, salary, boon, work_rank, grownup, applylevel, business_culture, company_id))
    session.commit()


if __name__ == '__main__':
    update_company_collect_info()
    # update_company_website_headquarter()

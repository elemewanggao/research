# -*- coding:utf-8 -*-
"""
xlrd用于Excel的读操作，可以支持xls,xlsx
xlwt用于Excel的写操作，只支持xls
"""
import os
import xlrd


class ExcelReader(object):
    u"""Excel读."""

    def __open_excel_by_file(self, path):
        u"""根据Excel文件路径打开."""
        with xlrd.open_workbook(path) as workbook:
            return workbook

    def __open_excel_by_contents(self, contents):
        u"""根据Excel文件内容打开."""
        with xlrd.open_workbook(file_contents=contents) as workbook:
            return workbook

    def __get_sheet(self, sheet):
        u"""获取sheet页."""
        if isinstance(sheet, int):
            sheet = self.workbook.sheet_by_index(sheet)
        else:
            sheet = self.workbook.sheet_by_name(sheet)
        return sheet

    def __init__(self, path=None, contents=None):
        u"""Excel读初始化."""
        if not path and not contents:
            raise Exception('at least have one para!')
        if path:
            if not os.path.exists(path):
                raise Exception('file path does not exist!')

            self.workbook = self.__open_excel_by_file(path)
        else:
            self.workbook = self.__open_excel_by_contents(contents)

    def sheets(self):
        u"""获取Excel页的sheet页名称."""
        sheets_name = []
        sheets_num = self.workbook.nsheets
        for i in xrange(sheets_num):
            sheets_name.append((self.workbook.sheet_by_index(i).name).strip())
        return sheets_name

    def nrows(self, sheet):
        u"""获取Excel的sheet页的行数."""
        sheet = self.__get_sheet(sheet)
        return sheet.nrows

    def ncols(self, sheet):
        u"""获取Excel某sheet页的列数."""
        sheet = self.__get_sheet(sheet)
        return sheet.ncols

    def __convert_cell_value(self, value):
        u"""Excel中对于数字读出来为float类型,123->123.0,将本来是int的数字按int形返回."""
        float_to_int = lambda x: int(x) if isinstance(x, float) and x == int(x) else x
        return float_to_int(value)

    def read_sheet(self, sheet, mode=0):
        u"""读取sheet页数据.

        sheet:可以是数字，表示第几个sheet页，数字的时候从0开始;或是sheet页的名称
        mode:读取excel的方式 0:按行读  非0:按列读 默认行读
        """
        nrows = self.nrows(sheet)
        ncols = self.ncols(sheet)
        data = []
        sheet = self.__get_sheet(sheet)

        if not mode:
            for i in xrange(nrows):
                row_data = tuple([
                    self.__convert_cell_value(value) for value in sheet.row_values(i)])
                data.append(row_data)
        else:
            for j in xrange(ncols):
                col_data = tuple([
                    self.__convert_cell_value(value) for value in sheet.col_values(j)])
                data.append(col_data)
        return data

    def read_sheet_by_row_col(self, sheet, row, col):
        u"""获取sheet里面的某个单元格内容."""
        data = self.read_sheet(sheet)
        nrows = self.nrows(sheet)
        ncols = self.ncols(sheet)
        if row >= nrows or col >= ncols:
            return ''
        return str(self.__convert_cell_value(data[row][col])).strip()

    def read(self, mode=0):
        u"""读整个Excel.

        mode:读取excel的方式 0:按行读  非0:按列读 默认行读
        """
        result_data = []
        sheets_num = self.workbook.nsheets
        for i in xrange(sheets_num):
            sheet_name = self.workbook.sheet_by_index(i).name
            result_data.append({'sheet_name': sheet_name, 'data': self.read_sheet(i, mode)})
        return result_data

from openpyxl import Workbook
import os

def create_worksheet(worksheet_name):
    wb = Workbook()
    ws = wb.create_sheet(worksheet_name)
    return wb, ws


def save_excel_file(workbook, folder_path, file_name):
    excel_file_name = str(folder_path) + '/' + file_name + '.xlsx'

    if os.path.exists(str(folder_path) + '/~$' + file_name + '.xlsx'):
        return 6
    workbook.save(excel_file_name)
    return excel_file_name


def worksheet_write(worksheet, col_num, *args, **kwargs):
    start_row = 'A'
    if kwargs:
        start_row = kwargs['start_row']

    for num, arg in enumerate(args):
        worksheet[f'{chr(ord(start_row) + num)}{col_num}'] = arg

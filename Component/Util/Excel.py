from openpyxl import Workbook


def worksheet_write(worksheet, col_num, *args, **kwargs):
    start_row = 'A'
    if kwargs:
        start_row = kwargs['start_row']

    for num, arg in enumerate(args):
        worksheet[f'{chr(ord(start_row) + num)}{col_num}'] = arg


def create_worksheet(worksheet_name):
    wb = Workbook()
    ws = wb.create_sheet(worksheet_name)
    return wb, ws


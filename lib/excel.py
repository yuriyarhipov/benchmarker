from openpyxl import load_workbook

class Excel(object):
    filename = None

    def __init__(self, filename):
        self.filename = filename

    def get_data(self):
        data =[]

        wb = load_workbook(filename=self.filename, use_iterators=True)
        ws = wb.active

        for excel_row in ws.iter_rows():
            row = []
            for cell in excel_row:
                if cell.value:
                    row.append(cell.value)
                else:
                    row.append('')
            data.append(row)
        return data

    def get_competitors_template(self):
        return self.get_data()[1:]

    def get_data_set(self):
        return self.get_data()









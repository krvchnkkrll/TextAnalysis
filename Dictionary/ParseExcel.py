import os
import openpyxl


class ParseExcelWrapper:
    def __init__(self):
        self.data = []
        self.folder_path = "../Wordsdata"

    def parse_excel_data(self):
        data_files = os.listdir(self.folder_path)
        for file in data_files:
            workbook = openpyxl.load_workbook(f"Wordsdata/{file}")
            sheet = workbook.active

            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    self.data.append(cell)

        return self.data

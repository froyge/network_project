from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

path = Path('output') / 'Модель_избыточной_реакции_исправленная.xlsx'
wb = load_workbook(path)
if 'Базовые срезы статьи' in wb.sheetnames:
    del wb['Базовые срезы статьи']
ws = wb.create_sheet('Базовые срезы статьи')

NAVY = '17365D'; BLUE = '1F4E78'; PALE = 'EEF5FB'; WHITE = 'FFFFFF'; YELLOW = 'FFF2CC'
THIN = Side(style='thin', color='B7C9D6')
ws.merge_cells('A1:F1')
ws['A1'] = 'Базовые отраслевые срезы из статьи - используются как benchmark'
ws['A1'].fill = PatternFill('solid', fgColor=NAVY)
ws['A1'].font = Font(bold=True, size=15, color=WHITE)
ws['A1'].alignment = Alignment(vertical='center')
ws.row_dimensions[1].height = 28
headers = ['Отрасль','Всего наблюдений','Валидная модель Гордона','Стандартное отклонение','Среднее отклонение','Статус применимости']
for j,h in enumerate(headers,1):
    c=ws.cell(3,j,h); c.fill=PatternFill('solid',fgColor=BLUE); c.font=Font(bold=True,color=WHITE); c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True); c.border=Border(left=THIN,right=THIN,top=THIN,bottom=THIN)
rows = [
    ['Электроэнергетика',120,56,0.5140,0.1210,'основной отраслевой ориентир'],
    ['Нефтегазовая отрасль',89,20,0.5049,-0.1150,'основной отраслевой ориентир'],
    ['Банки',49,13,0.5177,0.2098,'использовать с осторожностью'],
    ['Связь и телекоммуникация',17,13,0.1664,-0.4096,'использовать с осторожностью'],
    ['Трубопроводный транспорт',8,7,0.6455,-0.0421,'предварительный ориентир'],
    ['Холдинги',24,5,0.1965,-0.4003,'предварительный ориентир'],
    ['Черная металлургия',15,5,0.1678,1.3579,'предварительный ориентир'],
    ['Строительство зданий',8,4,0.1058,0.5186,'не использовать как самостоятельный норматив'],
    ['Производство лекарств и биотехнологии',5,4,0.1103,-0.5065,'не использовать как самостоятельный норматив'],
    ['Недвижимость и фонды недвижимости',4,4,0.7477,-0.2056,'не использовать как самостоятельный норматив'],
    ['Воздушный транспорт',4,4,0.0431,0.2385,'не использовать как самостоятельный норматив'],
    ['Производство продуктов и напитков',33,1,0.0,-0.2724,'единичное наблюдение'],
    ['Добыча драгоценных металлов',16,1,0.0,-0.2184,'единичное наблюдение'],
    ['Прочее машиностроение и приборостроение',8,1,0.0,-0.0197,'единичное наблюдение'],
    ['Итого по валидной подвыборке',470,138,0.5632,0.0415,'benchmark общей выборки'],
]
for i,row in enumerate(rows,4):
    for j,v in enumerate(row,1):
        c=ws.cell(i,j,v); c.border=Border(left=THIN,right=THIN,top=THIN,bottom=THIN); c.alignment=Alignment(vertical='center',wrap_text=True)
        if j==1: c.fill=PatternFill('solid',fgColor=PALE); c.font=Font(bold=True)
    ws.cell(i,4).number_format='0.00%'; ws.cell(i,5).number_format='0.00%'
ws['A21']='Назначение'
ws['B21']='Секторные средние и стандартные отклонения не заменяют новую квантильную модель. Они используются как benchmark при тестировании: новая модель должна давать не худшее покрытие при более узком или сопоставимом диапазоне.'
ws['A22']='Ограничение'
ws['B22']='Срезы с числом валидных наблюдений менее 5 не рассматриваются как самостоятельные нормативы.'
for r in [21,22]:
    ws.cell(r,1).fill=PatternFill('solid',fgColor=YELLOW); ws.cell(r,1).font=Font(bold=True); ws.cell(r,2).fill=PatternFill('solid',fgColor=YELLOW)
    for c in ws[r][:2]: c.border=Border(left=THIN,right=THIN,top=THIN,bottom=THIN); c.alignment=Alignment(vertical='center',wrap_text=True)
for j,w in enumerate([40,18,22,22,20,46],1): ws.column_dimensions[get_column_letter(j)].width=w
ws.freeze_panes='A4'; ws.sheet_view.showGridLines=False
wb.save(path)
print(path)

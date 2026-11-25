import tkinter as tk
from tkinter import filedialog, colorchooser
import qrcode
from PIL import Image, ImageTk
from functools import partial


# Словарь для хранения текущей конфигурации QR code
data_qr = {
    'img_file': None, # Переменная для хранения QR code
    'img_color': "#c0c0c0", # цвет QR code по умолчанию
    'img_bg': "white", # задний фон QR code по умолчанию
    'logo': None, # логотип на QR code
    'logo_side': 'center', # расположение логотипа
    'text': 'Образец QR code' # текс который будет преобразован в QR code
}


def choice_color(place):
    """Функция устанавливает цвет"""
    
    color = colorchooser.askcolor()
    colorHEX = color[1]
    if colorHEX:
        data_qr[place] = colorHEX
    create_qr()


def add_logo(logo=None):
    """Функция добавляет ссылку на логотип в словарь"""
    
    data_qr['logo'] = logo
    if logo:
        status = 'normal' 
    else:
        selected_place_logo.set("center") # устанавливаем в значение по умолчанию
        status = 'disabled'
    switch_radio_button(status) # изменяем статус radio_button
    add_side_logo()
    create_qr()


def switch_radio_button(status):
    """Функция активирует или деактивирует radio_button"""
    
    for radio_button in [radio_center, radio_left, radio_right, radio_top, radio_bottom]:
        radio_button.config(state=status)
                
                
def add_side_logo():
    """Функция сохраняет в словарь значение положения логотипа"""
    
    data_qr['logo_side'] = selected_place_logo.get()
    create_qr()
    
    
def add_text():
    """Функция добавляет введённый текст в словарь"""
    
    data = entry.get() # получаем введённые данные
    if data == '': # Если ничего не ввели
        data_qr['text'] = 'Образец QR code'
    else:
        data_qr['text'] = data
    create_qr()


def create_qr():
    """Функция создаёт QR code"""

    data = data_qr['text']

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(data) # Загружаем данные

    qr.make(fit=True) # Подбираем минимальный размер для QR-кода
    
    # Генерация изображения QR-кода без логотипа
    img = qr.make_image(
                fill_color=data_qr['img_color'],
                back_color=data_qr['img_bg']
                )
    
    if data_qr['logo']: # Добавляем логотип в QR-код (елси data_qr['logo'] != None)
        
        img = img.convert('RGB')  
        logo = Image.open(data_qr['logo']) # Загрузка логотипа
        
        #  Масштаб логотипа — 25% от ширины QR-кода
        qr_width, qr_height = img.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
           
        # Расчёт позиции логотипа
        if data_qr['logo_side'] == "center":
            logo_pos = (
                    (qr_width - logo_size) // 2,
                    (qr_height - logo_size) // 2
                )    
        elif data_qr['logo_side'] == "bottom":
            logo_pos = (
                    (qr_width - logo_size) // 2,
                    (qr_height - logo_size)
                )
        elif data_qr['logo_side'] == "top":
            logo_pos = (
                    (qr_width - logo_size) // 2,
                    (0)
                )    
        elif data_qr['logo_side'] == "right":
            logo_pos = (
                    (qr_width - logo_size),
                    (qr_height - logo_size) // 2
                )
        elif data_qr['logo_side'] == "left":
            logo_pos = (
                    (0),
                    (qr_height - logo_size) // 2
                )
            
        img.paste(logo, logo_pos, mask=logo) # Вставка логотипа
        
    img = img.resize((200, 200))

    img_tk = ImageTk.PhotoImage(img)
    qr_lable.config(image=img_tk)
    qr_lable.image = img_tk
    data_qr['img_file'] = img # сохраняем значение img в словарь
    
    
def save_qr():
    """Функция сохраняет QR code"""
    
    if data_qr['text'] != 'Образец QR code':
        file = filedialog.asksaveasfile(
            mode='w',
            defaultextension=".png",
            filetypes=[
                    ("PNG", ".png"),
                    ("JPEG", ".jpeg"),
                    ("WEBP", ".webp"),
                    ("ALL", ".*"),
                    ]
            )
    
        # Если пользователь нажал «Сохранить» (файл не None)
        if file:
            data_qr['img_file'].save(file.name)  # Сохраняем изображение
            entry.delete(0, tk.END) # Очищаем поле ввода текста
            qr_lable.config(image="", text='QR code сохранён', font='normal 15')
            selected_place_logo.set("center")
            switch_radio_button('disabled')
            
            # значения словаря приводим в начальное состояние
            data_qr['img_file'] = None
            data_qr['img_color'] = "#c0c0c0" 
            data_qr['img_bg'] = "white" 
            data_qr['logo'] = None
            data_qr['text'] = 'Образец QR code'
            data_qr['logo_side'] = 'center'


window = tk.Tk()
window.title("Генератор QRcode") # Название 
window.geometry("600x500") # Размер окна
window.resizable(width=False, height=False)  # запрет на изменение окна

# Создаём объект PhotoImage из файла
icon = tk.PhotoImage(file=r"C:\Users\nemo\Desktop\Проекты HTML\Python\Create_Qrcode\img\logo.png")

# Устанавливаем его как иконку окна
window.iconphoto(False, icon)  # Первый аргумент: False — иконка только для главного окна

frame = tk.Frame(window, borderwidth=2, relief='solid')
frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

name = tk.Label(frame, text='Введите текст для конвертации', font='normal 14')
name.pack(pady=5)

# Создаём переменную
entry_var = tk.StringVar()

entry = tk.Entry(frame, textvariable=entry_var, width=30, font='normal 14')
entry.pack(pady=5)

# Создаём фрейм, внутри которого будет выбор цвета
choice_frame = tk.Frame(frame)
choice_frame.pack(pady=5)

button_bg = tk.Button(
    choice_frame, 
    text='Цвет фона', 
    font='10', width=15, 
    command=lambda: choice_color('img_bg'))

button_bg.grid(row=0, column=0, padx=5)

button_color = tk.Button(
    choice_frame, text='Цвет QR code', 
    font='10', width=15, 
    command=lambda: choice_color('img_color'))

button_color.grid(row=0, column=1, padx=5)

# Создаём фрейм, внутри которого будут кнопки
button_frame = tk.Frame(frame, width=30)
button_frame.pack(pady=10)

button1 = tk.Button(button_frame, text='Обычный QR', font='10', width=15, command=add_logo)
button1.grid(row=0, column=0, padx=5)

button2 = tk.Button(button_frame, 
                    text='Телефон QR', 
                    font='10', width=15, 
                    command=partial(add_logo, r'C:\Users\nemo\Desktop\Проекты HTML\Python\Create_Qrcode\img\logo_phone.png')
                    )
button2.grid(row=0, column=1, padx=5)

button3 = tk.Button(button_frame,
                    text='Email QR', 
                    font='10', width=15, 
                    command=partial(add_logo, r'C:\Users\nemo\Desktop\Проекты HTML\Python\Create_Qrcode\img\logo_mail.png')
                    )
button3.grid(row=0, column=2, padx=5)

# Создаём фрейм, внутри которого будут radiobutton
radio_frame = tk.Frame(frame)
radio_frame.pack(pady=5)

radio_title = tk.Label(radio_frame, text="Расположение логотипа: ", font='10')
radio_title.grid(row=0, column=0)

# Создаём общую переменную для radiobutton
selected_place_logo = tk.StringVar(value="center")

# Создаём переключатели
radio_center = tk.Radiobutton(radio_frame, text="Центр", variable=selected_place_logo, value="center", state='disabled', command=add_side_logo)
radio_center.grid(row=0, column=1)
radio_left = tk.Radiobutton(radio_frame, text="Лево", variable=selected_place_logo, value="left", state='disabled', command=add_side_logo)
radio_left.grid(row=0, column=2)
radio_right = tk.Radiobutton(radio_frame, text="Право", variable=selected_place_logo, value="right", state='disabled', command=add_side_logo)
radio_right.grid(row=0, column=3)
radio_top = tk.Radiobutton(radio_frame, text="Верх", variable=selected_place_logo, value="top", state='disabled', command=add_side_logo)
radio_top.grid(row=0, column=4)
radio_bottom = tk.Radiobutton(radio_frame, text="Низ", variable=selected_place_logo, value="bottom", state='disabled', command=add_side_logo)
radio_bottom.grid(row=0, column=5)


qr_lable = tk.Label(frame, width=200, height=200)
qr_lable.config(image=create_qr())
qr_lable.pack(anchor='center', pady=10)

# Метод trace запускает функцию при изменении переменной
# "w" означает, что отслеживается только запись (не создание)
# entry_var.trace("w", lambda *args: qr_lable.config(image=create_qr(logo=None)))
entry_var.trace_add("write", lambda *args: qr_lable.config(image=add_text()))

button4 = tk.Button(frame, text='Сохранить QR', font='10', width=15, command=save_qr)
button4.pack(pady=5)


window.mainloop()
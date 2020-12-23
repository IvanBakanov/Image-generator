# Adapted for .exe

import requests
import colorama
from colorama import Fore, Back, Style
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from random import randint as rnd
from random import choice as ch

colorama.init()

sys_barr='-----'
color=''
bit_letters='ABCDEF'
rgb_lst=[]
strict_filt_lst=[ImageFilter.CONTOUR, ImageFilter.DETAIL, ImageFilter.EMBOSS, ImageFilter.FIND_EDGES, ImageFilter.SHARPEN]
graceful_filt_lst=[ImageFilter.BLUR, ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE]
    
# ----- Functions -----
# Перевод цвета из HEX формата в RGB
def Hex_to_rgb(hex_color):
    global rgb_lst
    for i in range(0, len(hex_color), 2):
        res_1=16*int(hex_color[i]) if hex_color[i].isdigit() else 16*int(bit_letters.index(hex_color[i])+10)
        res_2=int(hex_color[i+1]) if hex_color[i+1].isdigit() else int(bit_letters.index(hex_color[i+1])+10)
        rgb_lst.append(res_1+res_2)
    return tuple(rgb_lst)

# Функция для ввода цвета текста
def Color_enter():
    global color
    print('\n'+Fore.WHITE+'White: #FFFFFF\n'+Fore.RED+'Red: #FF0000\n'+Fore.GREEN+'Green: #00FF00\n'+Fore.CYAN+'Blue: #0000FF\n'+Fore.YELLOW+'Yellow: #FFFF00')
    print(Style.RESET_ALL)
    color=str(input('Enter the color of your text in HEX format. You can use the above colors.\n'))    

# Генерация картинки в изящном стиле
def Graceful_st():
    filt_img=img.filter(ch(graceful_filt_lst))
    return filt_img

# Генерация картинки в строгом стиле
def Strict_st():
    filt_img=img.filter(ch(strict_filt_lst))
    return filt_img

# Обработка данных
def Data_processing():
    if style==2:
        img=Graceful_st()
    elif style==3:
        img=Strict_st()
    # Рисуем текст на картинке
    if text!='/skip':
        ImageDraw.Draw(img).text((rnd(0, img.width//4), rnd(0, img.height//4)), text, font=font, fill=color)
    return img

# ----- Start -----
# ----- Copyright and about program -----
print(Back.BLUE+'© Bakanov Ivan\nhttps://github.com/IvanBakanov')
print(Style.RESET_ALL+'Version 0.0.1\n')

# ----- First user step -----
print('First, select your image style:')
style=str(input('Normal - 1\n'+'Graceful - 2\n'+'Strict - 3\n'))
# Список с вариантами ответа
style_lst=['1', '2', '3']
# Проверка на число
while True:
    if not style in style_lst:
        print(Fore.RED+'Error: You entered an invalid number')
        print(Style.RESET_ALL)
        print('First, select your image style:')
        style=str(input('Normal - 1\n'+'Graceful - 2\n'+'Strict - 3\n'))
    else:
        style=int(style)
        break
    
print(Fore.GREEN+'{0} Success {0}'.format(sys_barr))
print(Style.RESET_ALL)

# ----- Second user step -----
while True:
    img_file=str(input('Next, enter the URL of the picture you like or image path: '))
    # URL
    if img_file[0:4]=='http':
        try:
            # Пытаемся получить ответ...
            resp=requests.get(img_file, stream=True).raw
        except requests.exceptions.RequestException as e:
            print(Fore.RED+'Error: '+str(e).format(sys_barr))
            print(Style.RESET_ALL)
            continue
        else:
            try:
                # Пытаемся открыть найденную картинку...
                img=Image.open(resp)
            except Exception:
                print(Fore.RED+'Error: Unable to open image')
                print(Style.RESET_ALL)
                continue
            else:
                break
    # PATH
    else:
        try:
            img=Image.open(img_file)
        except Exception as e:
            print(Fore.RED+'Error: Unable to open image')
            print(Style.RESET_ALL)
            continue
        else:
            break

print(Fore.GREEN+'{0} Success {0}'.format(sys_barr))
print(Style.RESET_ALL)

# Изменяем размер картинки
while True:
    try:
        img_size=str(input('Enter the size of the image in pixels along the x and y axes, separated by a space,\nor write “/skip” to keep the original size.\nYour image size - {}.\n'.format(img.size)))
        if img_size!='/skip': 
            img_size=img_size.split(' ')
            for i in range(len(img_size)):
                img_size[i]=int(img_size[i])
            img=img.crop((0, 0, img_size[0], img_size[1]))
    except Exception:
        print(Fore.RED+'Error: Bad input')
        print(Style.RESET_ALL)
        continue
    else:
        print(Fore.GREEN+'{0} Success {0}'.format(sys_barr))
        print(Style.RESET_ALL)
        break
    
# ----- Third user step -----
text=str(input('If you want to add text to the picture, then enter English text, if not,\nthen write "/skip".\n'))
if text!='/skip':
    # Просим ввести цвет в HEX
    Color_enter()
    while True:
        try:
            if color[0]=='#':
                color=Hex_to_rgb(color[1:])
            else:
                print(Fore.RED+'Error: You entered the wrong color')
                Color_enter()
                continue
        except Exception:
            print(Fore.RED+'Error: You entered the wrong color')
            Color_enter()
            continue
        else:
            print(Fore.GREEN+'{0} Success {0}'.format(sys_barr))
            break
        
    # Получаем путь к шрифту и размер текста
    while True:
        try:
            print(Style.RESET_ALL)
            path=str(input('Enter the full path to the font you want to use for the text.\nC:\Windows\Fonts\Arial.ttf - standart.\n'))
            f_size=str(input('\nEnter text size: '))
            font=ImageFont.truetype(path, int(f_size))
        except Exception as e:
            print(Fore.RED+'Error: You entered the wrong information ({})'.format(e))
            continue
        else:
            print(Fore.GREEN+'{0} Success {0}'.format(sys_barr))
            break
print(Style.RESET_ALL)
    
# ----- Data processing -----
img=Data_processing()

# ----- Saving a picture -----
img_name=str(input('Enter image file name: '))
file_ext=str(input('\nEnter file extension (png/jpeg/bmp): ')).lower()
while file_ext!='png' and file_ext!='jpeg' and file_ext!='bmp':
    print(Fore.RED+'Error: Bad input')
    print(Style.RESET_ALL)
    file_ext=str(input('Enter file extension (png/jpeg/bmp): ')).lower()
img.save('{0}.{1}'.format(img_name, file_ext), file_ext)
print(Fore.GREEN+'{0} Success {0}'.format(sys_barr))
print(Style.RESET_ALL)
print('The file is located next to the program.')

# ----- End the program -----
input('\nEnter something to exit: ')
   

 

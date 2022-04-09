from PIL import Image, ImageDraw, ImageFont
from datetime import date

def get_month(current_date):
    month_num = current_date.month
    if month_num == 1:
        return "january"
    elif month_num == 2:
        return "february"
    elif month_num == 3:
        return "march"
    elif month_num == 4:
        return "april"
    elif month_num == 5:
        return "may"
    elif month_num == 6:
        return "june"
    elif month_num == 7:
        return "july"
    elif month_num == 8:
        return "august"
    elif month_num == 9:
        return "september"
    elif month_num == 10:
        return "october"
    elif month_num == 11:
        return "november"
    elif month_num == 12:
        return "december"
    else:
        return "DATE_ERROR"

def create_image():
    canvas = Image.open("assets/imageBlank.png")
    todays_date = date.today()
    font = ImageFont.truetype(font='assets/Helvetica.ttf', size=69)
    draw = ImageDraw.Draw(canvas)
    draw.text([1150, 500], get_month(todays_date), fill=(255, 0, 0), font=font)
    draw.text([1155, 600], str(todays_date.day), fill=(255, 0, 0), font=font)
    canvas.save("buffer/image_date.png", "PNG")

create_image()
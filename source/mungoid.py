from PIL import Image, ImageDraw
import numpy as np

def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def st_color(c_in):
    color = c_in.lower()
    if color == "red":
        return [(255, 7, 5), (206, 0, 0)]
    elif color == "blue":
        return [(17, 36, 147), (7, 11, 147)]
    elif color == "green" or color == "dark green":
        return [(17, 127, 45), (10, 77, 46)]
    elif color == "pink":
        return [(237, 84, 186), (171, 43, 173)]
    elif color == "orange":
        return [(239, 125, 13), (179, 62, 21)]
    elif color == "yellow":
        return [(245, 245, 87), (194, 135, 34)]
    elif color == "grey" or color == "gray":
        return [(63, 71, 78), (30, 31, 38)]
    elif color == "white":
        return [(214, 224, 240), (131, 148, 191)]
    elif color == "purple":
        return [(107, 47, 187), (59, 23, 124)]
    elif color == "brown":
        return [(113, 73, 30), (94, 38, 21)]
    elif color == "teal" or color == "cyan":
        return [(56, 253, 219), (36, 168, 190)]
    elif color == "lime" or color == "light green":
        return [(80, 239, 57), (21, 167, 66)]
    else:
        raise ValueError
    
def darken(color):
    darkened = []
    for i in color:
        darkened.append(int(i*0.78))

    return tuple(darkened)

def create_image(rgb=None, color=None):
    if color != None:
        colorlist = st_color(color)
    
    elif rgb != None:
        print("Using RGB colorspace:", rgb)
        colorlist = [rgb]
        colorlist.append(darken(rgb))

    else:
        raise ValueError
        return

    canvas = Image.open('assets/among-us.png')
    image_data = np.array(canvas)
    red, green, blue, alpha = image_data.T
    #Get Mask
    bright_areas = (red == 255) & (green == 7) & (blue == 5)
    dark_areas = (red > 119) & (green < 100)
    shade_areas = (red == 206) & (green == 0) & (blue == 0)
    #Apply Mask
    image_data[..., :-1][dark_areas.T] = darken(colorlist[1])
    image_data[..., :-1][shade_areas.T] = colorlist[1]   
    image_data[..., :-1][bright_areas.T] = colorlist[0] 

    out = Image.fromarray(image_data)
    out.save('buffer/mungoid.png', 'PNG')
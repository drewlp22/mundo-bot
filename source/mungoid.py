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

    print(colorlist)
    canvas = Image.open('assets/among-us.png')
    image_data = np.array(canvas)
    red, green, blue, alpha = image_data.T
    #Bright Colors
    bright_areas = (red == 255) & (green == 7) & (blue == 5)
    image_data[..., :-1][bright_areas.T] = colorlist[0]
    #Shaded Colors
    
    shade_areas = (red == 206) & (green == 0) & (blue == 0)
    image_data[..., :-1][shade_areas.T] = colorlist[1]
    #Dark Colors
    dark_areas = (red > 119) & (green < 100)
    image_data[..., :-1][dark_areas.T] = darken(colorlist[1])

    out = Image.fromarray(image_data)
    out.save('buffer/mungoid.png', 'PNG')
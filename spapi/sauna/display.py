from threading import Thread
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_GPIO.SPI as SPI
import ST7735
from spapi.sauna import thermometer

SPEED_HZ = 4000000

# Raspberry Pi configuration.
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Create TFT LCD display class.
DISP = ST7735.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))

THERM = None
TEMP = 0
HUMID = 0

def get_center_pos(canvas_pos: tuple, canvas_size: tuple, object_size: tuple):
    center_pos_x = canvas_pos[0] + ((canvas_size[0] / 2) - (object_size[0] / 2))
    center_pos_y = canvas_pos[1] + ((canvas_size[1] / 2) - (object_size[1] / 2))
    return (int(center_pos_x), int(center_pos_y))

def draw_rotated_text(image, text, position, angle, font, fill=(255, 255, 255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0, 0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    image.paste(rotated, position, rotated)

def get_text_size(image, text, font):
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    return (width, height)

def display_thread():
    while True:
        DISP.clear()

        #Draw Thermometer Image
        image_therm = Image.open('../resources/thermometer.png')
        image_therm = image_therm.rotate(90, expand=True)
        DISP.buffer.paste(image_therm, (21, 127), image_therm)

        #Draw Humidity Image
        image_humid = Image.open('../resources/humidity.png')
        image_humid = image_humid.rotate(90, expand=True)
        DISP.buffer.paste(image_humid, (85, 127), image_humid)

        #Draw Degree Celcius Image
        image_dc = Image.open('../resources/degreecelcius.png')
        image_dc = image_dc.rotate(90, expand=True)
        DISP.buffer.paste(image_dc, (26, 12), image_dc)

        #Draw Percentage Image
        image_percent = Image.open('../resources/percent.png')
        image_percent = image_percent.rotate(90, expand=True)
        DISP.buffer.paste(image_percent, (90, 13), image_percent)

        #Draw Line Image
        image_line = Image.open('../resources/line.png')
        image_line = image_line.rotate(90, expand=True)
        DISP.buffer.paste(image_line, (65, 20), image_line)

        font_temp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 29)
        global THERM
        temp_text = "{:.1f}".format(THERM.temperature)
        temp_text_size = get_text_size(DISP.buffer, temp_text, font_temp)
        temp_text_position = get_center_pos(
            (0, 0),
            (64, 160),
            (temp_text_size[1], temp_text_size[0]))

        font_humid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
        humid_text = str(int(THERM.humidity))
        humid_text_size = get_text_size(DISP.buffer, humid_text, font_humid)
        humid_text_position = get_center_pos(
            (64, 0),
            (64, 160),
            (humid_text_size[1], humid_text_size[0]))

        draw_rotated_text(
            DISP.buffer,
            temp_text,
            temp_text_position,
            90, font_temp, fill=(255, 255, 255))
        draw_rotated_text(
            DISP.buffer,
            humid_text,
            humid_text_position,
            90, font_humid, fill=(255, 255, 255))

        DISP.display()

def start_display(therm: thermometer.Thermometer):
    # Initialize display.
    DISP.begin()

    # Clear the display.
    DISP.clear()

    global THERM
    THERM = therm

    _thread = Thread(target=display_thread)
    _thread.daemon = True
    _thread.start()

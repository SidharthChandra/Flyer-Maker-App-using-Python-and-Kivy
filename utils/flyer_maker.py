from PIL import Image, ImageDraw, ImageFont


class FlyerMaker:
    LINE_FONT = "static/Oswald-Bold.ttf"
    ALIGNMENT = {"top": 100, "center": 2}

    def __init__(self, image_path, quote, position):
        self.image_path = image_path
        self.quote = quote
        self.position = position

    def execute(self):
        base_layer, width, height = self.add_transparent_black(self.image_path)
        final_image = self.add_quotes(base_layer, width, height, self.quote, self.position)
        return final_image

    @staticmethod
    def add_transparent_black(image_path):
        img = Image.open(image_path)
        width, height = img.size
        black_img = Image.new('RGB', (width, height), (0, 0, 0))
        img = img.convert('RGBA')
        black_img = black_img.convert('RGBA')
        base_layer = Image.blend(img, black_img, alpha=0.6)
        return base_layer, width, height

    def add_quotes(self, base_layer, width, height, quote, position):
        draw = ImageDraw.Draw(base_layer)
        quote_lines = quote.split("|")
        quote_lines = list(filter(None, quote_lines))
        num_lines = len(quote_lines)
        self.set_bottom_alignment(num_lines, width)
        font_size_dict = self.get_font_size_and_spacing(height)
        line_spacing = 10
        for line in quote_lines:
            font = ImageFont.truetype(self.LINE_FONT, font_size_dict["font_size"])
            text_w, text_h = font.getsize(line)
            x_pos = (width - text_w) / 2
            y_pos = (height / self.ALIGNMENT[position]) + line_spacing
            draw.text((x_pos, y_pos), line.upper().strip(), (255, 255, 255), font=font)
            line_spacing += font_size_dict["font_size"]
        return base_layer

    def set_bottom_alignment(self, num_lines, width):
        if width > 700:
            self.ALIGNMENT["bottom"] = 1 + (num_lines * 0.05)
        elif width <= 500:
            self.ALIGNMENT["bottom"] = 1 + (num_lines * 0.15)
        elif 500 < width <= 700:
            self.ALIGNMENT["bottom"] = 1 + (num_lines * 0.10)

    @staticmethod
    def get_font_size_and_spacing(height):
        if height < 600:
            size_dict = {"font_size": 25, "watermark_size": 15}
        elif height >= 1700:
            size_dict = {"font_size": 80, "watermark_size": 35}
        elif 600 <= height < 1700:
            size_dict = {"font_size": 40, "watermark_size": 20}
        return size_dict

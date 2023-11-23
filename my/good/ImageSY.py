from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
def watermark_img(img_path,res_path, text, pos):
    img = Image.open(img_path)
    wm = ImageDraw.Draw(img)
    col= (9, 3, 10)
    wm.text(pos, text, fill=col)
    img.show()
    img.save(res_path)



img = '/Users/lzf2/Desktop/python/1.png'
watermark_img(img, 'result.jpg','刘志方111111111111', pos=(100, 100))



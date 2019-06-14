from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import random

#设置字体，如果没有，也可以不设置
font = ImageFont.truetype("./old/NotoSansCJK-Bold.ttc",72)
 
#打开底版图片
n = str(random.randint(1,5))
imageFile = "./old/old-" + n + ".jpg"
im1=Image.open(imageFile)
    
# 在图片上添加文字 1
draw = ImageDraw.Draw(im1)
with open("./old/tmp.txt") as tmp :
    t = tmp.read()
    draw.text((100, 100),t,(255,255,0),font=font)
    draw = ImageDraw.Draw(im1)

# 保存
im1.save("./old/target.jpg")

# 上傳imgur
from imgurpython import ImgurClient

client_id = '7291da1009844e4'
client_secret = '6167b1eeded3edba21d8b58380561dc66b473f8d'
access_token = '941e397db1f99c71080841fa18b450502440ddfd'
refresh_token = '927780137a650ad68e0d3fe655eadb22ebc4608e'
client = ImgurClient(client_id, client_secret, access_token, refresh_token)
album = None # You can also enter an album ID here
config = {
    'album': album,
}
image = client.upload_from_path("./old/target.jpg", config=config, anon=False)
with open("./old/link.txt",'w') as lin :
    lin.write(image['link'])


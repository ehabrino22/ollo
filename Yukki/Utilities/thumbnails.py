from Yukki import BOT_NAME
import os
import random
from os import path

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np


ddef changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)

    # fonts
    font1 = ImageFont.truetype(r'Utils/Lalezar-Regular.ttf', 30)
    font2 = ImageFont.truetype(r'Utils/Lalezar-Regular.ttf', 60)
    font3 = ImageFont.truetype(r'Utils/Lalezar-Regular.ttf', 40)
    font4 = ImageFont.truetype(r'Utils/Lalezar-Regular.ttf', 35)

    image4 = ImageDraw.Draw(image2)
    image4.text((10, 10), BOT_NAME, fill="white", font = font1, align ="left") 
    image4.text((670, 150), status, fill="white", font = font2, align ="left") 

    # title
    title1 = truncate(title)
    image4.text((670, 300), text=title1[0], fill="white", font = font3, align ="left") 
    image4.text((670, 350), text=title1[1], fill="white", font = font3, align ="left") 

    # description
    views = f"Views : {views}"
    duration = f"Duration : {duration} Mins"
    channel = f"Channel : {channel}"

    image4.text((670, 450), text=views, fill="white", font = font4, align ="left") 
    image4.text((670, 500), text=duration, fill="white", font = font4, align ="left") 
    image4.text((670, 550), text=channel, fill="white", font = font4, align ="left")

    image2.save(f"cache/final{userid}.png")
    os.remove(f"cache/thumb{userid}.jpg")
    final = f"cache/final{userid}.png"
    return final

from captcha.image import ImageCaptcha
import random
import hashlib

iconset = ['1','2','3','4','5','6','7','8','9',
          'a','b','c','d','e','f','g','h','i','j','k', 'm','n','p','q','r','s','t','u','v','w','x','y','z',
          'A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']

CapchaSize = 5

def CaptchaGenerator(chat_id, bot):
    captcha = ImageCaptcha()
    CaptchaStringList = []
    CaptchaString = ''

    for i in range(CapchaSize):
        char = random.choice(iconset)
        CaptchaStringList.append(char)

    for item in CaptchaStringList:
        CaptchaString += str(item)
    print(CaptchaString)
    image = captcha.generate(CaptchaString)
    bot.send_photo(chat_id, image)
    return HashCapcha(CaptchaString)

def HashCapcha(capcha):
    str = capcha.lower().encode('utf-8')
    return hashlib.sha256(str).hexdigest()







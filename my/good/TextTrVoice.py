from pygame import mixer
from gtts import gTTS


def main():
    tts = gTTS('我爱你，王燕燕，我的小宝贝蛋蛋老婆，你是个笨猪猪111')
    tts.save('output.mp3')
    mixer.init()
    mixer.music.load('output.mp3')
    mixer.music.play()


if __name__ == "__main__":
    main()
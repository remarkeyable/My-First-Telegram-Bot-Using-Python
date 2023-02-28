import os
KEY= os.environ['KEY']
AUDIO_PROCESSING = "Hey hooman, buckle up! Transcribing your file might take a while. Go take a walk, hit the store, " \
                   "breathe in some O2 or fly to the moon! I'll have it done when pigs fly! Just kidding, I'll make it snappy."
REMINDER = "Hey hooman! Howdy! Ready to transcribe? Great! But wait! Audio files only, no selfies or duck-faces. " \
           "And just so you know, I'm top-notch but not perfect. Don't sue if I love you becomes I loathe tofu. Let's go!"
UNKNOWN = "Hey hooman, I can't hear squat! You sure your audio file wasn't lost in a black hole or " \
          "sucked up by aliens, or do I need to get my ears checked by a purr-fessional??"


import telebot
import whisper

bot = telebot.TeleBot(KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, REMINDER)

#this will execute when the user sent a random message
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Aweee ~ I haven't been trained for this yet. Please use the command /start")

#will handle an audio/voice file sent by the user
@bot.message_handler(content_types=['audio','voice'])
def get_audio(message):
    #if user sent a voice  message this will execute
    try:
        bot.reply_to(message, AUDIO_PROCESSING )
        file = bot.get_file(message.voice.file_id)
        dl = bot.download_file(file.file_path)
        with open('tele', 'wb') as new_file:
            new_file.write(dl)
            # will handle the file and process using Open AI whisper module
            try:
                model = whisper.load_model('base')
                result = model.transcribe("tele", fp16=False, language="English")
                text = result['text']
                bot.reply_to(message, text)
                bot.reply_to(message, "Tada ~! Transcription done.")
                print("done")
            except:
                bot.reply_to(message, UNKNOWN)
                print("done")
     #else if user sent an audio file (voice that's not directly came from telegram ft, this will execute)
    except AttributeError:
        file = bot.get_file(message.audio.file_id)
        dl = bot.download_file(file.file_path)
        with open('tele', 'wb') as new_file:
            new_file.write(dl)
            #will handle the file and process using Open AI whisper module
            try:
                model = whisper.load_model('base')
                result = model.transcribe("tele", fp16=False, language="English")
                text = result['text']
                bot.reply_to(message, text)
                bot.reply_to(message, "Tada ~! Transcription done.")
                print("done")
            except:
                bot.reply_to(message, UNKNOWN)
                print("done")

bot.infinity_polling()
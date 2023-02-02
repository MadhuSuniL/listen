from threading import Thread
from gtts import gTTS
import os
from datetime import datetime
from .models import Text
from time import time



class Contert_to_audio(Thread):
    def __init__(self,request,page_no):
        self.request = request
        self.page_no = page_no
        Thread.__init__(self)
        
    def run(self):
        id = self.request.session['pdf']
        big_content = Text.objects.get(id=id).content
        name = Text.objects.get(id=id).file_name
        texts_list = str(big_content).split('^^^')
        final_text = texts_list[self.page_no]
        audio = gTTS(final_text, lang='en',slow=True)
        try:
            os.remove("static/"+self.request.session['file_name'])
        except:
            pass 
        file_name = name+str(time())+f"page_{self.page_no}"+".mp3"
        self.request.session['file_name'] = str(file_name)
        audio.save("static/"+file_name)
        data = {
            "text" : final_text,
            "path" : "/static/"+file_name,
            'line' : final_text[0:20],
            'no' : self.page_no
        }
        return data
        
                
        
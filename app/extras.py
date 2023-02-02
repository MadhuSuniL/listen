import PyPDF2
from time import time
from .models import Text
def file_to_text(file,request):
    page_texts = []
    pdfreader = PyPDF2.PdfReader(file)
    total_pages =  len(pdfreader.pages)
    s = time()
    for page_no in range(total_pages):
        page = pdfreader._get_page(page_no)
        page_texts.append(str(page.extract_text()))    
    sample_text_list = []    
    big_content = ''''''
    p = 0
    for page in page_texts:
        if page != '':
            big_content += page
            big_content += "^^^"
        
            if len(page) > 100 :
                sample_text_list.append({
                    'page':p,
                    'text':page[:100]+'...'
                })    
            else:
                sample_text_list.append({
                    'page':p,
                    'text':page[:len(page)]+'...'
                })    
                
        p += 1
    
    text = Text.objects.create(file_name=file.name,content=big_content)
    request.session['pdf'] = text.id
    
    data = {
        'total_pages':total_pages,
        'sample_contents':sample_text_list,
        }
    
    
    return data


from gtts import gTTS
import os
from datetime import datetime
def text_to_audio(request,page_no):
   id = request.session['pdf']
#    id = 1
   big_content = Text.objects.get(id=id).content
   name = Text.objects.get(id=id).file_name
   texts_list = str(big_content).split('^^^')
   final_text = texts_list[page_no]
   
   if len(final_text) == 0:
       final_text = 'Dear user, This Page is empty continue with next page..!'
   audio = gTTS(final_text, lang='en',lang_check=True)
   try:
       os.remove("static/"+request.session['file_name'])
   except:
       pass 
   file_name = name+str(time())+f"page_{page_no}"+".mp3"
   request.session['file_name'] = str(file_name)
   audio.save("static/"+file_name)

   if page_no == len(texts_list)-1:
         next_ref = 0
   else:
       next_ref = page_no + 1
    
   if page_no == 0:
         pre_ref = len(texts_list)-1
   else:
       pre_ref = page_no - 1 
   print(page_no,pre_ref,next_ref,len(texts_list)) 
   data = {
       "text" : final_text,
       "path" : "/static/"+file_name,
       'line' : final_text[0:20],
       'no' : page_no+1,
       'next_url':"/get_audio/"+str(next_ref),
       'pre_url':"/get_audio/"+str(pre_ref)
   }
   request.session['data'] = data
   return data
   


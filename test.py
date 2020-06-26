import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from pydub.silence import split_on_silence

myaudio = AudioSegment.from_file("audio.wav" , "wav") 
chunk_length_ms = 59000 # pydub calculates in millisec
chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec
  
#Export all of the individual chunks as wav files

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    print ("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")

i=0
for chunk in chunks:
    print ("in chunks")
    chunk_silent = AudioSegment.silent(duration = 10)
    audio_chunk = chunk_silent + chunk + chunk_silent
    audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
    filename = 'chunk'+str(i)+'.wav'
    print("Processing chunk "+str(i))
    file = filename
    r = sr.Recognizer()
    with open("recognize.txt", "a") as rct:
        with sr.AudioFile(file) as source:
            r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)
        while True:
            try:
                rec = r.recognize_google(audio_listened)
                rct.write(rec + " ")
                print (rec + " ")
                break
            except Exception as e:
                print(e)
                None
                #rec = r.recognize_google(audio_listened, show_all=True)
                #rct.write(rec + " ")
                #print(rec,type(rec))

        i += 1
    rct.close()
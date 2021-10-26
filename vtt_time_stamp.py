from tkinter import *
from tkinter.filedialog import askopenfilename
from pygame import mixer

mixer.init()
music = mixer.music
class mus():
    pass
musi = mus()


root = Tk()
root.attributes("-topmost",True)


# ____________ GETTING FILE ___________
file_Lab = Label(root,text="File Name",font="N 14",bg="black",fg="blue");file_Lab.pack(fill="x")
musi.music = askopenfilename(
    initialdir = "",
    title = "Select Music File",
    filetypes = (
        ("MP3 type","*.mp3"),("OGG type","*.ogg"),("WAV type","*.wav"),("All types","*.*")
        )
    )
musi.file = askopenfilename(
    initialdir = "",
    title = "Select Subtitle File (file to be edited)",
    filetypes = (
        ("All types","*.*"),("VTT type","*.vtt")
        )
    )
musi.text_file = askopenfilename(
    initialdir = "",
    title = "Select Text File (pre-written text)",
    filetypes = (
        ("All type","*.*"),("VTT file","*.vtt"),("Text file","*.txt")
        )
    )

file_Lab.config(text=f"MUSIC:  {musi.music} \n SUB:  {musi.file} \n TEXT:{musi.text_file}")
# __________ File Name on window done __________


# 00:00:00.100 --> 00:00:04.220

def vtt_write(file,start,finish,text):
    Content = f"{start} --> {finish}\n"+text+"\n\n"
    with open(file,"a") as f:
        f.write(Content)
    return Content

fr1 = Frame(root);fr1.pack(fill="both")

fr = Frame(fr1);fr.pack(side="left",fill="both",expand=1)
fr_vtt = Frame(fr);fr_vtt.pack(side="bottom",fill="both",expand=1)


file = Text(fr1,width=50)
file.pack(side="right")
file.insert(1.0,"SUBTITLE FILE")

preview = Text(fr1,width=40);preview.pack(side="right")
preview.insert(1.0,"TEXT FILE")


def file_data():
    file.delete(2.0,"end")
    with open(musi.file,encoding="Latin-1") as f:
        data = f.read()
    file.insert(2.0,"\n"+data)
    del data

    preview.delete(2.0,"end")
    with open(musi.text_file,encoding="Latin-1") as f:
        data = f.read()
    preview.insert(2.0,"\n"+data)
    del data
file_data()

def start():
    global fin
    music.load(musi.music)
    music.play()
    fin_update() if fin else None
    fin = False
Button(fr,text="Play",command=start).pack(side="left")


musi.paused = False
def pauser():
    music.unpause() if musi.paused else music.pause()
    musi.paused = not musi.paused
Button(fr,text="Pause/Unpause",command=pauser).pack(side="left")


Button(fr,text="Refresh",command=None).pack(side="right")#file_data


musi.start = StringVar()
musi.finish = StringVar()
musi.text = StringVar()

musi.start.set("00:00:00.000")
musi.finish.set("00:00:00.000")

fin = True
def fin_update():
    time = music.get_pos()
    m = str( int( (time/1000)/60 ) ).zfill(2)
    up = f"00:{m}:{ str( abs(round(int(m)*60 - time/1000 ,3)) ).zfill(6) }"

    musi.finish.set(up)

    root.after(100,fin_update)

def sub_yield(file):
    with open(file) as f:
        while True:
            x = f.readline()
            if x not in ("\n",""):
                yield x.rstrip()
            elif x == "":
                return
            else:
                continue

data = sub_yield(musi.text_file)

def add():
    fin = musi.finish.get()
    vtt_write(musi.file,musi.start.get(),fin,musi.text.get())
    musi.start.set(fin)
    musi.text.set(next(data))


Label(fr_vtt,text="From:").grid(row=0,column=0)
Label(fr_vtt,text="To:").grid(row=0,column=1)

Label(fr_vtt,textvariable=musi.start,font="14").grid(row=1,column=0,padx=10)
Label(fr_vtt,textvariable=musi.finish,font="14").grid(row=1,column=1,padx=10)

Label(fr_vtt,text="Subtitle:",font="16").grid(columnspan=10,sticky="news",padx=10)
Entry(fr_vtt,textvariable=musi.text).grid(columnspan=10,sticky="news",padx=10)

Button(fr_vtt,text="Next",command=lambda:musi.text.set(next(data)) ).grid(sticky="w",row=4,column=0,padx=10,pady=10)
Button(fr_vtt,text="Add",command=add).grid(sticky="news",row=4,column=1,columnspan=10,pady=10)


# Button(fr,text="Jump 1 min",command=lambda:music.set_pos(59)).pack()

root.mainloop()

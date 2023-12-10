from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as tkb
import random

minute = 1
second = 60

def random_kelime():
    with open("test.txt", "r" ,encoding="utf-8") as test:
        lines = test.readlines()
    lines = [line.strip() for line in lines]
    return random.sample(lines,45)

def update_soru_alani ():
    soru_alani.config(text=rand_lines)

def update_timer():
    global second
    second -= 10
    if second >= 10:
        timer.config(text=f"{minute}:{second}")
    else:
        timer.config(text=f"{minute}:0{second}")
    tid = timer.after(1000, update_timer)
    if second == 0:
        timer.after_cancel(tid)
        girdi_alani.configure(state="disabled")
    
def weird_timer():
    timer.after(1000, update_timer)

def spaceBind(e):
    print(rand_lines)
    global minute
    minute = 0 
    if not hasattr(spaceBind, "bir_kere_calis"):
        weird_timer()
        spaceBind.bir_kere_calis = True
    try:
        if girdi_alani.get() == rand_lines[0] :
            girdi_alani.configure(bootstyle="success")
            girdi_alani.after(100, trueAns)
        if girdi_alani.get() != rand_lines[0]:
            girdi_alani.configure(bootstyle="danger")
            girdi_alani.after(100, falseAns)
    except IndexError:
        pass

def trueAns():
    girdi_alani.configure(bootstyle="dark")
    girdi_alani.delete(0,tkb.END)
    girdi_alani.icursor(0)        
    rand_lines.pop(0)
    true_meter.step(1)
    update_soru_alani()

def falseAns():
    girdi_alani.configure(bootstyle="dark")
    girdi_alani.delete(0,tkb.END)
    girdi_alani.icursor(0)
    rand_lines.pop(0)
    false_meter.step(1)
    update_soru_alani()

def meter():
    # false_meter.step(1)
    pass

def fast_remove(e):
    girdi_alani.delete(0, tkb.END)

def izle(e):
    print(e)

# ttkbootstrap config 
root = tkb.Window(themename="superhero", title="TypingTest", size=(1000,600), resizable=(False,False))
root.iconbitmap("favicon.ico")

# tkb UI
soru_alani = tkb.Label(root, bootstyle="inverse-light",background="white" ,text="", justify="left", wraplength=680, font=("",14))
soru_alani.place(x=150 , y=50, relheight=0.18, relwidth=0.7)

# Girdi Alanı
girdi_alani_frame = tkb.Frame(root, bootstyle="secondary")
girdi_alani_frame.place(x=150 , y=190 , relheight=0.09, relwidth=0.7)

girdi_alani = tkb.Entry(girdi_alani_frame, bootstyle="light", font=("", 14))
girdi_alani.place(x=100 , y=4 , relheight=0.85, relwidth=0.6)

timer = tkb.Label(girdi_alani_frame, text=f"{minute}:00", bootstyle="inverse-dark", font=("",19))
timer.place(x=540 , y=6)

photo = tkb.PhotoImage(file=r"img/reload.png")
photo_image = photo.subsample(19,19)

refresh_button = tkb.Button(girdi_alani_frame, image=photo_image , bootstyle="primary", takefocus=False, command=meter)
refresh_button.place(x=630 , y=5)
# -------------------

# CPM or Etc
true_meter = tkb.Meter(amounttotal=100, bootstyle="success",amountused=0, interactive=False, subtext="Doğru", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=7, metertype="semi", meterthickness=10)
true_meter.place(x=310 , y=400)

cpm_meter = tkb.Meter(amounttotal=400, amountused=78, interactive=False, subtext="CPM", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=7, metertype="semi", meterthickness=10)
cpm_meter.place(x=450 , y=400)

false_meter = tkb.Meter(amounttotal=100, bootstyle="danger", amountused=0, interactive=False, subtext="Yanlış", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=6, metertype="semi", meterthickness=10)
false_meter.place(x=590 , y=400)
# -------------------------------------
if __name__ == "__main__":
    girdi_alani.bind("<space>", spaceBind)
    girdi_alani.bind("<Control-a>", fast_remove)
    root.bind("<KeyPress>", izle)
    rand_lines = random_kelime()
    soru_alani.config(text=rand_lines)
    root.mainloop()


#       Toplam yazılan karakter sayısı
# CPM = ------------------------------
#        Dakika başına geçen süre / 5 
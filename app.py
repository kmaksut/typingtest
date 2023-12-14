from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as tkb
import random
 
minute = 1
second = 60
total_true_char = 0
total_false_char = 0

def random_kelime():
    with open("test.txt", "r" ,encoding="utf-8") as test:
        lines = test.readlines()
    lines = [line.strip().lower() for line in lines]
    return random.sample(lines,35)

def update_soru_alani ():
    soru_alani.config(text=rand_lines)

def update_timer():
    global second, tid
    second -= 1
    if second >= 10:
        timer.config(text=f"{minute}:{second}")
    else:
        timer.config(text=f"{minute}:0{second}")
    tid = timer.after(1000, update_timer)
    if second == 0:
        timer.after_cancel(tid)
        girdi_alani.configure(state="disabled")
        refresh_button.configure(state="enabled")
        second = 60

def weird_timer():
    timer.after(1000, update_timer)

def spaceBind(e):
    print(girdi_alani.get())
    global minute, total_false_char, total_true_char
    minute = 0 
    if not hasattr(spaceBind, "one_times"):
        weird_timer()
        spaceBind.one_times = True
    try:
        if len(rand_lines) == 1 :
            timer.after_cancel(tid)
            refresh_button.configure(state="enabled")
            girdi_alani.configure(state="disabled")
            cpm_calculate()

        if girdi_alani.get() == rand_lines[0] :
            girdi_alani.configure(bootstyle="success")
            girdi_alani.after(100, trueAns)
            total_true_char += len(rand_lines[0])

        if girdi_alani.get() != rand_lines[0]:
            if second != 60 :    
                girdi_alani.configure(bootstyle="danger")
                girdi_alani.after(100, falseAns)
                total_false_char += len(rand_lines[0])
            else:
                girdi_alani.configure(bootstyle="dark")

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

def refresh_test():
    global rand_lines, second, minute
    true_meter.amountusedvar.set(0)
    false_meter.amountusedvar.set(0)
    cpm_meter.amountusedvar.set(0)
    girdi_alani.configure(state="enabled")
    girdi_alani.delete(0, tkb.END)
    girdi_alani.icursor(0)
    rand_lines = random_kelime()
    update_soru_alani()
    second = 60
    minute = 0
    timer.config(text=f"{minute}:00")
    refresh_button.configure(state="disabled")
    weird_timer()

def fast_remove(e):
    girdi_alani.delete(0, tkb.END)

def cpm_calculate():
    total_char = total_true_char+total_false_char
    prcs = (60-second)
    if second == 60:
        return cpm_meter.amountusedvar.set(int(total_char/(60/5)))
    else:
        return cpm_meter.amountusedvar.set(int(total_char/(prcs/5)))

def kp_watch(e):
    print(e)

# ttkbootstrap config 
root = tkb.Window(themename="superhero", title="TypingTest", size=(1000,600), resizable=(False,False))
root.iconbitmap("img/favicon.ico")

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

refresh_button = tkb.Button(girdi_alani_frame, state="disabled", image=photo_image , bootstyle="primary", takefocus=False, command=refresh_test)
refresh_button.place(x=630 , y=5)
# -------------------

# CPM or Etc
true_meter = tkb.Meter(amounttotal=100, bootstyle="success",amountused=0, interactive=False, subtext="Doğru", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=7, metertype="semi", meterthickness=10)
true_meter.place(x=310 , y=400)

cpm_meter = tkb.Meter(amounttotal=400, amountused=0, interactive=False, subtext="CPM", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=7, metertype="semi", meterthickness=10)
cpm_meter.place(x=450 , y=400)

false_meter = tkb.Meter(amounttotal=100, bootstyle="danger", amountused=0, interactive=False, subtext="Yanlış", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=6, metertype="semi", meterthickness=10)
false_meter.place(x=590 , y=400)
# -------------------------------------
if __name__ == "__main__":
    girdi_alani.bind("<space>", spaceBind)
    girdi_alani.bind("<Control-a>", fast_remove)
    # root.bind("<KeyPress>", kp_watch)
    rand_lines = random_kelime()
    soru_alani.config(text=rand_lines)
    root.mainloop()


#       Toplam yazılan karakter sayısı
# CPM = ------------------------------
#        Dakika başına geçen süre / 5 
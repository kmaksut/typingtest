from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as tkb
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.validation import *
from tkinter import messagebox
import pymongo 
import tools
import random

# Global Vars
minute = 1
second = 60
total_true_char: int = 0
total_false_char: int = 0
isLogin: bool = False
# -------------------

# Funcs

def random_kelime():
    with open("test.txt", "r" ,encoding="utf-8") as test:
        lines = test.readlines()
    lines = [line.strip().lower() for line in lines]
    return random.sample(lines,35)

def update_soru_alani ():
    soru_alani.config(text=rand_lines)

def update_timer():
    global second, tid
    second -= 10
    if second >= 10:
        timer.config(text=f"{minute}:{second}")
    else:
        timer.config(text=f"{minute}:0{second}")
    tid = timer.after(1000, update_timer)
    if second == 0:
        timer.after_cancel(tid)
        girdi_alani.configure(state="disabled")
        refresh_button.configure(state="enabled")
        cpm_calculate()
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

def login_register():

    client = pymongo.MongoClient("mongodb://localhost:27017")
    def visibility_change():
        password_entry.configure(show=False)
        visibility_button.configure(image=visibility_off)
    
    def login():
        try:
            collection = client["your_database"]
            users = collection["users"]
            if users.find_one({"username":username_entry.get(),"password":password_entry.get()}) :
                messagebox.showinfo("Login","Giriş Onaylandı")
                isLogin = True
                if isLogin == True:
                    login_register_button.place_forget()
                    toplevel.destroy()
                    dashboard_button = tkb.Button(root, image=visibility_on , bootstyle="primary-outline", takefocus=False)
                    dashboard_button.place(x=930, y=10)

                    dashboard_top = tkb.Toplevel(title="Dashboard",size=(400,400) ,resizable=(False,False), position=(500,300))
                    dashboard_top.iconbitmap("img/keyboard_2.ico")

                    dashboard_top.mainloop()

            else:
                messagebox.showerror("Login","Kullanıcı adı veya şifre yanlış !!!")
        except Exception as e :
            print(e)

    # PhotoImage
    username_image = tkb.PhotoImage(file=r"img/person.png")
    password_image = tkb.PhotoImage(file=r"img/lock.png")
    visibility_on = tkb.PhotoImage(file=r"img/visibility_on.png")
    visibility_off = tkb.PhotoImage(file=r"img/visibility_off.png")

    # Styles
    notebook_style = tkb.Style()
    notebook_style.configure("TNotebook",highlightbackground="red")

    toplevel = tkb.Toplevel(title="Login-Register",resizable=(False,False), size=(400,400), position=(900,280))
    toplevel.iconbitmap("img/keyboard_2.ico")
    
    top_label = tkb.Label(toplevel, text="Login", font=("",15))
    top_label.place(x=175 , y=20)

    separator_top = tkb.Separator(toplevel, bootstyle="secondary", orient="horizontal", )
    separator_top.place(x=0, y=50, relheight=0.1, relwidth=1)

    # Notebook
    login_register_notebook = tkb.Notebook(toplevel, bootstyle="light", style="TNotebook")
    login_register_notebook.place(x=8 , y=90)

    # Login
    login_frame = tkb.Frame(login_register_notebook, width=380, height=250)
    
    username_icon = tkb.Label(login_frame, image=username_image ,bootstyle="inverse-primary", anchor="center")
    username_icon.place(x=10, y=40, relheight=0.18, relwidth=0.13)

    password_icon = tkb.Label(login_frame, image=password_image ,bootstyle="inverse-primary", anchor="center")
    password_icon.place(x=10, y=120, relheight=0.18, relwidth=0.13)

    username_entry = tkb.Entry(login_frame, font=("",13))
    username_entry.place(x=58, y=40, relwidth=0.8, relheight=0.18)

    password_entry = tkb.Entry(login_frame, font=("",13), show="*")
    password_entry.place(x=58, y=120, relwidth=0.8, relheight=0.18)

    visibility_button = tkb.Button(login_frame, image=visibility_on, takefocus=False, command=visibility_change)
    visibility_button.place(x=315, y=120, relheight=0.18)

    login_button = tkb.Button(login_frame, text="Login", takefocus=False, command=login)
    login_button.place(x=140, y=200, relwidth=0.3, relheight=0.16)
    
    # Register
    register_frame = tkb.Frame(login_register_notebook, width=380, height=250)

    register_username_icon = tkb.Label(register_frame, image=username_image ,bootstyle="inverse-primary", anchor="center")
    register_username_icon.place(x=10, y=40, relheight=0.18, relwidth=0.13)

    register_password_icon = tkb.Label(register_frame, image=password_image ,bootstyle="inverse-primary", anchor="center")
    register_password_icon.place(x=10, y=120, relheight=0.18, relwidth=0.13)

    register_username_entry = tkb.Entry(register_frame)
    register_username_entry.place(x=58, y=40, relwidth=0.8, relheight=0.18)

    register_password_entry = tkb.Entry(register_frame, font=("",13), show="*")
    register_password_entry.place(x=58, y=120, relwidth=0.8, relheight=0.18)

    register_button = tkb.Button(register_frame, text="Login", takefocus=False)
    register_button.place(x=140, y=200, relwidth=0.3, relheight=0.16)

    login_register_notebook.add(login_frame, text="Login")
    login_register_notebook.add(register_frame, text="Register")

    # Configs
    for lconfigs in [username_entry, register_username_entry]:
        lconfigs.insert(0, "username")
        lconfigs.configure(foreground="grey", font=("",9))

    for rconfigs in [password_entry, register_password_entry]:
        rconfigs.insert(0, "password")
        rconfigs.configure(foreground="grey", font=("",9))

    # funcs

    def login_inputs(event):
        print(password_entry.get().strip())
        # Login username
        if username_entry.get().strip() == " " or tools.is_space(username_entry.get()):
            username_entry.delete(0, tkb.END)  
            username_entry.icursor(0)

        # Login password
        if password_entry.get().strip() == " " or tools.is_space(password_entry.get()):
            password_entry.delete(0,tkb.END)
            password_entry.icursor(0)

    def login_register_switch(e):
            if login_register_notebook.index(login_register_notebook.select()) == 1: 
                top_label.configure(text="Login")
                top_label.place(x=175, y=20)
            else: 
                top_label.configure(text="Register") 
                top_label.place(x=160,y=20)
    login_register_notebook.bind("<Button-1>", login_register_switch)

    def ufocusIn(event):
        # Login Username Entry
        if username_entry.get() == "username":
            username_entry.delete(0,tkb.END)
            username_entry.insert(0,"")
            username_entry.configure(foreground="white", font=("",13))
        # Register Username Entry
        if register_username_entry.get() == "username":
            register_username_entry.delete(0,tkb.END)
            register_username_entry.insert(0,"")
            register_username_entry.configure(foreground="white", font=("",13))

    def ufocusOut(event):
        # Login Username Entry
        if username_entry.get() == "":
            username_entry.insert(0,"username")
            username_entry.configure(foreground="grey", font=("",9))
        # Register Username Entry
        if register_username_entry.get() == "":
            register_username_entry.insert(0,"username")
            register_username_entry.configure(foreground="grey", font=("",9))

    def rfocusIn(event):
        # Login Password Entry
        if password_entry.get() == "password":
            password_entry.delete(0,tkb.END)
            password_entry.insert(0, "")
            password_entry.configure(foreground="white", font=("",13))  
        # Register Password Entry
        if register_password_entry.get() == "password":
            register_password_entry.delete(0,tkb.END)
            register_password_entry.insert(0, "")
            register_password_entry.configure(foreground="white", font=("",13))

    def rfocusOut(event):
        # Login Password Entry
        if password_entry.get() == "":
            password_entry.insert(0,"password")
            password_entry.configure(foreground="grey", font=("",9))
        # Register Password Entry
        if register_password_entry.get() == "":
            register_password_entry.insert(0,"password")
            register_password_entry.configure(foreground="grey", font=("",9))


    # Binds
    for usernameBindings in [username_entry, register_username_entry]:
        usernameBindings.bind("<FocusIn>",ufocusIn)
        usernameBindings.bind("<FocusOut>", ufocusOut)
        
    for passwordBindings in [password_entry, register_password_entry]:
        passwordBindings.bind("<FocusIn>",rfocusIn)
        passwordBindings.bind("<FocusOut>", rfocusOut)

    for loginBindindgs in [username_entry, password_entry]:
        loginBindindgs.bind("<Key>", login_inputs)
        loginBindindgs.bind("<Key>", login_inputs)

    toplevel.mainloop()
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ttkbootstrap config 
root = tkb.Window(title="TypingTest", themename="superhero" ,size=(1000,600),position=(400,200) ,resizable=(False,False))
root.iconbitmap("img/keyboard_2.ico")

# Photo Image
refresh_photo = tkb.PhotoImage(file=r"img/refresh.png")
account_photo = tkb.PhotoImage(file=r"img/account.png")
# photo_image = refresh_photo.subsample(19,19) # fotoğraf boyutunu ayarlar

# Styles
account_photo_style = tkb.Style()
account_photo_style.configure("TButton",bg="red")

# tkb UI
soru_alani = tkb.Label(root, bootstyle="inverse-light",background="white" ,text="", justify="left", wraplength=680, font=("",14), borderwidth=0.5, relief="solid")
soru_alani.place(x=150 , y=50, relheight=0.18, relwidth=0.7)

# Girdi Alanı
girdi_alani_frame = tkb.Frame(root, bootstyle="secondary")
girdi_alani_frame.place(x=150 , y=190 , relheight=0.09, relwidth=0.7)

girdi_alani = tkb.Entry(girdi_alani_frame, bootstyle="light", font=("", 14))
girdi_alani.place(x=100 , y=4 , relheight=0.85, relwidth=0.6)

timer = tkb.Label(girdi_alani_frame, text=f"{minute}:00", bootstyle="inverse-dark", font=("",16), background="#2b3e50", width=3.5, padding=3)
timer.place(x=540 , y=6)

refresh_button = tkb.Button(girdi_alani_frame, bootstyle="primary" ,state="disabled", image=refresh_photo, takefocus=False, command=refresh_test)
refresh_button.place(x=625 , y=5, relheight=0.8)

# Login - Register
login_register_button = tkb.Button(root, image=account_photo, takefocus=False, bootstyle="secondary-outline", command=login_register)
login_register_button.place(x=930, y=10)

# CPM or Etc
true_meter = tkb.Meter(amounttotal=100, bootstyle="success",amountused=0, interactive=False, subtext="Doğru", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=7, metertype="semi", meterthickness=10)
true_meter.place(x=310 , y=400)

cpm_meter = tkb.Meter(amounttotal=400, amountused=0, interactive=False, subtext="CPM", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=7, metertype="semi", meterthickness=10)
cpm_meter.place(x=450 , y=400)

false_meter = tkb.Meter(amounttotal=100, bootstyle="danger", amountused=0, interactive=False, subtext="Yanlış", metersize=80, textfont=("",11), subtextfont=("",6), stripethickness=10, wedgesize=6, metertype="semi", meterthickness=10)
false_meter.place(x=590 , y=400)

# ToolTip
# cpm_meter_tooltip = ToolTip(cpm_meter, text="Merhaba", delay=1)

# -------------------------------------
if __name__ == "__main__":
    girdi_alani.bind("<space>", spaceBind)
    girdi_alani.bind("<Control-a>", fast_remove)
    rand_lines = random_kelime()
    soru_alani.config(text=rand_lines)
    root.mainloop()

#       Toplam yazılan karakter sayısı
# CPM = ------------------------------
#        Dakika başına geçen süre / 5 
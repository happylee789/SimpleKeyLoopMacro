#https://pypi.org/project/keyboard/
# pyinstaller.exe -F -w --onefile --icon=icon.ico main.py
import keyboard, time
import threading
import mySound as sound
import sys # 애플리케이션 종료 등

insSound = sound.mySound()

isRunning = False
Trigger = False
mySoundEffect = ""
myHotkey = []
mySkill = []
myDelay = []
myInstance = []

def threadSound():
    insSound.playSound(mySoundEffect)
# 단축키 및 스킬 키로 ',' 사용금지

with open('config.txt') as f:
    lines = f.readlines() # list containing lines of file
    i=0
    for line in lines:
        line = line.strip()
        if line:
            columns = [item.strip() for item in line.split(',')]
            if mySoundEffect=="": mySoundEffect=line
            else:
                myDelay.append(columns[0])
                myHotkey.append(columns[1:3])
                mySkill.append(columns[3])

#-------------------------------------------
import tkinter as tk # 애플리케이션 gui
# 새 윈도우를 만들고, 위젯 및 기능을 넣습니다.
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        # 업데이트용 변수와 라벨
        self.log = tk.StringVar()
        self.log.set("How To Use? ▶ README.txt")
        self.lb3 = tk.Label(window, textvariable=self.log, fg="black", font=("Arial",15))
        # self.lb3.config(font=("Arial",30))
        # self.lb3.grid(row=0,column=0)
        self.lb3.pack(fill='both',expand=True)

window = tk.Tk()

window.title("Simple Key Press Loop")
window.geometry("300x50+1200+200")
window.resizable(True,True)
window.call('wm', 'attributes', '.', '-topmost', '1')
# 앱 시작
app = Application(master=window)

class myLoop():
    def __init__(self,_delay,_hotKeys,_skillKeys):
        keyboard.add_hotkey(_hotKeys[0], self.initSkill, args=())
        keyboard.add_hotkey(_hotKeys[1], self.stopSkill, args=())
        self.hotkeys = _hotKeys
        self.delay = float(_delay)
        self._skillKeys = _skillKeys
        self.skillKeys = [item.strip() for item in _skillKeys.split('+')]

    def threadSkills(self):
        global isRunning, Trigger
        if isRunning : return
        else : isRunning = True
        max = 999
        for i in range(max):
            app.log.set("RUNNING : "+self._skillKeys.upper()+"("+str(i+1)+")")
            if len(self.skillKeys)==1:
                keyboard.press(self.skillKeys[0])
                time.sleep(0.02)
                keyboard.release(self.skillKeys[0])    
            if len(self.skillKeys)==2:
                keyboard.press(self.skillKeys[0])
                keyboard.press(self.skillKeys[1])
                time.sleep(0.02)
                keyboard.release(self.skillKeys[0]+', '+self.skillKeys[1])                
            if len(self.skillKeys)==3:
                keyboard.press(self.skillKeys[0])
                keyboard.press(self.skillKeys[1])
                keyboard.press(self.skillKeys[2])
                time.sleep(0.02)
                keyboard.release(self.skillKeys[0]+', '+self.skillKeys[1]+', '+self.skillKeys[2])
            if i+1 < max:
                for _ in range(max(1,int(self.delay*10.0))):
                    time.sleep(0.1)
                    if Trigger:
                        app.log.set("STOP")
                        isRunning = False
                        Trigger = False
                        x = threading.Thread(target=threadSound, args=())
                        x.setDaemon = True
                        x.start()
                        return
        app.log.set("STOP")
        Trigger = False
        isRunning = False
        x = threading.Thread(target=threadSound, args=())
        x.setDaemon = True
        x.start()

    def initSkill(self):
        keyboard.release(self.hotkeys[0].replace('+',','))
        x = threading.Thread(target=self.threadSkills, args=())
        x.setDaemon = True
        x.start()

    def stopSkill(self):
        keyboard.release(self.hotkeys[1].replace('+',','))
        global Trigger
        if isRunning:
            Trigger = True

for i in range(len(myHotkey)):
    myInstance.append(myLoop(myDelay[i],myHotkey[i],mySkill[i]))

app.mainloop()
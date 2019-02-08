from tkinter import *
import random

xPos = 20
yPos = 20
xSpeed = 1
ySpeed = 0
scl = 20
menue = 20
speed = 1
speedUp = True
fr = 150
gameOver = False

# r = 0
# g = 170
# b = 0 

width = 400
height =  400

geo = str(width)+"x"+str(height)

foodX = scl*2
foodY = scl*2

total = 0
tail = []

# Fenster
tk = Tk()
tk.title("Spiel 1")
tk.configure(background='darkgray')
tk.geometry(geo)

#tk.wm_attributes("-transparent", True)


# "Leinwand" erstelen u
cs = Canvas(tk,background = "black", bd=0, highlightthickness=0)
cs.place(x=0, y=20, width=width, height=height)


def pick_Location():
    global foodX, foodY
    foodX = random.randint(0,width//scl-1)*scl
    foodY = random.randint(0,(height-menue)//scl-1)*scl

def eat():
    global total
    if xPos == foodX and yPos == foodY:
        total += 1
        return True
    else:
        return False

def death():
    global xPos, yPos, tail, total, fr, gameOver
    for i in tail:
        if xPos == i[0] and yPos == i[1]:
            #total = 0
            #tail = [] 
            gameOver = True

            # Anezeige "GAME OVER"    
            lGO = Label(master=tk, text='GAME OVER', fg='red', bg='darkgray', font=('Courier',24))
            lGO.place(x=100, y=180, width=200, height=40)

            cs.create_rectangle(xPos,yPos,xPos+scl,yPos+scl, fill="red")

            

def draw_tail():
    global tail, total
    for i in range(0,len(tail)):
        cs.create_rectangle(tail[i][0], tail[i][1], tail[i][0]+scl,
                            tail[i][1]+scl, fill = "darkgreen")

def animiate(level=1):
    cs.delete("all")
    draw_one_frame()
    if not gameOver:
        tk.after(fr,animiate)

def draw_one_frame():
    global xPos, yPos, total, speed, speedUp, fr#,r,g,b

    #colorval = "#%02x%02x%02x" % (r,g ,b )

    xPos %= width
    yPos %= height-menue
        
    if  total == len(tail):
        for i in range(len(tail)-1):
            tail[i] = tail[i+1]
        if (len(tail)>0):   
            tail[-1] = (xPos,yPos)
    else:
        tail.append((xPos,yPos)) 

    xPos = xPos + xSpeed * scl
    yPos = yPos + ySpeed * scl

    if (eat()):
        pick_Location()    
  
    cs.create_rectangle(foodX,foodY,foodX+scl,foodY+scl, fill="blue")
    
    draw_tail()
    cs.create_rectangle(xPos,yPos,xPos+scl,yPos+scl, fill="green")
    
    death()

    if total > 0 and speedUp and total % 10 == 0:
        speedUp = False 
        speed += 1
        fr = int(fr // 1.5)
    
    if total % 10 != 0:
        speedUp = True
    
    lScore.config(text='Score: '+str(total))
    lSpeed.config(text='Speed: '+str(speed))

def key(event):
    global xSpeed, ySpeed
    if event.keysym == "Up":
        xSpeed = 0
        ySpeed = -1

    if event.keysym == "Down":
        xSpeed = 0
        ySpeed = 1

    if event.keysym == "Right":
        xSpeed = 1
        ySpeed = 0

    if event.keysym == "Left":
        xSpeed = -1
        ySpeed = 0

tk.bind_all("<Key>",key)

# Label der rStatuszeile
# Punkteanzeige
lScore = Label(master=tk, text='Score: '+str(total), fg='yellow', bg='darkgray', font=('Courier', 16))
lScore.place(x=0, y=0, width=100, height=20)

# Geschwindigkeitsanzeige    
lSpeed = Label(master=tk, text='Speed: '+str(speed), fg='yellow', bg='darkgray', font=('Courier', 16))
lSpeed.place(x=300, y=0, width=100, height=20)


tk.after(100,animiate)  
tk.mainloop()
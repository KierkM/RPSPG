import tkinter as tk
import config
from random import randint

class Rpspg(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
        self.createBackground()
        self.welcomeText()
        self.resultText()
        self.hpBox()
        

    def createWidgets(self):
        #various buttons, the three actions and some test commands
        self.rockButton = tk.Button(text = 'Low Attack', command = lambda: self.playAction(0))
        self.paperButton = tk.Button(text = 'Mid Attack', command = lambda: self.playAction(1))
        self.scissButton = tk.Button(text = 'High Attack', command = lambda: self.playAction(2))
        self.atButton = tk.Button(text = '@ spawn', command=self.spawnAt)
        self.atRemove = tk.Button(text = '@ remove', command=lambda: self.delAt(config.n - 1))
        self.runGame = tk.Button(text = 'Start game logic', command=self.cpuAction)
        self.buttons = [self.rockButton,self.paperButton,self.scissButton,
                        self.atButton,self.atRemove,self.runGame]
        i = 0
        
        for button in self.buttons:
            if(i<3):
                button.grid(column=41 + i, row = 30)
            else:
                button.grid(column=41 + (i-3), row = 31)
            i = i + 1

    def createBackground(self):
        #creates canvas and paints background
        self.canvas = tk.Canvas(height = 400, width = 400)
        self.bkimage = tk.PhotoImage(file = 'background.png')
        self.background = self.canvas.create_image(200,200, image=self.bkimage)
        self.canvas.grid(rowspan=40,columnspan=40, row = 0, column = 0)

    def welcomeText(self):
        #adds the first text field to the game
        self.wtext = tk.Message(text='Welcome to RPSRPG',width = 200)
        self.wtext.grid(column = 1,row = 41)

    def resultText(self):
        #second text field
        self.rtext = tk.Message(text="Blank?", width = 250)
        self.rtext.grid(column = 1, row = 42)

    def hpBox(self):
        #hp display
        self.hpbox = tk.Message(text='HP ' + str(config.playerhp))
        self.hpbox.grid(column = 41, row = 1)

    def spawnAt(self):
        #spawns enemies, limit of 3, specified locations runs actions so cpu is ready
        if(config.n<3):
            self.atimage = tk.PhotoImage(file = 'atsymb.png')
            
            self.wtext.config(text='@ spawned!')
            config.imagearray.append(self.atimage)
            for img in config.imagearray:
                self.atimgspawn = self.canvas.create_image((200+50*config.n) ,
                                                       (300-50*config.n),
                                                       image=self.atimage,
                                                       tag = 'at'+str(config.n))
            config.n = config.n + 1
            self.cpuAction()
           
    def delAt(self, x):
        #remove enemies, board is cleared and spawned between turns.
        if(config.n > 0):
            config.imagearray.pop(x)
            config.cpuchoice.pop(x)
            self.canvas.delete('at'+str(x))
            
            self.wtext.config(text='@ deleted')
            config.n = config.n - 1
           
            

    def cpuAction(self):
        #cpu picks a random selection, noted by ints 0,1 or 2
        i = 0
        j = 0
        #reset holding arrays for future turns, removes old info
        config.textarray = []
        config.cpuchoice = []
        #text field 1 shows enemy ready to act
        self.wtext.config(text='Enemy prepares to act!')
        while(i < len(config.imagearray)):
            config.cpuchoice.append(randint(0,2)) # num of choices made = num of images on board
            if(config.cpuchoice[i] == 0):
                config.textarray.append('Soldier '+str(i + 1)+' readies a low attack!') 
            elif(config.cpuchoice[i] == 1):
                config.textarray.append('Soldier '+str(i + 1)+' readies a mid attack!')
            elif(config.cpuchoice[i] == 2):
                config.textarray.append('Soldier '+str(i + 1)+' readies a high attack!')
            i = i + 1

        #initialize our final display string blank to remove any old info.
        #combine strings stored in array to create final string to display
        readytext = ""  
        while(j < len(config.textarray)):
            readytext = readytext + " " + config.textarray[j]
            j = j + 1
        self.wtext.config(text=config.textarray)

    def playAction(self,p):
        #main action module, collects player choice data from buttons and compares with
        #cpu choices to determine outcome
        i = 0
        j = 0
        k = len(config.cpuchoice)
        attacks = config.playerattacks  #you can only attack so many times a turn
        res = ""
        config.textarray = []
        config.tbd = []
        while(i < k and config.playerhp > 0):
            #conditions are checked only if you have attacks left
            if(p == 0 and attacks > 0):
                if(config.cpuchoice[i] == 1):
                    config.textarray.append('You Lose!')
                elif(config.cpuchoice[i] == 0):
                    config.textarray.append('Tie!')
                elif(config.cpuchoice[i] == 2):
                    config.textarray.append('You Win!')
               
            elif(p == 1 and attacks > 0):
                if(config.cpuchoice[i] == 2):
                    config.textarray.append('You Lose!')
                elif(config.cpuchoice[i] == 1):
                    config.textarray.append('Tie!')
                elif(config.cpuchoice[i] == 0):
                    config.textarray.append('You Win!')
            elif(p == 2 and attacks > 0):
                if(config.cpuchoice[i] == 0):
                    config.textarray.append('You Lose!')
                elif(config.cpuchoice[i] == 2):
                    config.textarray.append('Tie!')
                elif(config.cpuchoice[i] == 1):
                    config.textarray.append('You Win!')

            elif(attacks == 0):         #no more attacks case
                config.textarray.append('You are defenseless!')

            if(attacks > 0):  
                attacks = attacks - 1

            #following statement counts how many enemies survived
            if(config.textarray[i] != 'You Win!' and len(config.textarray) > 0):
                j = j + 1

            #two checks for hp loss, lose or no attacks
            if(config.textarray[i] == 'You Lose!'):
                config.playerhp = config.playerhp - 1

            if(config.textarray[i] == 'You are defenseless!'):
                config.playerhp = config.playerhp - 1
            self.hpbox.config(text=str(config.playerhp))
            res = res + '\n' + config.textarray[i]
            
            i = i + 1
        self.rtext.config(text=res)
        #clear all enemies death also causes all enemies to clear
        while(0 < k + 1):
            self.delAt(k - 1)
            k = k - 1

        #respawn survivors
        while(0 < j):
            self.spawnAt()
            j = j - 1

        #check global win/loss conditions
        if(config.playerhp <= 0):
            self.wtext.config(text='You died!')

        if(len(config.imagearray) <= 0 and config.playerhp > 0):
            self.wtext.config(text='You won the fight!')

        
        
        
            
        
        
app = Rpspg()
app.master.title('RPSPG')
app.mainloop()

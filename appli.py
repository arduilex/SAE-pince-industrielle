import RPi.GPIO as GPIO
from VL53L0X import CapteurTof
from HCSR04 import CapteurHC
from os import system

# Féfinition de la classe Application
class Application(object):
    """Classe qui contrôle chaque menuu de l'application"""
    def __init__(self, cad):
        # Configuration du pifacecad
        self.cad = cad
        self.cad.lcd.backlight_on()
        self.cad.lcd.blink_off()
        self.cad.lcd.cursor_off()
        # Gestion mesure et chiffrage
        self.mesure = 0
        self.etat = "ope"
        self.led_color="green"
        # coordonnées de départ et des menus
        self.cursor = 0
        self.col, self.row = (0,0)
        self.id_menu = "home"
        self.db_menu = {
            'home':[("get",(1,0)),("set",(5,0)),("H",(9,0)),("mod",(1,1)),("typ",(5,1)),("cap",(9,1))],
            'typ': [("good",(1,0)),("beter",(6,0)),("best",(1,1)),("speed",(6,1)),("OK",(14,1))],
            'set': [("min:",(1,0)),("max:",(1,1)),("rs",(14,0)),("OK",(14,1))],
            'mod': [("auto",(1,0)),("manual",(1,1)),("OK",(14,1))],
            'cap': [("laser",(1,0)),("ultrason",(1,1)),("OK",(14,1))],
            'H':   [("get",(1,0)),("set",(5,0)),("H",(9,0)),("mod",(1,1)),("typ",(5,1)),("cap",(9,1)),("exit",(12,0)),("OK",(14,1))]
        }
        # Récupération des parametres enregistrés dans le fichier texte
        f = open("parameter.txt", 'r')
        self.parameter = eval(f.readline())
        self.led_pin = eval(f.readline())
        self.optoc_pin = eval(f.readline())
        self.optoc_etat = [0, 0]
        self.hc_pin = eval(f.readline())
        f.close()
        if self.parameter["cap"]=="laser":
            self.range = self.parameter["range_tof"]
        else:
            self.range = self.parameter["range_hc"]
        GPIO.setmode(GPIO.BCM)
        for pin in self.led_pin.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        for pin in self.optoc_pin.values():
            GPIO.setup(pin, GPIO.OUT)
        # Récupération du manuel d'utilisation pour le menu Help
        f = open("manual.txt", 'r')
        brut = f.readlines()
        f.close()
        self.doc = {}
        self.doc_range = [0]*2
        for i in range(0, len(brut), 3):
            self.doc[brut[i][:-2]] = brut[i+1][:-1]
        # Gestion du menu set
        self.input_value = [0]*4
        self.input_lock = 0
        # Création d'un objet CapteurTof 
        self.tof = CapteurTof()
        # Création d'un objet CapteurHC
        self.hc = CapteurHC(self.hc_pin)
        if self.parameter["cap"]=="laser":
            self.tof.start_ranging(self.parameter["typ"])
            self.delay = self.tof.get_timing()
        else:
            self.delay = self.hc.get_timing(self.parameter["typ"])
        # Affichage du menu home
        self.update_model()
        #self.get_mesure()
        self.parameter["mod"] = "manual"
        self.update_mesure()
    def update_model(self):
        self.cad.lcd.clear()
        for element in self.db_menu[self.id_menu]:
            col,row=element[1]
            self.cad.lcd.set_cursor(col,row)
            self.cad.lcd.write(element[0])
        self.col, self.row = (1,0)
        self.cursor = 0
        self.update_selected()
        self.cad.lcd.home()
        self.cad.lcd.write(">")
    def change_captor(self):
        self.parameter["mod"]="manual"
        if self.parameter["cap"]=="laser":
                self.parameter["range_hc"] = self.range
                self.range = self.parameter["range_tof"]
                self.tof.start_ranging(self.parameter["typ"])
                self.delay = self.tof.get_timing()
        else:
            self.parameter["range_tof"] = self.range
            self.range = self.parameter["range_hc"]
            #self.tof.stop_ranging()
            self.delay = self.hc.get_timing(self.parameter["typ"])
    def input_set(self):
        row = self.cad.lcd.get_cursor()[1]
        self.cad.lcd.set_cursor(5, row)
        val=self.range[row]
        self.input_value = [val//1000%10]+[val//100%10]+[val//10%10]+[val%10]
        self.cad.lcd.write("0"*(4-len(str(val)))+str(val)+"mm*")
        self.cad.lcd.set_cursor(5, row)
        self.cad.lcd.cursor_on()
    def input_update(self, sens):
        if sens==0:
            if self.input_lock:
                self.cad.lcd.blink_off()
                self.input_lock=False
            elif self.cad.lcd.get_cursor()[0]==11:
                newValue = 0
                self.input_value.reverse()
                for i in range(4):
                    newValue+=10**i*self.input_value[i]
                self.range[self.row] = newValue
                self.id_menu="set"
                self.cad.lcd.cursor_off()
                self.cad.lcd.blink_off()
                self.update_set()
            else:
                self.cad.lcd.blink_on()
                self.input_lock=True
        elif self.input_lock:
            col = self.cad.lcd.get_cursor()[0]-5
            self.input_value[col]+=sens
            if self.input_value[col]<0:
                self.input_value[col] = 9
            elif self.input_value[col]>9:
                self.input_value[col] = 0
            self.cad.lcd.write(str(self.input_value[col]))
            self.cad.lcd.set_cursor(col+5, self.row)
        else:
            col, row = self.cad.lcd.get_cursor()
            col += sens
            if col<5:
                col=5
            elif col==10:
                col=8
            elif col>8:
                col=11
            self.cad.lcd.set_cursor(col, row)     
    def update_set(self):
        range_str = ['']*2
        for i, val in enumerate(self.range):
            range_str[i] = "0"*(4-len(str(val)))+str(val)+"mm "
        for k in range(2):
            self.cad.lcd.set_cursor(5,k)
            self.cad.lcd.write(range_str[k])
        self.cad.lcd.set_cursor(self.col, self.row) 
    def get_mesure(self):
        if self.parameter["cap"]=="laser":
            self.mesure = self.tof.get_distance()
        else:
            self.mesure = self.hc.get_distance()
        if self.mesure > 8000 or self.mesure < 0:
            self.optoc_etat = [1, 1]
            self.led_color = "Error"
            self.etat = "err"
        elif self.mesure > self.range[1]:
            self.etat = "ope"
            self.led_color = "green"
            self.optoc_etat = [1, 0]
        elif self.mesure < self.range[0]:
            self.etat = "clo"
            self.led_color = "red"
            self.optoc_etat = [0, 1]
        else:
            self.etat = "tak"
            self.led_color = "orang"
            self.optoc_etat = [0, 0]
            #print(self.optoc_etat)
    def update_mesure(self):
        if self.mesure > 8000 or self.mesure<0:
            ch_mesure = "out"
        else:
            ch_mesure = str(self.mesure)
        self.cad.lcd.set_cursor(10, 0)
        self.cad.lcd.write(' '*(4-len(ch_mesure))+ch_mesure+"mm")
        self.cad.lcd.set_cursor(13, 1)
        self.cad.lcd.write(self.etat)
        self.update_led()
        self.cad.lcd.set_cursor(self.col, self.row)
    def update_led(self):
        for pin in self.led_pin.values():
            GPIO.output(pin, False)
        if self.led_color != "Error":
            GPIO.output(self.led_pin[self.led_color], True)
    def update_optoc(self):
        for pin, etat in zip(self.optoc_pin.values(), self.optoc_etat):
            GPIO.output(pin, etat)
    def update_selected(self):
        if self.id_menu in self.parameter:
            for menu in self.db_menu[self.id_menu]:
                if menu[0] == self.parameter[self.id_menu]:
                    col, row = menu[1]
                    self.cad.lcd.set_cursor(col-1, row)
                    self.cad.lcd.write("*")
        self.cad.lcd.set_cursor(self.col-1, self.row)
    def clean_up_selected(self, sub_menu, parameter):
        for menu in sub_menu:
            if menu[0] == parameter:
                col, row = menu[1]
                self.cad.lcd.set_cursor(col-1, row)
                self.cad.lcd.write(" ")
    def doc_print(self, sens=1):
        doc = self.doc[self.id_menu[2:]].split(' ')
        if sens==-1 and self.doc_range[0]>0 or sens==1 and self.doc_range[1]<len(doc)-1:
            if sens==1:
                start = self.doc_range[1]+1
                if start==1:
                    start=0
            else:
                start = self.doc_range[0]-1
                if start==-1:
                    start=0
            end=start
            n=0
            use=0
            while n<33 and end>=0 and end<len(doc):
                n += len(doc[end])+1
                if n>16 and not use:
                    #n+= 16-(n-len(doc[end])-1)
                    n += 17-n+len(doc[end])
                    use=1
                end += sens
            end-=sens
            if end<0:
                end =0
            for i in range(3):
                if n>33:
                    n-=len(doc[end])
                    end -= sens
            if sens==-1:
                start,end = end,start
            lcd_str = ""
            use=0
            for k in range(start, end+1):
                lcd_str+=doc[k]+' '
                if k<end:
                    if not use and len(lcd_str)+len(doc[k+1])>=16:
                        lcd_str+="\n"
                        use=1
            self.cad.lcd.clear()
            self.cad.lcd.write(lcd_str)
            self.doc_range=[start, end]
    def exit(self):
        if self.parameter["cap"] == "laser":
            self.parameter["range_tof"] = self.range
        else:
            self.parameter["range_hc"] = self.range
        f = open("parameter.txt", 'w')
        f.write("{}\n{}\n{}\n{}".format(self.parameter, self.led_pin, self.optoc_pin, self.hc_pin))
        f.close()
        GPIO.output(self.led_pin[self.led_color], 0)
        self.cad.lcd.cursor_off()
        self.cad.lcd.backlight_off()
        self.cad.lcd.clear()
        self.cad.lcd.write(" Good bye.")
        GPIO.cleanup()
        exit()
        #system("sudo halt")
    def action_cursor(self, sens):
        if "H" in self.id_menu and len(self.id_menu)>1:
            self.doc_print(sens)
        elif self.id_menu == "set_input":
            self.input_update(sens)
        else:
            nb = len(self.db_menu[self.id_menu])
            self.cad.lcd.set_cursor(self.col-1, self.row)
            self.cad.lcd.write(" ")
            if sens == 1 and self.cursor < nb:
                self.cursor += 1
            elif self.cursor>=0:
                self.cursor -= 1
            if self.cursor == nb:
                self.cursor = 0
            elif self.cursor == -1:
                self.cursor = nb-1
            # update col, row
            self.col,self.row = self.db_menu[self.id_menu][self.cursor][1]
            self.update_selected()
            self.cad.lcd.write(">")
    def action_enter(self):
        if "H" in self.id_menu and len(self.id_menu)>1:
            self.id_menu="H" 
            self.update_model()
        elif self.id_menu == "set_input":
            self.input_update(0)
        else:
            action = self.db_menu[self.id_menu][self.cursor][0]
            if self.id_menu == "home":
                if action=="get":
                    self.get_mesure()
                    self.update_mesure() 
                else:
                    self.id_menu=action 
                    self.update_model()
                    if action=="set":
                        self.update_set()
                    elif action=="cap":
                        self.parameter["mod"]="manual"
            else:
                if action=="OK":
                    self.id_menu="home"
                    self.update_model()
                    self.update_mesure()
                elif "set" in self.id_menu:
                    if action=="rs":
                        self.range = [100, 200]
                        self.update_set()
                    else:
                        self.id_menu+="_input"
                        self.input_set()
                elif self.id_menu=="mod":
                    self.clean_up_selected(self.db_menu["mod"], self.parameter["mod"])
                    self.parameter["mod"] = self.db_menu["mod"][self.cursor][0]
                    self.update_selected()
                elif self.id_menu=="typ":
                    self.clean_up_selected(self.db_menu["typ"], self.parameter["typ"])
                    self.parameter["typ"] = self.db_menu["typ"][self.cursor][0]
                    self.update_selected()
                    if self.parameter["cap"]=="laser":
                        self.tof.start_ranging(mode=self.parameter["typ"])
                    else:
                        self.hc.get_timing(mode=self.parameter["typ"])
                elif self.id_menu=="cap":
                    self.clean_up_selected(self.db_menu["cap"], self.parameter["cap"])
                    self.parameter["cap"] = self.db_menu["cap"][self.cursor][0]
                    self.change_captor()
                    self.update_selected()
                elif "H" in self.id_menu:
                    if action == "exit":
                        self.exit()
                    else:
                        self.id_menu += "_"+action
                        self.doc_range=[0]*2
                        self.doc_print()
    def action_button(self, pin):
        self.cad.lcd.cursor_off()
        self.cad.lcd.blink_off()
        if pin==1:
            self.id_menu="home"
            self.update_model()
            self.update_mesure()
        elif pin==0:
            self.exit()

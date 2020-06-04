import tkinter as tk
import math, Crypto, ast, sys, base64
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

#creating a "dictionary"/button customization
button_config = {
    "bg":"#242742",
    "fg":"#d1d2de",
    "font":("Consolas bold", 12),
    "height": "2",
    "width": "7",
    "relief": "flat",
    "activebackground":"#313454"

}

digits = ["✓", "x²", "C","n!", "sin", "cos", "tan","sin⁻¹", "cos⁻¹", "tan⁻¹"]
#creating variable, first 2 invert the results from radius to grade)/cnt = control variable
deg = 1
inversa_deg = 1
cnt = 0
class Calculator:
    #creating construct (parameter master = base window)
    def __init__(self, master):
        try:
            self.privatekey, self.publickey = self.rsakeys()
            self.encrypt(self.publickey, b'ABDD2F81B2C3EADBC347C1')
        except:
            sys.exit()
            print("RSA KEY Invalid") 

        self.master = master

        #creating frame - Display Frame
        self.displayFrame = tk.Frame(self.master)
        self.displayFrame.pack()

        #packing frame in the screen (buttons)
        self.buttonsFrame = tk.Frame(self.master)
        self.buttonsFrame.pack()

        #creating database in order to create the calculator display/sunken=relevo)
        self.output = tk.Entry(self.displayFrame, width=30, relief="sunken", bd=3, font=("Consolas bold",17), fg="#c9c9c5", bg="#242742")

        # positioning widget in the main grid
        self.output.grid(row = 0, column = 0)

        #to access the variable created deg, inversa deg and cnt
        self.convert = tk.Button(self.displayFrame, button_config, width=3, height = 0, text = "DEG", bg ="#e35124", command = self.degreesRadians)
        self.convert.grid(row = 0, column = 1)

        self.createButtons()

    def rsakeys(self):  
        length=1024  
        privatekey = RSA.generate(length, Random.new().read)  
        publickey = privatekey.publickey()  
        return privatekey, publickey

    def encrypt(self, rsa_publickey, plain_text):
        encryptor = PKCS1_OAEP.new(rsa_publickey)
        encrypted = encryptor.encrypt(b'%s' % plain_text)
        b64cipher=base64.b64encode(encrypted)
        return b64cipher

    def decrypt(self, rsa_privatekey, b64cipher):
        decoded_ciphertext = base64.b64decode(b64cipher)
        decryptor = PKCS1_OAEP.new(rsa_privatekey)
        decrypted = decryptor.decrypt(ast.literal_eval(str(decoded_ciphertext)))
        return decrypted
    
    def sign(self, privatekey,data):
        return base64.b64encode(str((privatekey.sign(data,''))[0]).encode())

    def verify(self, publickey,data,sign):
        return publickey.verify(data,(int(base64.b64decode(sign)),))

    #creating buttons in the calculator i a 2d matrix
    def createButtons(self):
        self.buttons = [["✓", "x²", "**", "(", ")", "/"],
                        ["sin", "cos", "7", "8", "9", "+"],
                        ["sin⁻¹", "cos⁻¹", "4", "5", "6", "-"], 
                        ["tan", "tan⁻¹", "1", "2", "3", "*"],
                        ["n!", "n", ".", "0", "=", "C"]]
    
        #creating a repetion link that aceess different components from our calculator everytime
        for line in range(len(self.buttons)):
            #to access only the line and then column
            for column1 in range(len(self.buttons[line])):
                text1 = self.buttons[line][column1]
                #lambda = anonymous function
                #lambda x,y : expression 

            #save the information done in each interaction in a variable call text

                b = tk.Button(self.buttonsFrame, button_config, text = text1, command = lambda x = text1: self.buttonActions(x))
                b.grid(row = line, column = column1)

    #put all the functionalities inside our calculator
    def buttonActions(self, text1):
        global deg
        global inversa_deg
        if text1 != "=":
            if text1 not in digits:
                self.output.insert('end', text1)
            else:
                if text1 == "✓":
                    self.addValue(math.sqrt(float(self.output.get())))
                elif text1 == "n!":
                    self.addValue(math.factorial(float(self.output.get())))
                elif text1 == "x²":
                    self.addValue(float(self.output.get()) ** 2)
                elif text1 == "C":
                    self.addValue("")
                elif text1 == "n":
                    self.addValue(3.1415926535897932)
                elif text1 == "sin":
                    self.addValue(math.sin(float(self.output.get()) * deg))
                elif text1 == "cos":
                    self.addValue(math.cos(float(self.output.get()) * deg))
                elif text1 == "tan":
                    self.addValue(math.tan(float(self.output.get()) * deg))
                elif text1 == "sin⁻¹":
                    self.addValue(math.asin(float(self.output.get())) * inversa_deg)
                elif text1 == "cos⁻¹":
                    self.addValue(math.acos(float(self.output.get())) * inversa_deg)
                elif text1 == "tan⁻¹":
                    self.addValue(math.atan(float(self.output.get())) * inversa_deg)
                #eval = receive a string and calculate
        else:
            self.addValue(eval(self.output.get()))

                  
    def addValue(self, value):
        self.output.delete(0,'end')
        self.output.insert('end', value) 

    #global means that the variable is out of the scope, however we need to access it
    def degreesRadians(self):
        global deg
        global inversa_deg
        global cnt

        #if cnt == 0 it means that it was in radian and the user want it in degree)
        if (cnt == 0):
            deg = math.pi / 180
            inversa_deg = 180 / math.pi
            #changing buttonś name to RAD
            self.convert['text'] = "RAD"
            cnt = 1
        #if cnt different of 0
        else:
            deg = 1
            inversa_deg = 1
            self.convert['text'] = "DEG"
            cnt = 0
   



#creating object(first tk =access class, second Tk =class created)
object = tk.Tk()

Calculator(object)

#keep window loop
object.mainloop()
# pip install auto-py-to-exe   / auto-py-to-exe

























#!/usr/bin/env python3

import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
import os
import qiskit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute,IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.providers.aer import QasmSimulator



HOST = '127.0.0.1'
Socket = 123456

# After connecting, we want to use Diffie Hellman exchange to
# Exchange a single secret number.  That number out of x will
# be the pad to use.


# Builds the GUI chat, Server must be up and running
class client():
    dhprivkeys = []
    dhpubkeys = []
    secrets = []
    bundle = []

    # Obligatory initialization function
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, Socket))

        message = tkinter.Tk()
        message.withdraw()

        self.alias = simpledialog.askstring("Alias", "Please list your Alias", parent=message)

        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    # Creates the GUI
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="gray")

        frame1 = tkinter.Frame(master=self.win, bg='gray')
        frame1.pack()

        self.chatlabel = tkinter.Label(frame1, text="Chat (Unsecured): ", bg="light blue")
        self.chatlabel.config(font=("Times New Roman", 12))
        self.chatlabel.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(frame1, height=3)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msglabel = tkinter.Label(frame1, text="Type Here (Unsecured): ", bg="red")
        self.msglabel.config(font=("Times New Roman", 12))
        self.msglabel.pack(padx=20, pady=5)

        self.inputarea = tkinter.Text(frame1, height=2)
        self.inputarea.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(frame1, text="Send Chat", command=self.write)
        self.send_button.config(font=("Times New Roman", 12))
        self.send_button.pack(padx=20, pady=5)


        frame2 = tkinter.Frame(master=self.win, bg='gray')
        frame2.pack()

        self.dhlabel = tkinter.Label(frame2, text="DH calculation", bg="gray")
        self.dhlabel.config(font=("Times New Roman", 12))
        self.dhlabel.pack(padx=20, pady=5)

        self.dharea = tkinter.scrolledtext.ScrolledText(frame2, height=2)
        self.dharea.config(state='disabled')
        self.dharea.pack(padx=20, pady=5)


        self.dhPlabel = tkinter.Label(frame2, text="P = ", bg="gray")
        self.dhPlabel.config(font=("Times New Roman", 12))
        self.dhPlabel.pack(side=LEFT, pady=5)

        self.dhP = tkinter.Entry(frame2, width=3)
        self.dhP.pack(side=LEFT, pady=5)

        self.dhGlabel = tkinter.Label(frame2, text="g = ", bg="gray")
        self.dhGlabel.config(font=("Times New Roman", 12))
        self.dhGlabel.pack(side=LEFT, pady=5)

        self.dhG = tkinter.Entry(frame2, width=3)
        self.dhG.pack(side=LEFT, pady=5)


        frame3 = tkinter.Frame(master=self.win, bg='gray')
        frame3.pack(padx=5, pady=5)

        frame3sub = tkinter.Frame(master=frame3, bg='gray')
        frame3sub.pack(side=LEFT, padx=5, pady=5)

        frame3a = tkinter.Frame(master=frame3sub, bg='gray')
        frame3a.pack(side=LEFT, padx=5, pady=5)

        self.dhl1 = tkinter.Label(frame3a, text="1", bg="gray")
        self.dhl1.pack()

        self.dhinput = tkinter.Text(frame3a, height=2, width=20)
        self.dhinput.pack(pady=5)

        self.dhbutton = tkinter.Button(frame3a, text="Get # of Characters", command=self.numChars)
        self.dhbutton.config(font=("Times New Roman", 12))
        self.dhbutton.pack(pady=5)

        frame3b = tkinter.Frame(master=frame3sub, bg='gray')
        frame3b.pack(side=LEFT, padx=5, pady=5)

        self.dhl2 = tkinter.Label(frame3b, text="2", bg="gray")
        self.dhl2.pack()

        self.dhinput2 = tkinter.Text(frame3b, height=2, width=20)
        self.dhinput2.pack(pady=5)

        self.dhbutton2 = tkinter.Button(frame3b, text="Create Public Keys", command=self.pubkeys)
        self.dhbutton2.config(font=("Times New Roman", 12))
        self.dhbutton2.pack(pady=5)

        frame3c = tkinter.Frame(master=frame3sub, bg='gray')
        frame3c.pack(side=LEFT, padx=5, pady=5)

        self.dhl3 = tkinter.Label(frame3c, text="3", bg="gray")
        self.dhl3.pack()

        self.dhinput3 = tkinter.Text(frame3c, height=2, width=20)
        self.dhinput3.pack(pady=5)

        self.dhbutton3 = tkinter.Button(frame3c, text="Create OTP from Secrets", command=self.privkeys)
        self.dhbutton3.config(font=("Times New Roman", 12))
        self.dhbutton3.pack(pady=5)


        frame4 = tkinter.Frame(master=self.win, bg='gray')
        frame4.pack(padx=5, pady=5)

        frame4sub = tkinter.Frame(master=frame4, bg='gray')
        frame4sub.pack(side=LEFT, padx=5, pady=5)

        frame4a = tkinter.Frame(master=frame4sub, bg='gray')
        frame4a.pack(side=LEFT, padx=5, pady=5)

        self.encodelabel = tkinter.Label(frame4a, text="Encode", bg="gray")
        self.encodelabel.config(font=("Times New Roman", 12))
        self.encodelabel.pack(pady=5)

        self.encodeinput = tkinter.Text(frame4a, height=2, width=20)
        self.encodeinput.pack(pady=5)

        self.encodebutton = tkinter.Button(frame4a, text="Encode message", command=self.encode)
        self.encodebutton.config(font=("Times New Roman", 12))
        self.encodebutton.pack(pady=5)

        frame4b = tkinter.Frame(master=frame4sub, bg='gray')
        frame4b.pack(pady=5)

        self.decodelabel = tkinter.Label(frame4b, text="Decode", bg="gray")
        self.decodelabel.config(font=("Times New Roman", 12))
        self.decodelabel.pack(pady=5)

        self.decodeinput = tkinter.Text(frame4b, height=2, width=20)
        self.decodeinput.pack(pady=5)

        self.decodebutton = tkinter.Button(frame4b, text="Decode message", command=self.decode)
        self.decodebutton.config(font=("Times New Roman", 12))
        self.decodebutton.pack(pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE WINDOW", self.stop)
        self.win.mainloop()
        pass

    # Write text to the chat textbox
    def write(self):
        message = f"{self.alias}: {self.inputarea.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.inputarea.delete('1.0', 'end')
        pass

    # Create public keys for DH secret sharing
    def pubkeys(self):
        p = self.dhP.get()
        g = self.dhG.get()
        a = int(p)
        b = int(g)
        num = self.dhinput.get('1.0', 'end')
        numkeys = int(num)
        pubkeys = []
        secrets = []
        bundle = []
        i = 0
        while i < numkeys:
            rpk = int.from_bytes(os.urandom(1), "big")
            secrets.append(rpk)
            pubk = (b**rpk) % a
            pubkeys.append(pubk)
            i += 1
        # list is secrets THEN public keys
        bundle.append(secrets)
        bundle.append(pubkeys)
        self.dharea.config(state='normal')
        self.dharea.delete('1.0', 'end')
        self.dharea.insert('end', "Secret: ")
        self.dharea.insert('end', bundle[0])
        self.dharea.insert('end', " Public Keys:")
        self.dharea.insert('end', bundle[1])
        self.dharea.yview('end')
        self.dharea.config(state='disabled')
        pass

    # Creates private keys for DH secret sharing
    def privkeys(self):
        p = self.dhP.get()
        a = int(p)
        pub = self.dhinput2.get('1.0', 'end')
        publickeys = pub.split()
        secretlist = self.dhinput3.get('1.0', 'end')
        secrets = secretlist.split()
        shskeys = []
        y = len(publickeys)
        j = 0
        while j < y:
            privkexp = int(secrets[j])
            pubk = int(publickeys[j])
            sharedsecret = (pubk ** privkexp) % a
            shskeys.append(sharedsecret)
            j += 1
        self.dharea.config(state='normal')
        self.dharea.delete('1.0', 'end')
        self.dharea.insert('end', shskeys)
        self.dharea.yview('end')
        self.dharea.config(state='disabled')

    def splitString(self, message):
        return[char for char in message]
        pass


    def numChars(self):
        line = self.dhinput.get('1.0', 'end')
        linechars = self.splitString(line)
        i = 0
        while i < (len(linechars) - 1):
            i += 1
        self.dharea.config(state='normal')
        self.dharea.delete('1.0', 'end')
        self.dharea.insert('end', i)
        self.dharea.yview('end')
        self.dharea.config(state='disabled')
        pass


    def encode(self):
        message = self.encodeinput.get('1.0', 'end')
        msg = self.splitString(message)
        key = self.dhinput3.get('1.0', 'end')
        key = key.split()
        alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', ' ']
        msgtoint = []
        keylist = []
        encodedmessage = []
        for k in key:
            keylist.append(int(k))
        for item in msg:
            for letter in alph:
                if(item == letter):
                    msgtoint.append(alph.index(letter))
        iterate = 0
        final = len(msg) - 1
        while iterate < final:
            a = msgtoint[iterate]
            b = keylist[iterate]
            sum = (a + b) % 27
            encodedmessage.append(sum)
            iterate += 1
        self.dharea.config(state='normal')
        self.dharea.delete('1.0', 'end')
        self.dharea.insert('end', encodedmessage)
        self.dharea.yview('end')
        self.dharea.config(state='disabled')
        pass


    def decode(self):
        message = self.decodeinput.get('1.0', 'end')
        msg = message.split()
        key = self.dhinput3.get('1.0', 'end')
        keylist = key.split()

        alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', ' ']
        msgints = []
        keylistints = []
        decodedmessage = []
        msgtostring = []
        x = len(msg)
        y = 0
        for item in msg:
            item = int(item)
            msgints.append(item)
        for keys in keylist:
            keys = int(keys)
            keylistints.append(keys)
        while y < x:
            c = msgints[y]
            d = keylistints[y]
            e = c - d
            if (e < 0):
                e += 27
            decodedmessage.append(e)
            y += 1
        for item in decodedmessage:
            for letter in alph:
                if(item == (alph.index(letter))):
                    msgtostring.append(letter)
        self.dharea.config(state='normal')
        self.dharea.delete('1.0', 'end')
        self.dharea.insert('end', msgtostring)
        self.dharea.yview('end')
        self.dharea.config(state='disabled')
        pass

    def deletePads(self):
        pass

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'ALIAS':
                    self.sock.send(self.alias.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("An Error Occured")
                self.sock.close()
                break




if __name__ == "__main__":
    HOST = '127.0.0.1'
    Socket = 123456

    HOST = input("Please enter host address")
    if (HOST == ''):
        HOST = '127.0.0.1'
        print("Host is localhost")

    Socket = input("Please enter port number")
    if (Socket == ''):
        Socket = int('12345')
        print("Port Number is 12345")
    else:
        Socket = int(Socket)

    client = client(HOST, Socket)



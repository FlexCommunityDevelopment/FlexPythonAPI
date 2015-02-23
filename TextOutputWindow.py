from Tkinter import *
import ScrolledText
import threading
import Queue

class TextOutputWindow(threading.Thread):

    def ShutDown(self):
        return self.shutDown

    def ShutDown(self, value):
        self.shutDown = value
        
    def __init__(self, func):
        self.shutDown = func
        self.quit = 0
        self.clear = 0
        self.queue = Queue.Queue()
        threading.Thread.__init__(self)
        self.root = Tk()
        self.root.title("FlexRadio Output")
        self.start()
        self.root.after(100, self.periodicCall)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.quit_cb)
        self.text = ScrolledText.ScrolledText(self.root)
        self.text.pack(expand=YES, fill=BOTH)
        self.root.mainloop()

    def periodicCall(self):
        if self.quit:
            self.root.quit()
        else:
            if self.clear:
                self.clear = 0
                self.text.delete('1.0', END)
            while self.queue.qsize():
                try:
                    msg = self.queue.get()
                    self.text.insert(END, msg)
                    self.text.see(END)
                except Queuy.Empty:
                    pass
            self.root.after(100, self.periodicCall)

    def quit_cb(self):        
        print('shutting down window...')
        while self.queue.qsize():
            try:
                self.queue.get()
            except Queuy.Empty:
                pass
                
        if self.shutDown != None:        
            self.shutDown()
            
        self.root.quit()

    def add(self, message):
        self.queue.put(message + '\n')

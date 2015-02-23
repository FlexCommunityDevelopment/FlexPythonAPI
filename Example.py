import clr
import binascii
import time
clr.AddReference("FlexLib")
clr.AddReference("Flex.UiWpfFramework")
clr.AddReference("System.Reflection")
from CLR.System import Type
from Flex.UiWpfFramework.Mvvm import ObservableObject
from Flex.Smoothlake.FlexLib import IQStream
from Flex.Smoothlake.FlexLib import API
from Flex.Smoothlake.FlexLib import Panadapter
from TextOutputWindow import TextOutputWindow
from System.Windows import Size
from System.Reflection import BindingFlags
 
# ----------------------------------------
# ----- API Event Handlers ---------------
# ----------------------------------------

rig = None
pa = None
iq = None
fall = None
maxPans = None

iqReceived = 0
panReceived = 0
fallReceived = 0

daxIQChannel = 1
panCenterFreq = 7.204
panAntenna = 'ANT1'
panBand = '40'

def RadioAdded(radio):
    global rig
    global maxPans
    
    rig = radio

    msg_win.add('Radio Added: ' + radio.IP.ToString())

    rig.MessageReceived += MessageReceived
    rig.PropertyChanged += radio_PropertyChanged
    rig.IQStreamAdded += IQStreamAdded
    rig.PanadapterAdded += PanadapterAdded
    rig.SliceAdded += SliceAdded
 
    if rig.Model == 'FLEX-6300':
        maxPans = 2
    elif rig.Model == 'FLEX-6500':
        maxPans = 4
    elif rig.Model == 'FLEX-6700':
        maxPans = 8
    else:
        maxPans = 2
  
    msg_win.add('Radio Model: ' + rig.Model)
    msg_win.add('Max panadapters: ' + str(maxPans))
  
def RadioRemoved(radio):
    msg_win.add('Radio Removed: ' + radio.IP.ToString())

# ----------------------------------------
# ----- Radio Event Handlers -------------
# ----------------------------------------

def MessageReceived(severity, msg):
    msg_win.add('Message: ' + msg)

def SliceAdded(slice):
    msg_win.add('Slice added Index: %s, Freq: %s' % (str(slice.Index), str(slice.Freq)))
    
def PanadapterAdded(panadapter, waterfall):
    global pa
    global rig
    global iq
    global fall
    
    msg_win.add('Panadapter added: ' + str(panadapter.StreamID))  
    
    fall = waterfall
    
    fall.DataReady += fall_DataReady
    
    pa = panadapter;

    pa.DataReady += pan_DataReady;
    pa.PropertyChanged += pan_PropertyChanged;

    pa.DAXIQChannel = daxIQChannel
    pa.Band = panBand
    pa.CenterFreq = panCenterFreq   #Randome frequency selected.
    pa.RXAnt = panAntenna
    
    #Size seems to be important as without it, you won't receive any pan or waterfall data ready events.  Makese sense since the waterfall would be zero in size.
    pa.Size = Size(400.0, 100.0)
    pa.RequestPanadapterFromRadio()
    
    iq = rig.CreateIQStream(daxIQChannel)
    iq.Pan = pa
    iq.DataReady += iq_DataReady
    iq.RequestIQStreamFromRadio()                

def pan_DataReady(panadapter, data):
    global panReceived
    
    panReceived += 1
    if panReceived % 100 == 0:  #Print every so often
        msg_win.add('Pan Stream Id: %s, Count: %s, length: %s' % (panadapter.StreamID, str(panReceived), str(data.Length)))

def fall_DataReady(waterfall, tile):
    global fallReceived
    
    fallReceived += 1
    if fallReceived % 100 == 0: #Print every so often
        msg_win.add('Fall Stream Id: %s, Count: %s, TimeCode: %s' % (waterfall.StreamID, fallReceived, str(tile.Timecode)))
        
def pan_PropertyChanged(sender, event):
    val = sender.GetType().GetProperty(event.PropertyName, BindingFlags.Public | BindingFlags.Instance | BindingFlags.IgnoreCase).GetValue(sender, None);
    #msg_win.add('PA Change: %s Value: %s' % (event.PropertyName,val))
    
def radio_PropertyChanged(radio, event):
    global maxPans
    val = radio.GetType().GetProperty(event.PropertyName, BindingFlags.Public | BindingFlags.Instance | BindingFlags.IgnoreCase).GetValue(radio, None);
    #msg_win.add('Change: %s Value: %s Type: %s' % (event.PropertyName,val, type(val).__name__))
        
    if type(val) is unicode:
        val = val.strip(' \t\n\r\0')    #Noticed radio Status property value had trailing nulls for some reason - this will clean them up.
    
    if event.PropertyName == 'Status' and val == 'Available':
        msg_win.add('Connecting...')
        radio.Connect()
    
    elif event.PropertyName == 'PanadaptersRemaining' and val == maxPans:   #For this example there may be no existing pans
        msg_win.add('Requesting panfall...')
        radio.RequestPanafall()  
        
    elif event.PropertyName == 'Nickname':
        msg_win.add('Radio Name: ' + val)
    
def IQStreamAdded(stream):
    msg_win.add('IQ Stream Added, Stream ID: ' + str(stream.StreamID))
    
# ----------------------------------------
# ----- Panadapter Event Handlers --------
# ----------------------------------------

def iq_DataReady(stream, data):
    global iqReceived
    
    iqReceived += 1
    if iqReceived % 500 == 0:   #Print every so often
        msg_win.add('Stream Id: %s, Count: %s, length: %s, BytesPerSecond: %s' % (stream.StreamID, str(iqReceived), str(data.Length), str(stream.BytesPerSecFromRadio)))
         
# ----------------------------------------
# ----- main -----------------------------
# ----------------------------------------

def Quit():
    #It seams that if some thread is still hanging around it may cause this excpetion: Fatal Python error: PyImport_GetModuleDict: no module dictionary!
    #I don't know what to do about it - this code to clean up event handlers maybe helped?
    global pa
    global iq
    global rig
    
    print('cleaning up connections...')
    
    iq.DataReady -= iq_DataReady
    iq.Close()
    iq = None
    pa.DataReady -= pan_DataReady
    pa.Close(True)
    pa = None
    
    rig.PropertyChanged -= radio_PropertyChanged
    rig.MessageReceived -= MessageReceived
    rig.IQStreamAdded -= IQStreamAdded
    rig.PanadapterAdded -= PanadapterAdded
    rig.SliceAdded -= SliceAdded
    rig.Disconnect()

    import sys
    
    print('Exit')
    sys.exit(0)
    
if __name__ == '__main__':

    inval = raw_input('hit enter to start - your chance to attach a debugger!')
    
    msg_win = TextOutputWindow(Quit)
    
    msg_win.add('Initializing')
     
    API.ProgramName = "Python"
    API.RadioAdded += RadioAdded
    API.RadioRemoved += RadioRemoved
    API.Init()
    

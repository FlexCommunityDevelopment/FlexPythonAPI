# FlexPythonAPI
Collaboration space for working on Flex Radio Python code

*****************************************************************************************
***** This space is not managed by or represented by the Flex Radio Systems company *****
*****************************************************************************************

This is basically a copy of some Python code from Mark Erbaugh via the Flex Community site.  I've run with it and have added support
for the radio IQ stream, pan stream, and waterfall stream.  It assumes there are no pan adapters in use on the radio - I do not recommend you
run this Python code while an instance of Smart SDR is running as I'm seeing some confusion of stream IDs when this is done - no doubt
due to my lack of understanding of how the radio supports multiple clients.

On my initial attempt to get this code to work I had to get the source for pythonnet from: https://github.com/pythonnet/pythonnet.git
I built it on a laptop running Windows 8.1 Pro with the Windows 8.1 SDK installed.  This was necessary because the existing binaries
for download on the pythonnet site have an old bug that make it incompatible with PCs running .Net 4.5.  The bug was fixed and checked into
this git repo so you should have no trouble if you get and build it.

I am *very* new to Python coding - have learned a bit while working on this code so my apologies for the poor syntax, lack of comments
and etc etc.  I am looking for a Python IDE that would make coding in this environment easier - I am spoiled by the Intelisense in
Visual Studio along with the other coding tools inclding a good Python debugger.  I did my debugging by adding an input statement before
the Python code runs and then attach Visual Studio debugger but this is good for debugging pyhonnet and not really debugging the python code.

I hope to learn from anyone deciding to join this group!

Cheers

Larry
N7BCP/HB9EYQ
Basel Switzerland

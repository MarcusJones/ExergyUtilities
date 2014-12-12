# ExergyUtilities
# Copyright (c) 2010, B. Marcus Jones <>
# All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The :mod:`xx` module 
"""

from __future__ import division    

#===============================================================================
# Set up
#===============================================================================
# Standard:


from config import *

import logging.config
import unittest

from exergy_frame.tests.utility_inspect import get_self, get_parent, listObject
import wx
from utility_pathOLD import filter_files_dir

#===============================================================================
# Code
#===============================================================================
def simple_yes_no(question="Question; Yes or No?"):
    app = wx.PySimpleApp()
    retCode = wx.MessageBox(question, "", wx.YES|wx.NO)
    if (retCode == 2):
        return True
    else:
        return False  


class MyClass(object):
    """This class does something for someone. 
    """
    def __init__(self, aVariable): 
        pass

class runDirectory(wx.Frame):
    """
    Does *something* with a directory
    Pass in the something as a function
    """
    
    #----------------------------------------------------------------------
    def __init__(self, dirName = "c:", fileName=".", extensionSearch = "html$", runFunc = None):
        
        
        self.runFunction = runFunc
        self.dirName = dirName
        self.extensionSearch = extensionSearch
        self.fileName = fileName
        
        self.update()
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        # Start GIU
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "File and Folder Dialogs Tutorial")
        self.panel = wx.Panel(self, -1)
        
        # Test
        self.t1 = wx.TextCtrl(self.panel, wx.ID_ANY, "Test it out and see")
        #wx.CallAfter(t1.SetInsertionPoint, 0)        
        box.Add(self.t1, 0, wx.EXPAND)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.t1)
        self.t1.Bind(wx.EVT_CHAR, self.EvtChar)
        
        # Text
        title = wx.StaticText(self.panel, wx.ID_ANY, 'Current directory')
        box.Add(title, 0, wx.EXPAND)
        
        #print self.dirName
        # Text control box, shows current dir
        self.textBox1 = wx.TextCtrl(self.panel, wx.ID_ANY, "{}".format(self.dirName) )
        box.Add(self.textBox1, 0, wx.EXPAND)

        # Text
        title = wx.StaticText(self.panel, wx.ID_ANY, 'Extension')
        box.Add(title, 0, wx.EXPAND)

        # Text control box, shows current extension
        self.textBox2 = wx.TextCtrl(self.panel, wx.ID_ANY, self.extensionSearch)
        self.textBox2.Bind(wx.EVT_KEY_DOWN, self.change_ctrl_ext)
        
        self.Bind(wx.EVT_TEXT, self.EvtText, self.t1)
        self.t1.Bind(wx.EVT_CHAR, self.EvtChar)        
        box.Add(self.textBox2, 0, wx.EXPAND)
        
        # Change dir
        self.dirDlgBtn = wx.Button(self.panel, label="Change directory")
        self.dirDlgBtn.Bind(wx.EVT_BUTTON, self.onDir)
        box.Add(self.dirDlgBtn, flag=wx.LEFT, border=10)
        
        # Run        
        self.runButton = wx.Button(self.panel, -1, 'Run {}'.format("Placeholder function name"))
        self.runButton.Bind(wx.EVT_BUTTON, self.onRun)
        box.Add(self.runButton, 0, wx.EXPAND)
        
        # List
        self.listBox1 = wx.ListBox(self.panel, -1,choices=self.filesList)
        box.Add(self.listBox1, 0, wx.EXPAND)

        #self.listBox1 = wx.ListBox(self.panel,choices=[], id = wx.ID_ANY,name='listBox1', parent=self,style=0)
        #self.listBox1.SetBackgroundColour(wx.Colour(255, 255, 128))
        #self.listBox1.Bind(wx.EVT_LISTBOX, self.OnListBox1Listbox,
        #id=wxID_FRAME1LISTBOX1)        
        
        # Finalize form
        self.panel.SetSizer(box)
        self.Centre()
        

    def update(self):
        # Get files
        self.filesList =  filter_files_dir(self.dirName,self.fileName,self.extensionSearch)
        print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)
        #self.lbox.SetItems(self.choices)
        
    def EvtText(self, event):
        print "Hit {} - {}".format(whoami(), event.GetString())
        self.update()        
        #self.log.WriteText('EvtText: %s\n' % event.GetString())
        #print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)

    def EvtTextEnter(self, event):
        #self.log.WriteText('EvtTextEnter\n')
        print "Hit {}; {}".format(whoami(), event.GetString())
        self.update()        
        #print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)
        
        #event.Skip()

    def EvtChar(self, event):
        print "Hit {}".format(whoami())
        self.update()
        #self.log.WriteText('EvtChar: %d\n' % event.GetKeyCode())
        #print "Update: dir {}, ext {} ".format(self.dirName, self.extensionSearch)
        event.Skip()


        
    def change_ctrl_ext(self,event):
        print "Hit {}".format(whoami())
        self.update()
             
    def onRun(self, event):
        logging.debug("Run function {}".format(self.dirName))
        print "Hit {}".format(whoami())
        self.runFunction(self.dirName)
        self.update()
        
    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        
        if dlg.ShowModal() == wx.ID_OK:
            self.dirName = dlg.GetPath()
            logging.debug("Selected Dir: {}".format(self.dirName))
            self.textBox1.ChangeValue(self.dirName)
            
        dlg.Destroy()
        
        self.update()
        
        
def YesNoOLD(parent, question, caption = 'Yes or no?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result

def simpleYesNo(question="Question; Yes or No?"):
    print wx
    print dir(wx)
    
    app = wx.PySimpleApp()
    retCode = wx.MessageBox(question, "", wx.YES|wx.NO)
    if (retCode == 2):
        return True
    else:
        return False  
         




class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self, startingDir = "c:"):
        
        self.dirName = startingDir
        
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "File and Folder Dialogs Tutorial")
        self.panel = wx.Panel(self, -1)
        
        
        
        box = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self.panel, wx.ID_ANY, 'Current directory')
        box.Add(title, 0, wx.EXPAND)
        
        
        self.textBox1 = wx.TextCtrl(self.panel, wx.ID_ANY, self.dirName )
        box.Add(self.textBox1, 0, wx.EXPAND)
        

        box.Add(wx.Button(self.panel, -1, 'Button2'), 0, wx.EXPAND)
        
        box.Add(wx.Button(self.panel, -1, 'Button3'), 0, wx.ALIGN_CENTER)
        
        #self.onDir = "asdf"
        self.dirDlgBtn = wx.Button(self.panel, label="Show DirDialog")
        self.dirDlgBtn.Bind(wx.EVT_BUTTON, self.onDir)
        box.Add(self.dirDlgBtn, flag=wx.LEFT, border=10)

        self.panel.SetSizer(box)
        self.Centre()
        
    #- onDir ---------------------------------------------------------------------
    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        
        if dlg.ShowModal() == wx.ID_OK:
            self.dirName = dlg.GetPath()
            logging.debug("Selected Dir: {}".format(self.dirName))
            self.textBox1.ChangeValue(self.dirName)
            
        dlg.Destroy()

def runDirFilter(runFunction):

        
    app = wx.App(False)
    dirName = "C:\Dropbox\BREEAM ENE 5 Results1\\"
    
    
    frame = runDirectory(dirName = "c:", fileName=".", extensionSearch = "html$", runFunc =runFunction)
    
    frame.Show()
    app.MainLoop()

def YesNoOLD(parent, question, caption = 'Yes or no?'):
    dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result

def simpleYesNo(question="Question; Yes or No?"):
    print wx
    print dir(wx)
    
    app = wx.PySimpleApp()
    retCode = wx.MessageBox(question, "", wx.YES|wx.NO)
    if (retCode == 2):
        return True
    else:
        return False  

def check_path(f):
    print(f)
    if path_exists(f):
        if simple_yes_no("Delete file {}?".format(f)):
            os.remove(f)
        else:
            pass

#===============================================================================
#---Simple text
#===============================================================================

class MyFrame(wx.Frame):
    
    def set_text(self, inputtext):
        self.text = inputtext
        
    def get_text(self):
        return(self.text)
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(320, 350))

        #self.text = "TESTING"
        panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, self.get_text(), (45, 25), style=wx.ALIGN_CENTRE)
        #wx.StaticText(panel, -1, lyrics2, (45, 190), style=wx.ALIGN_CENTRE)
        #wx.MessageBox('Continue?', "", wx.YES|wx.NO)
        #wx.Button(self, 1, 'Ok', (90, 185), (60, -1))
        #retCode = wx.MessageBox('Continue?', "", wx.YES|wx.NO)
        #if (retCode == 2):
        #    return True
        #else:
        #    return False  
        self.Centre()


class MyTextApp(wx.App):
    def OnInit(self):
        #print(text)
        #raise
        frame = MyFrame(None, -1, 'statictext.py')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
    

def simple_text(input_text):
    app = MyTextApp(0)
    #print(app)
    app.set_text(input_text)
        #s#elf.text = inputtext
    #app.text = 'APPLES'
    #raise
    app.MainLoop()    

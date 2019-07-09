
import kivy
import sys

sys.path.append("./src")

from db import *

kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

# Load the file written by kivy lang to describe the windows' exterior.
Builder.load_file('conf/scheme.kv')

class menu(Screen):
  '''
    The menu screen
  '''
  def __init__(self, **kwargs):
    self.count = 0
    self.db = Database()
    super(menu, self).__init__(**kwargs)
  
  def print(self):
    self.count += 1
    self.ids['testButton'].text = str(self.count) + ' Hits'
  
  def addKV(self):
    key = self.ids['key'].text
    value = self.ids['value'].text
    self.db.addVal(key, value)
    self.db.dump()
    self.ids['value'].text = ''
  
  def findV(self):
    key = self.ids['key'].text
    self.ids['value'].text = str(self.db.find(key))


class vokeybulary(App):
  '''
    The body of vokeybulary
  '''
  def build(self):
    return menu()

if __name__ == "__main__":

  app = vokeybulary()
  app.run()

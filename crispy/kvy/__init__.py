import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.graphics.transformation import Matrix
from kivy.properties import StringProperty
from .functions import *
from .customwidgets import KeyboardWidget
from kivy.config import Config

kivy.require("1.9.0")
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')



#!/usr/bin/python
import os
import sys
import subprocess
import shlex

import pygtk
import gtk
import appindicator

class AppIndicatorExample:
    def __init__(self):
        self.ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon ("indicator-messages-new")
        self.ind.set_icon("distributor-logo")

        self.menu = gtk.Menu()
        
        open_ui_item = gtk.MenuItem("Open UI")
        open_ui_item.connect("activate", open_ui)
        open_ui_item.show()
        self.menu.append(open_ui_item)

        enable_render = gtk.MenuItem("Enable Rendering")
        enable_render.connect("activate", enable)
        enable_render.show()
        self.menu.append(enable_render)

        disable_render = gtk.MenuItem("Disable Rendering")
        disable_render.connect("activate", disable)
        disable_render.show()
        self.menu.append(disable_render)

        quit_item = gtk.MenuItem("Quit")
        quit_item.connect("activate", self.quit)
        quit_item.show()
        self.menu.append(quit_item)
                    
        self.menu.show()

        self.ind.set_menu(self.menu)

    def quit(self, widget, data=None):
        gtk.main_quit()

def disable(*kwargs):
    disable_file = project_path + "/disable_host.py"
    cmd = "python {0}".format(disable_file)
    subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)

def enable(*kwargs):
    enable_file = project_path + "/enable_host.py"
    cmd = "python {0}".format(enable_file)
    subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)

def open_ui(*kwargs):
    control_panel_file = project_path + "/control_panel.py"
    cmd = "python {0}".format(control_panel_file)
    subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.realpath(__file__))
    #App Indicator
    indicator = AppIndicatorExample()
    main()
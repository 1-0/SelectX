#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selectx import _ as _


__plugin_name__ = _(u'SelectX Run Python')
__plugin_menu_caption__ = _(u'Run Python')
__plugin_menu_key__ = 'F5'
__plugin_menu_help__ = _(u'SelectX Run Python Script from current tab')
__plugin_menu_icon__ = '''applications_system'''
__plugin_version__ = '0.1.1'
__plugin_about__ = _(u'Run Python Script from current tab')

def __plugin_init__(self, params_list=[]):
    nnn = __plugin_name__+' '+__plugin_version__
    print nnn
    self.statusBar().showMessage(nnn)

def __plugin_run_function__(self):
    py_run(self)

def py_run(self, py_name=r'./hi.py', run_params=' '):
    import os
    if self:
        py_name = self.cWidget.edit.filePath
    if os.name in ['nt',]:
        status = os.system(r'start cmd /C "python ' + py_name + run_params+r''' &&  pause"''')
    else:
        status = os.system(r'xterm  -e "python ' + py_name + run_params+r''' && echo 'Waiting for press Enter key.' && read"''')
    print 'status - %s'%status
    return status

if __name__ == "__main__":
    py_run(0)

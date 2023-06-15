#!/usr/bin/env python
# -*- coding: utf-8 -*-




from pathlib import Path
from psychopy.localization import _translate
from psychopy.experiment import Param
from psychopy.experiment.routines import BaseStandaloneRoutine






class ViewpixxSetupRoutine(BaseStandaloneRoutine):  
    """A class for the viewpixx device
    """
    categories = ['Responses']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'viewpixx.png'
    tooltip = _translate('Viewpixx: Setup a Viewpixx (Should be the first routine of the experiment)')
    plugin = "psychopy-pixx"
    
    def __init__(self, exp, name='viewpixx', vmode='M16', scanBackLight=False, disabled=False):
        BaseStandaloneRoutine.__init__(self, exp, name = name, disabled=disabled)
        self.url = ""

        self.order += [
            'vmode', 'scanBackLight',
            ]

        # params
        del self.params['stopVal']
        del self.params['stopType']

        msg = _translate("Set to the wanted video mode (do not use Psychopy's gamma linearization for M16 and C48)")
        self.params['vmode'] = Param(
            'M16', valType='str', inputType="choice", categ='Basic',
            allowedVals=['C24', 'M16', 'L48', 'C48'],
            updates='constant',
            hint=msg,
            label=_translate('video mode'))
        msg = _translate("Should the scanning back light be used?")
        self.params['scanBackLight'] = Param(
            False, valType='bool', inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_translate('scanning back light'))
        msg = _translate("Should the scanning back light be used?")
 

    def writeInitCode(self, buff):
        """write the code that will be called for routine initialization"""
        code = "# This is generated by the initialization of the Routine {}\n".format(self.params["name"])
        code += "from pypixxlib.viewpixx import VIEWPixx\n"
        code += "prefs.general['allowGUI'] = False\n"
        code += "pixxdevice = VIEWPixx()\n"
        code += "pixxdevice.setScanningBackLight({})\n".format(self.params["scanBackLight"].val)
        code += "pixxdevice.setVideoMode({})\n".format(self.params["vmode"])
        code += "pixxdevice.updateRegisterCache()\n"
        buff.writeIndented(code)

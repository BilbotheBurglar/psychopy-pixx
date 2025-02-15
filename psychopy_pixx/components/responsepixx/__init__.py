#!/usr/bin/env python
# -*- coding: utf-8 -*-



__all__ = ['ResponsepixxComponent']


from pathlib import Path
from psychopy.localization import _translate, _localized as __localized
from psychopy.experiment.components import (BaseComponent, Param, getInitVals)

_localized = __localized.copy()


_localized.update({'forceEndROutineOnPress': _translate('End Routine on press'),
                   'lights': _translate('Button lights'),
                   'red': _translate('Red button'),
                   'green': _translate('Green button'),
                   'yellow': _translate('Yellow button'),
                   'blue': _translate('Blue button'),
                   'white': _translate('White button'),})

class ResponsepixxComponent(BaseComponent):  # or (VisualComponent)
    """A class for the viewpixx buttonbox responsepixx
    """
    categories = ['Responses']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'responsepixx.png'
    tooltip = _translate('Responsepixx: Record Responsepixx buttonpresses (works only with Viewpixx routine beforehand)')
    plugin = "psychopy-pixx"
    
    def __init__(self, exp, parentName, name='responsepixx',
                 startType='time (s)', startVal=0.0,
                 stopType='duration (s)', stopVal=1.0,
                 startEstim='', durationEstim='', 
                 forceEndROutineOnPress=False, lights=True,
                 red=True, green=True, yellow=True, blue=True, white=True):
        super(ResponsepixxComponent, self).__init__(
            exp, parentName, name=name,
            startType=startType, startVal=startVal,
            stopType=stopType, stopVal=stopVal,
            startEstim=startEstim, durationEstim=durationEstim)

        self.type = 'Responsepixx'
        self.url = "https://github.com/wichmann-lab/psychopy-pixx#responsepixx-button-box"

        self.order += [
            'forceEndROutineOnPress', 'lights', 'red', 'green', 'yellow', 'blue', 'white',
            ]

        # params

        msg = _translate("Should a button press force the end of the routine"
                         " (e.g end the trial)?")
        self.params['forceEndROutineOnPress'] = Param(
            forceEndROutineOnPress, valType="bool", inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_localized['forceEndROutineOnPress'])
        
        msg = _translate("Should the button lights be turned on?")
        self.params['lights'] = Param(
            True, valType='bool', inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_localized['lights'])
        
        msg = _translate("Should the red button be clickable?")
        self.params['red'] = Param(
            True, valType='bool', inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_localized['red'])
        msg = _translate("Should the green button be clickable?")
        self.params['green'] = Param(
            True, valType='bool', inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_localized['green'])
        msg = _translate("Should the yellow button be clickable?")
        self.params['yellow'] = Param(
            True, valType='bool', inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_localized['yellow'])
        msg = _translate("Should the blue button be clickable?")
        self.params['blue'] = Param(
            True, valType='bool', inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_localized['blue'])
        msg = _translate("Should the white button be clickable?")
        self.params['white'] = Param(
            True, valType='bool', inputType="bool", categ='Basic',
            updates='constant',
            hint=msg,
            label=_localized['white'])
        
        
        


    def writeInitCode(self, buff):
        """write the code that will be called at initialization"""
        buff.writeIndented("# This is generated by writeInitCode\n")
        inits = getInitVals(self.params, 'PsychoPy')
        code = ('{} = visual.BaseVisualStim('.format(inits['name']) +
                'win=win, name="{}")\n'.format(inits['name'])
                )
        buff.writeIndentedLines(code)
        code = "from psychopy_pixx.devices import ResponsePixx\n"
        
        clickable = []
        if self.params['red'].val:
            clickable.append('red')
        if self.params['green'].val:
            clickable.append('green')
        if self.params['blue'].val:
            clickable.append('blue')
        if self.params['yellow'].val:
            clickable.append('yellow')
        if self.params['white'].val:
            clickable.append('white')
            
        code += "{}Device = ResponsePixx(pixxdevice, buttons = {}, events = [\'down\'], lights = {})\n".format(self.params['name'], clickable, self.params["lights"])
        buff.writeIndentedLines(code)

    def writeRoutineStartCode(self, buff):
        """Write the code that will be called at the start of the routine
        """
        buff.writeIndented("# This is generated by the writeStartCode\n")
        code = "# starting the responsepixx and setup a python list for storing the button presses\n"
        code += "{}Device.start()\n".format(self.params["name"])
        code += "{}Resp = {{\"name\" : [], \"time\" : [] }}\n".format(self.params["name"])

        buff.writeIndentedLines(code)

    def writeFrameCode(self, buff):
        """Write the code that will be called every frame"""
        buff.writeIndented("# This is generated by the writeFrameCode\n")

        forceEnd = self.params['forceEndROutineOnPress'].val

        #writes an if statement to determine whether to draw etc
        indented = self.writeStartTestCode(buff)
        buff.setIndentLevel(-indented, relative=True)

        
        indented = self.writeStopTestCode(buff)
        if indented:
            buff.setIndentLevel(-indented, relative=True)


        #if STARTED and not FINISHED!
        code = "if {}.status == STARTED:\n".format(self.params["name"])
        buff.writeIndented(code)
        buff.setIndentLevel(1, relative=True)
        code = "prevButtonState = {}Device.getKeys()\n".format(self.params["name"])
        buff.writeIndented(code)
        code = "if len(prevButtonState)>0:\n"
        buff.writeIndented(code)
        buff.setIndentLevel(1, relative=True)
        code = "last_key = prevButtonState[-1]\n"
        buff.writeIndented(code)        
        if forceEnd:
            code ="continueRoutine = False #end routine on click\n"
            buff.writeIndented(code)
            code = "currentLoop.addData(\"{}.key\", last_key[\'name\'])\n".format(self.params["name"])
            buff.writeIndented(code)
            code = "currentLoop.addData(\"{}.rt\", last_key[\'time\'])\n".format(self.params["name"])
            buff.writeIndented(code)
        else:
            code = "{}Resp['name'].append(last_key['name'])\n".format(self.params["name"])
            buff.writeIndented(code)
            code = "{}Resp['time'].append(last_key['time'])\n".format(self.params["name"])
            buff.writeIndented(code)
        buff.setIndentLevel(-2, relative=True)  # to get out of if statement

        


    def writeRoutineEndCode(self, buff):
        """Write the code that will be called at the end of the routine"""
        buff.writeIndented("# This is generated by the writeRoutineEndCode\n")
        code = "{}Device.stop()\n".format(self.params["name"])
        buff.writeIndented(code)
        forceEnd = self.params['forceEndROutineOnPress'].val
        if not forceEnd:
            code = "currentLoop.addData(\"{}.key\", {}Resp[\"name\"])\n".format(self.params["name"], self.params["name"])
            buff.writeIndented(code)
            code = "currentLoop.addData(\"{}.rt\", {}Resp[\"time\"])\n".format(self.params["name"], self.params["name"])
            buff.writeIndented(code)

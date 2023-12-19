#!/usr/bin/env python

import sys

from scripts.common._controls import Controls
from scripts.actions.tuneaction import TuneAction
from scripts.actions.rotatetoaction import RotateToAction
from scripts.actions.frequencyaction import FrequencyAction


from scripts.controllers.rig.rigcontroller import RigController
from scripts.controllers.rotator.rotatorcontroller import RotatorController
from scripts.controllers.tone.tonecontroller import ToneController
from scripts.controllers.tuner.tunercontroller import TunerController
from scripts.common._logger import Logger

def main(argv=None):

    _logger = Logger()
    actionMap = {
        "Tune" : TuneAction,
        "RotateTo" : RotateToAction,
        "Frequency" : FrequencyAction
    }

    if argv is None:
        argv = sys.argv[1:]

    mock = False
    loglevel = 40
    autoTune = False

    action = None
    actionAutoStart = True

    actions = []

    _logger.Info(argv)
    for x in range(len(argv)) :
        _logger.Info(argv[x])

        if argv[x] == "-a" and x + 1 < len(argv) :
            actionEntry = {"action":argv[x + 1], "args" : []}

            y = x + 2
            while y < len(argv) :
                if argv[y].startswith("-") :
                    break
                else :
                    actionEntry["args"].append(argv[y])
                y += 1
            
            actions.append(actionEntry)
            #actions.append({"action":action, "args" : actionArgs})

            _logger.Info("Action = " + str(action))
        elif argv[x] == "-v" :
            loglevel = 99
        elif argv[x] == "-m" :
            mock = True

    _logger.Info("Mock = " + str(mock))

    controls = Controls()
    controls._logger = _logger
    controls._mock =  mock


    for actionEntry in actions :
        ScriptAction = actionMap[actionEntry["action"]]

        if ScriptAction != None :
            ScriptAction(controls, actionEntry["args"], actionAutoStart)
 
if __name__ == "__main__":
    main(sys.argv)
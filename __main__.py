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
    actions = {
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
    actionArgs = []

    _logger.Info(argv)
    for x in range(len(argv)) :
        _logger.Info(argv[x])


        if argv[x] == "-a" and x + 1 < len(argv) :
            _logger.Info("Action")
            action = argv[x + 1]

            _logger.Info("Action = " + str(action))
            #
            #autoTune = True
        elif argv[x] == "-arg" and x + 1 < len(argv) :
            actionArgs.append(argv[x + 1])
        elif argv[x] == "-v" :
            loglevel = 99
        elif argv[x] == "-m" :
            mock = True

    _logger.Info("Mock = " + str(mock))

    ScriptAction = None
    controls = Controls()
    controls.Logger = _logger
    controls.Mock =  mock
    controls.RigControl = RigController(mock)
    controls.TunerControl = TunerController(mock)
    controls.RotatorControl = RotatorController(mock)
    controls.ToneControl = ToneController(mock)


    if action != None :
        ScriptAction = actions[action]

    if ScriptAction != None :
        ScriptAction(controls, actionArgs, actionAutoStart)
 
if __name__ == "__main__":
    main(sys.argv)
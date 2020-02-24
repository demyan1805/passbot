import actions

store = {}

def dispatchEvent(id, currentState, action):
    newState = currentState

    if (action['type'] == actions.done):
        newState['DONE'] = True
        newState['ADD'] = False
        newState['DEL'] = False
        
    elif (action['type'] == actions.add):
        newState['ADD'] = True
        newState['NAME'] = False
        newState['LOGIN'] = False
        newState['PASS'] = False
        newState['DONE'] = False
        
    elif (action['type'] == actions.addName):
        newState['ADD'] = True
        newState['NAME'] = action['data']
        newState['LOGIN'] = False
        newState['PASS'] = False
        newState['DONE'] = False

    elif (action['type'] == actions.addLogin):
        newState['ADD'] = True
        newState['LOGIN'] = action['data']
        newState['PASS'] = False
        newState['DONE'] = False

    elif (action['type'] == actions.addPass):
        newState['ADD'] = False
        newState['PASS'] = action['data']
        newState['DONE'] = False

    elif (action['type'] == actions.delete):
        newState['DEL'] = True
        newState['NAME'] = False
        newState['CONFIRM'] = False
        newState['DONE'] = False
    
    elif (action['type'] == actions.deleteName):
        newState['DEL'] = True
        newState['NAME'] = action['data']
        newState['CONFIRM'] = False
        newState['DONE'] = False

    elif (action['type'] == actions.confirm):
        newState['DEL'] = False
        newState['CONFIRM'] = True
        newState['DONE'] = True

    elif (action['type'] == actions.setActiveMessage):
        newState['ACTIVE_MESSAGE'] = action['data']

    elif (action['type'] == actions.timer):
        newState['TIMER'] = action['data']

    return newState

def createAction(actionType, data = None):
    return {'type': actionType, 'data': data}

def getState(id):
    try:
        state = store[id]
    except:
        state = createInitialState(id)
    return state

def setState(id, action):
    try:
        currentState = store[id]
    except:
        currentState = {}
    newState = dispatchEvent(id, currentState, action)
    store[id] = newState
    return newState

def createInitialState(id):
    initialState = setState(id, createAction(actions.done))
    initialState = setState(id, createAction(actions.setActiveMessage))
    return initialState

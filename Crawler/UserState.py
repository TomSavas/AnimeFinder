from enum import Enum

class UserState(Enum):
	Watching = 1
	Completed = 2
	OnHold = 3
	Dropped = 4
	PlanningToWatch = 5
	NotDefined = 6

def IdentifyKissUserState(userState):
	if userState == 'Watched':
		return UserState.Completed
	elif userState == 'Unwatched':
		return UserState.PlanningToWatch
	else:
		Debug.Log('userState in IdentifyKissUserState', userState, 'is unidentified')
		return UserState.NotDefined 

def IdentifyUserState(userState):
	if userState == 'Completed' :
		return UserState.Completed
	elif userState == 'Watching':
		return UserState.Watching
	elif userState == 'Dropped':
		return UserState.Dropped
	elif userState == 'OnHold' or userState == 'On Hold':
		return UserState.OnHold
	elif userState == 'Planning To Watch' or userState == 'PlanningToWatch':
		return UserState.PlanningToWatch
	elif userState == 'Not Defined' or userState == 'NotDefined':
		return UserState.NotDefined
	else:
		Debug.Log('userState in IdentifyMalUserState', userState, 'is unidentified')
		return UserState.PlanningToWatch 
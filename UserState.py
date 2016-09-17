from enum import Enum

class UserState(Enum):
	Completed = 1
	Watching = 2
	Dropped = 3
	OnHold = 4
	PlanningToWatch = 5

def IdentifyKissUserState(userState):
	if userState == 'Watched':
		return UserState.Completed
	elif userState == 'Unwatched':
		return UserState.PlanningToWatch
	else:
		Debug.Log('userState in IdentifyKissUserState', userState, 'is unidentified')
		return UserState.PlanningToWatch 

def IdentifyMalUserState(userState):
	if userState == 'Completed':
		return UserState.Completed
	elif userState == 'Watching':
		return UserState.Watching
	elif userState == 'Dropped':
		return UserState.Dropped
	elif userState == 'OnHold':
		return UserState.OnHold
	elif userState == 'Planning to Watch':
		return UserState.PlanningToWatch
	else:
		Debug.Log('userState in IdentifyMalUserState', userState, 'is unidentified')
		return UserState.PlanningToWatch 

def UserStateToString(userState):
	if userState == UsetState.Completed:
		return 'Completed'
	elif userState == UsetState.Watching:
		return 'Watching'
	elif userState == UsetState.Dropped:
		return 'Dropped'
	elif userState == UsetState.OnHold:
		return 'On Hold'
	elif userState == UsetState.PlanningToWatch:
		return 'Planning to Watch'
	else:
		Debug.Log('userState in UserStateToString', userState, 'is unidentified')
		return 'Planning to Watch'
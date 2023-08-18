import dbWriter as dbWriter

db = dbWriter.dbWriter('users.json', 'questions.json', 'inviteCode.txt')
INVITE_CODE = 1111

def addQuestion(questionLink: str) -> int:
    db.addQuestion(None, questionLink)
    return 1

def markQuestionAsSolved(userName: str, questionLink: str) -> int:
    return db.markQuestionAsSolved(userName, questionLink)

def listQuestionStats(questionLink) -> []:
    return db.listQuestionStats(questionLink)

def listUserStats(userName) -> []:
    return db.listUserStats(userName)

def listAllQuestions() -> []:
    return db.listAllQuestions()

def listAllUsers(sort=False) -> []:
    return db.listAllUsers(sort)

def listQuestionsAccordingToMostSolved() -> []:
    return db.listQuestionsAccordingToMostSolved()

def checkInviteCode(userName: str, password: str, inviteCode: int) -> int:
    return db.checkInviteCode(userName, password, inviteCode)
    

def login(userName: str, password: str) -> int:
    return db.login(userName, password)


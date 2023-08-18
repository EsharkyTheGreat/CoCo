USERS = {}
QUESTIONS = {}

def addQuestion(userName, questionLink):
    if questionLink not in QUESTIONS:
        QUESTIONS[questionLink] = set()
    QUESTIONS[questionLink].add(userName)

    if userName not in USERS:
        USERS[userName] = set()
        USERS[userName].add(questionLink)

    return 1

def listQuestionStats(questionLink) -> []:
    if questionLink not in QUESTIONS:
        return []
    
    users = []
    for user in QUESTIONS[questionLink]:
        users.append(user)
    return users

def listUserStats(userName) -> []:
    if userName not in USERS:
        return []
    
    questions = []
    for question in USERS[userName]:
        questions.append(question)
    return questions

def listAllQuestions() -> []:
    questions = []
    for question in QUESTIONS:
        questions.append({"question": question, "users": listQuestionStats(question)})
    return questions

def listAllUsers(sort=False) -> []:
    users = []
    for user in USERS:
        users.append({"user": user, "questions": listUserStats(user)})
    if sort:
        users.sort(key=lambda x: len(x["questions"]), reverse=True)
    return users

def listQuestionsAccordingToMostSolved() -> []:
    questions = []
    for question in QUESTIONS:
        questions.append({"question": question, "users": listQuestionStats(question)})
    questions.sort(key=lambda x: len(x["users"]), reverse=True)
    return questions

        
        




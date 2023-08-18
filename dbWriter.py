import json

#open a json file and write the data to it
class dbWriter:
    def __init__(self, userFilename, quesFilename, inviteCodeFileName):
        self.usersFile = userFilename
        self.quesFile = quesFilename
        self.inviteCodeFile = inviteCodeFileName
        with open(self.usersFile, 'w') as f:
            json.dump({}, f)

        with open(self.quesFile, 'w') as f:
            json.dump({}, f)

        with open(self.inviteCodeFile, 'w') as f:
            f.write("1111")    
        
    def addUser(self, userName, password):
        with open(self.usersFile, 'w') as f:
            js = json.load(f)
            js[userName] = {
                "username": userName,
                "password": password,
                "questions": set()
            }
            json.dump(js, f)    

    

    def addQuestion(self, userName, questionLink):
        if userName != None:
            with open(self.usersFile, 'w') as f:
                js = json.load(f)
                js[userName]['questions'].add(questionLink)
                json.dump(js, f)

        with open(self.quesFile, 'w') as f:
            js = json.load(f)
            if questionLink not in js:
                js[questionLink] = {"up": 0, "down": 0,  "solved": set(), "link": questionLink}
            if userName != None:    
                js[questionLink]["solved"].add(userName)
            json.dump(js, f)

    def appendUsers(self, js, questionLink):
        if questionLink not in js:
            return []
        users = []
        for user in js[questionLink]["solved"]:
            users.append(user)
        return users
    
    def appendQuestions(self, js, userName):
        if userName not in js:
            return []
        questions = []
        for question in js[userName]['questions']:
            questions.append(question)
        return questions
    
    def listQuestionStats(self, questionLink):
        with open(self.quesFile, 'r') as f:
            js = json.load(f)
            return self.appendUsers(js, questionLink)
    
    def listUserStats(self, userName):
        with open(self.usersFile, 'r') as f:
            js = json.load(f)
            return self.appendQuestions(js, userName)
            

    def listAllQuestions(self):
        with open(self.quesFile, 'r') as f:
            js = json.load(f)
            questions = []
            for question in js:
                questions.append({"question": question, "users": self.appendUsers(js, question)})
            return questions

    def listAllUsers(self, sort=False):
        with open(self.usersFile, 'r') as f:
            js = json.load(f)
            users = []
            for user in js:
                users.append({"username": user, "questions": self.appendQuestions(js, user)})
            if sort:
                users.sort(key=lambda x: len(x["questions"]), reverse=True)
            return users
    
    def listQuestionsAccordingToMostSolved(self):
        questions = self.listAllQuestions()
        questions.sort(key=lambda x: len(x["users"]), reverse=True)
        return questions
    
    def checkInviteCode(self, userName, password, inviteCode):
        with open(self.inviteCodeFile, 'r') as f:
            
            code = f.read()
            if inviteCode == int(code):
                self.addUser(userName, password)
                
                with open(self.usersFile, 'r') as f:
                    js = json.load(f)
                    if userName in js:
                        return 0
                    else:
                        return inviteCode + 1
            else:
                return 0

    def login(self, userName, password):
        with open(self.usersFile, 'r') as f:
            js = json.load(f)
            if userName not in js:
                return 0
            
            if js[userName]['password'] != password:
                return 0
            
            return 1
    def markQuestionAsSolved(self, userName, questionLink):
        self.addQuestion(userName, questionLink)
        return 1    
    

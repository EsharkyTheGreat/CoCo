import json

#open a json file and write the data to it
class dbWriter:
    def __init__(self, userFilename, quesFilename, inviteCodeFileName):
        self.usersFile = userFilename
        self.quesFile = quesFilename
        self.inviteCodeFile = inviteCodeFileName
        # with open(self.usersFile, 'w') as f:
        #     json.dump({}, f)

        # with open(self.quesFile, 'w') as f:
        #     json.dump({}, f)

        # with open(self.inviteCodeFile, 'w') as f:
        #     f.write("1111")  
        with open(self.usersFile) as f:
            self.user_data = json.load(f)
        with open(self.quesFile) as f:
            self.ques_data = json.load(f)
        with open(self.inviteCodeFile) as f:
            self.invite_code = int(f.read())
        
    def addUser(self, userName, password):
        # with open(self.usersFile) as f:
        #     js = json.load(f)
        #     js[userName] = {
        #         "username": userName,
        #         "password": password,
        #         "questions": {}
        #     }
        self.user_data[userName] = {
            "username" : userName,
            "password" : password,
            "questions" : {},
            "rating" : 1000
        }
        with open(self.usersFile, 'w') as f:
            json.dump(self.user_data, f)    

    

    def addQuestion(self, userName, questionLink):
        if userName != None:
            # with open(self.usersFile, 'r+') as f:
            #     js = json.load(f)
            #     js[userName]['questions'][questionLink]+=1
            #     json.dump(js, f)
            # if questionLink not in self.user_data[userName]['questions']:
                # self.user_data[userName]['questions'][questionLink] = 0
            self.user_data[userName]['questions'][questionLink] = True

            with open(self.usersFile, 'w') as f:
                json.dump(self.user_data, f)

        # with open(self.quesFile, 'r+') as f:
        #     js = json.load(f)
        #     if questionLink not in js:
        #         js[questionLink] = {"up": 0, "down": 0,  "solved": {}, "link": questionLink}
        #     if userName != None:    
        #         js[questionLink]["solved"][userName]+=1
        #     json.dump(js, f)
        with open(self.quesFile, "w") as f:
            if questionLink not in self.ques_data:
                self.ques_data[questionLink] = {"up": {}, "down": {},  "solved": {}, "link": questionLink}
            if userName != None:
                # if userName not in self.ques_data[questionLink]["solved"]:
                    # self.ques_data[questionLink]["solved"][userName] = 0    
                self.ques_data[questionLink]["solved"][userName] = True
            json.dump(self.ques_data, f)

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
        # with open(self.quesFile, 'r') as f:
        #     js = json.load(f)
        #     return self.appendUsers(js, questionLink)
        # return self.appendUsers(self.ques_data,questionLink)
        # res = {i:self.ques_data[i] for i in self.ques.keys()}
        return self.ques_data[questionLink]
    
    def listUserStats(self, userName):
        # with open(self.usersFile, 'r') as f:
        #     js = json.load(f)
        #     return self.appendQuestions(js, userName)
        # return self.appendQuestions(self.user_data, userName)
        res = {}
        res["username"] = userName
        res['rating'] = self.user_data[userName]["rating"]
        res['questions'] = [x for x in self.user_data[userName]["questions"] if self.user_data[userName]["questions"][x]]
        return res
    
    def listAllQuestions(self):
        # with open(self.quesFile, 'r') as f:
        #     js = json.load(f)
        js = self.ques_data
        questions = []
        # for question in js:
            # questions.append({"question": question, "users": self.appendUsers(js, question)})
        for question in js.values():
            questions.append(question)
        return questions


    def listAllUsers(self, sort=False):
        # with open(self.usersFile, 'r') as f:
            # js = json.load(f)
        js = self.user_data
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
        # with open(self.inviteCodeFile, 'r') as f:
            # code = f.read()
            if inviteCode == self.invite_code:
                
                # f = open(self.usersFile, 'r')
                # js = json.load(f)
                if userName in self.user_data:
                    # f.close()
                    return 0
                else:
                    # f.close()
                    self.addUser(userName, password)
                    # f = open(self.inviteCodeFile, "w")
                    # f.write(str(inviteCode+1))
                    # f.close()
                    self.invite_code += 1
                    with open(self.inviteCodeFile,"w") as f:
                        f.write(str(self.invite_code))
                    return inviteCode + 1
            else:
                return 0

    def login(self, userName, password):
        # with open(self.usersFile, 'r') as f:
            # js = json.load(f)
            js = self.user_data
            if userName not in js:
                return 0
            
            if js[userName]['password'] != password:
                return 0
            
            return 1
    def markQuestionAsSolved(self, userName, questionLink):
        self.addQuestion(userName, questionLink)
        return 1    
    def unmark(self,userName,questionLink):
        self.user_data[userName]["questions"][questionLink] = False
        with open(self.usersFile,"w") as f:
            json.dump(self.user_data, f)
        self.ques_data[questionLink]["solved"][userName] = False
        with open(self.quesFile,"w") as f:
            json.dump(self.ques_data, f)
    
    def upvote(self,userName,questionLink):
        self.ques_data[questionLink]["up"][userName] = True
        with open(self.quesFile, "w") as f:
            json.dump(self.ques_data, f)

    def downvote(self,userName,questionLink):
        self.ques_data[questionLink]["up"][userName] = False
        with open(self.quesFile, "w") as f:
            json.dump(self.ques_data, f)

    def toprated(self):
        questions = self.listAllQuestions()
        questions.sort(key=lambda x: x["up"]-x["down"], reverse=True)
        return questions
    
    def topsolved(self):
        questions = self.listAllQuestions()
        questions.sort(key=lambda x: x["up"]-x["down"],reverse=True)
        res = []
        for q in questions:
            for x in q["solved"]:
                if q["solved"][x]:
                    res.append(q)
                    break
        return res
    def topunsolved(self):
        questions = self.listAllQuestions()
        questions.sort(key=lambda x: x["up"]-x["down"],reverse=True)
        res = []
        for q in questions:
            for x in q["solved"]:
                if not q["solved"][x]:
                    res.append(q)
                    break
        return res
    
    def topusers(self):
        users = [{"username":x["username"],"rating":x["rating"]} for x in self.user_data.values()].sort(lambda x: x["rating"],reverse=True)
        return users


class Banner:
    greet = "Welcome to CoCo \n1. Login \n2. Register\nEnter Q to quit"
    error = "Unable to understand input"
    caret = '> '
    username = "Username: "
    password = "password: "
    invite = "invite: "
    failed_login = "\033[0;31mUnable to Login\033[0m"
    failed_keyword = "\033[0;31mInvalid keyword\033[0m"
    Help = "Help coming soon!"
    welcome = "Welcome to Collector Codes!!\nYour invite code is"

    def red(string):
        print("\033[0;31m{}\033[0m".format(string))

    def green(string):
        print("\033[0;32m{}\033[0m".format(string))

from requests import get,post
#url = 'http://192.168.203.204:5000'
url = 'http://172.20.19.236:7652'
#-------------------- POST --------------------#
def add(token,chunks):
    x = post(url+"/add", json={"token":token,"question":chunks[1]}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
    else:
        Banner.green('success')

def mark(token,chunks):
    x = post(url+"/mark", json={"token":token,"question":chunks[1]}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
    else:
        Banner.green('success')

def unmark(token,chunks):
    x = post(url+"/unmark", json={"token":token,"question":chunks[1]}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
    else:
        Banner.green('success')

def up(token,chunks):
    x = post(url+"/up", json={"token":token,"question":chunks[1]}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
    else:
        Banner.green('success')

def down(token,chunks):
    x = post(url+"/down", json={"token":token,"question":chunks[1]}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
    else:
        Banner.green('success')
def stats(token,chunks):
    if chunks[1] not in ["user", "question"]:
        print(Banner.failed_keyword)
        return
    if chunk[1] == 'user':
        x = post(url+"/leaderboard/"+chunks[1], json={"token":token,"username":chunks[2]}).json()
    else:
        x = post(url+"/leaderboard/"+chunks[1], json={"token":token,"username":chunks[2]}).json()
            
    if x['status'] != "success":
        Banner.red(x['message'])
        return
    if chunks[1] == 'user':

#-------------------- GET ---------------------#

def qlist(token,chunks):
    x = get(url+"/list", json={"token":token}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
        return
    print("LINKS\t\tUPVOTES\tDOWNVOTES")
    for i in x['questions']:
        print("{}\t\t{}\t{}".format(i['question'],i['up'],i['down']))

def leaderboard(token,chunks):
    x = get(url+"/leaderboard", json={"token":token}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
        return
    print("USERNAME\t\tSOLVED")
    for i in x['leaderboard']:
        print("{}\t\t{}".format(i['username'],len(i['questions'])))



def top(token,chunks):
    if chunks[1] not in ["rated", "solved", "unsolved" , "player"]:
        print(Banner.failed_keyword)
        return
    x = get(url+"/leaderboard", json={"token":token}).json()
    if x['status'] != "success":
        Banner.red(x['message'])
        return
    if chunks[1] == 'player': 
        print("USERNAME\t\tRATING")
        for i in x['users']:
            print("{}\t\t{}".format(i['username'],i['rating']))
    else:
        chunks[1] == 'solved': 
        print("LINKS\t\tUPVOTES\tDOWNVOTES")
        for i in x['questions']:
            print("{}\t\t{}\t{}".format(i['question'],i['up'],i['down']))


def Help(token,chunks):
    print(Banner.Help)


keywords = {
        "add":(2,add), 
        "mark":(2,mark),
        "unmark":(2,unmark),
        "list":(1,qlist), 
        "ls":(1,qlist), 
        "leaderboard":(1,leaderboard), 
        "help":(1,Help), 
        "q":(1,),
        "lb":(1,leaderboard),
        "unmark":(2,unmark),
        "stats":(3,stats),
        "top":(2,top),
        "up":(2,up),
        "down":(2,down),
        }

def session(token):
    while True:
        inst = input(Banner.caret)
        inst = inst.strip().lower()
        chunks = inst.split()
        if (chunks[0] not in keywords) or (len(chunks) != keywords[chunks[0]][0]):
            print(Banner.failed_keyword)
            continue
        if(chunks[0] == 'q'): exit(0)
        keywords[chunks[0]][1](token,chunks)

def login():
    username = input(Banner.username)
    password = input(Banner.password)
    x = post(url+"/login", json={"username":username,"password":password}).json()
    if x['status'] != "success": 
        Banner.red(x['message'])
        print(Banner.failed_login)
        return False
    session(x['token'])

def autologin(username,password):
    x =post(url+"/login", json={"username":username,"password":password}).json()
    return x['token']

def register():
    invite = int(input(Banner.invite))
    username = input(Banner.username)
    password = input(Banner.password)
    x = post(url+"/register", json={"username":username,"password":password,"invite":invite}).json()
    if x['status'] != "success": 
        Banner.red(x['message'])
        print(Banner.failed_login)
        return False
    print(Banner.welcome,'\033[0;32m', x['invite'], '\033[0m')
    token = autologin(username,password)
    session(token)


def main():
    print(Banner.greet)
    while True:
        inp = input(Banner.caret)
        inp = inp.strip()
        if(inp == '1'):
            if login(): break
        elif(inp == '2'):
            if register(): break
        elif(inp.lower() == 'q'): exit(0)
        else:
            print(Banner.error)

if __name__ == "__main__":
    main()





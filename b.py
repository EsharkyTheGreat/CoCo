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

from requests import get,post
url = 'http://192.168.203.204:5000'

def add(token,chunks):
    x = post(url+"/add", json={"token":token,"question":chunks[1]}).json()
    print(x)

def qlist(token,chunks):
    x = get(url+"/list", json={"token":token}).json()
    print(x)

def leaderboard(token,chunks):
    x = get(url+"/leaderboard", json={"token":token}).json()
    print(x)

def mark(token,chunks):
    x = post(url+"/mark", json={"token":token,"question":chunks[1]}).json()
    print(x)


keywords = {"add":2, "mark":2, "list":1, "leaderboard":1 , "help":1 , "q":1, }
keyword_to_func = {"add":add, "mark":mark, "list":qlist, "leaderboard":leaderboard}

def session(token):
    while True:
        inst = input(Banner.caret)
        chunks = inst.split()
        if (chunks[0] not in keywords) or (len(chunks) != keywords[chunks[0]]):
            print(Banner.failed_keyword)
            continue
        if(chunks[0] == 'q'): exit(0)
        elif(chunks[0] == 'help'):
            print(Banner.Help)
            continue
        keyword_to_func[chunks[0]](token,chunks)

def login():
    username = input(Banner.username)
    password = input(Banner.password)
    x = post(url+"/login", json={"username":username,"password":password}).json()
    if x['status'] != "ok": 
        print("\033[031;m", x['message'], "\033[031;m", sep="")
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
    if x['status'] != "ok": 
        print("\033[031;m", x['message'], "\033[031;m",sep="")
        print(Banner.failed_login)
        return False
    print(Banner.welcome,'\033[0;32m', x['invite'], '\033[0m')
    token = autologin(username,password)
    session(token)


def main():
    print(Banner.greet)
    while True:
        inp = input(Banner.caret)
        if(inp == '1'):
            if login(): break
        elif(inp == '2'):
            if register(): break
        elif(inp.lower() == 'q'): exit(0)
        else:
            print(Banner.error)

if __name__ == "__main__":
    main()





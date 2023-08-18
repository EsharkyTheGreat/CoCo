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

keywords = {"add":2, "mark":2, "list":1, "leaderboard":1 , "help":1 , "q":1}
def add(token,q):
    x = requests.post(url+"/add", json={"token":token,"question":q}).json()

def list(token,q):
    x = requests.post(url+"/list").json()

def leaderboard(token,q):
    x = requests.get(url+"/leaderboard").json()

def mark(token,q):
    x = requests.post(url+"/mark", json={"token":token,"question":q}).json()


keyword_to_func = {"add":add, "mark":mark, "list":qlist, "leaderboard":leaderboard}

def session(token):
    while True:
        inst = input(Banner.caret)
        chunks = inst.split()
        if (chunks[0] not in keywords) or (len(chunks) != keywords[chunks[0]]):
            print(Banner.failed_keyword)
        if(chunks[0] == 'q'): exit(0)
        elif(chunks[1] == 'help'):
            print(Banner.Help)







from requests import get,post
def login():
    username = input(Banner.username)
    password = input(Banner.password)
    x = requests.post(url+"/login", json={"username":username,"password":password}).json()
    if x.status != "ok": 
        print(Banner.failed_login)
        return False
    session(x.token)

def autologin(username,password):
    x = requests.post(url+"/login", json={"username":username,"password":password}).json()
    return x.token

def register():
    invite = input(Banner.invite)
    username = input(Banner.username)
    password = input(Banner.password)
    x = requests.post(url+"/register", json={"username":username,"password":password,"invite":invite}).json()
    if x.status != "ok": 
        print(Banner.failed_login)
        return False
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





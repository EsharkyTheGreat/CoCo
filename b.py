class Banner:
    greet = "Welcome to CoCo \n1. Login \n2.Register\nEnter Q to quit"
    error = "Unable to understand input"
    caret = '> '
        
def login():
    pass
def register():
    pass

def main():
    print(Banner.greet)
    inp = input(Banner.caret)
    while True:
        if(inp == '1'):
            login()
        elif(inp == '2'):
            register()
        elif(inp.lower == 'q'): exit(0)
        else:
            print(Banner.error)

if __name__ == "__main__":
    main()






from WSUSSL.Shared.action import Action

def main():
    #init
    num,id,vx,vy,w,k,d = 0,0,0,0,0,0,0

    while True: 
        print("This is a debugger tool for testing action purposes")
        print("please select the number that you wanted to modify.")
        print("1. vx 2. vy 3. omega 4. kicker 5. dribbler 6. Done")
        try: 
            match num:
                case 0:
                    while id not in range(1,6):
                        id = int(input ("Please enter a Robot ID:"))
                case 1:
                    vx = float(input("Please enter the value for vx : "))
                case 2:
                    vy = float(input("Please enter the value for vy : "))
                case 3:
                    w = float(input("Please enter the value for omega(w): "))
                case 4:
                    k = 2 
                    while k not in (0,1):
                        print("Please enter the number for kicker operation")
                        k = int(input("0. No  1. Yes"))

                case 5:
                    d = float(input("Please enter dribbler speed"))
                case 6: 
                    new_action = Action(id,vx,vy,w,k,d)
                    print(new_action, "has been created")
                    return new_action
            num = int(input("Please Select an option : "))     
            
        except Exception:
            print("please input the correct values")
            print(Exception)


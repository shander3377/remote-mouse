import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
import autopy




SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
screen_width = None
screen_height = None


mouse = Controller() #storing information from the mouse

def getDeviceSize():
    global screen_height
    global screen_width
    for m in get_monitors(): #Get_monitor gets the x,y and height, width of the monitor
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])


def recv_msg(client_socket):
    global mouse
    while(True):
        try:
            msg = client_socket.recv(2048).decode()
            if msg:
                new_msg = eval(msg)
                if new_msg["data"] == "left_click":
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                elif new_msg["data"] == "right_click":
                    mouse.press(Button.right)
                    mouse.release(Button.right)
                else: #if the user is only trying to change the lcoation of the cursor
                    xpos = new_msg["data"][0]*screen_width
                    ypos = screen_height*(1-(new_msg["data"][1]-0.2)/0.6) 
                    mouse.position = (int(xpos), int(ypos))
        except:
            pass

def acceptConnections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection established with {client_socket} : {addr}")
        thread1 = Thread(target=recv_msg, args=(client_socket))
        thread1.start()       


def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Mouse ***\n")


    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    getDeviceSize()    
    acceptConnections()

setup()

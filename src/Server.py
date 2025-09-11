import socket
import pyttsx3
from colorama import Fore, Style

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.bind(('localhost', 12345))

    print("UDP Server is waiting for data")
    speak("UDP Server is waiting for data")

    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            Operation=data.decode()
            print(Fore.YELLOW + f"Client: the operation is {Operation}" + Style.RESET_ALL) 
            speak(f"Received the operation from client, the operation is {Operation}")

            server_socket.sendto("Send two numbers".encode(), addr)
            print(Fore.BLUE + f"Server: Send two numbers" + Style.RESET_ALL)

            data, addr = server_socket.recvfrom(1024)
            num1 = data.decode()
            if num1.lower() == "exit":
                print(Fore.RED + "Client disconnected." + Style.RESET_ALL)
                speak("Client disconnected")
                continue

            print(Fore.YELLOW + f"Client: the first number is {num1}" + Style.RESET_ALL)
            speak(f"Received the first number from client, the number is {num1}")

            data, addr = server_socket.recvfrom(1024)
            num2 = data.decode()

            if num2.lower() == "exit":
                print(Fore.RED + "Client disconnected." + Style.RESET_ALL)
                speak("Client disconnected")
                continue

            print(Fore.YELLOW + f"Client: the second number is {num2}" + Style.RESET_ALL)
            speak(f"Received the second number from client, the number is {num2}")

            try:
                if Operation.lower()=="addition":
                    result = int(num1) + int(num2)
                elif Operation.lower()=="subtraction":
                    result = int(num1) - int(num2)
                elif Operation.lower()=="multiplication":
                    result = int(num1) * int(num2)
                else:
                    result = int(num1) / int(num2)
                server_socket.sendto(str(result).encode(), addr)
                print(Fore.BLUE + f"Server: The result is {result}" + Style.RESET_ALL)
            except:
                print(Fore.RED + "Invalid input received." + Style.RESET_ALL)
                speak("Invalid input received")
                server_socket.sendto("Error: Invalid input".encode(), addr)

    except socket.error as e:
        print(Fore.RED + f"Socket error: {e}" + Style.RESET_ALL)
        speak("A socket error occurred")
        
    
if __name__ == "__main__":
    server()

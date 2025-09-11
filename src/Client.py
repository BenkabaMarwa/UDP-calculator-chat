
import socket
import pyttsx3
import time
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

def getValidNumber(prompt):
    while True:
        try:
            num = input(prompt)
            if num.lower() == "exit":
                return "exit"
            return str(int(num))
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter an integer." + Style.RESET_ALL)
            speak("Invalid input. Please enter an integer.")

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)

    server_address = ('localhost', 12345)

    print(Fore.GREEN + "Connected to server." + Style.RESET_ALL)
    speak("Connected to server")
    try:
        while True:
            maxAttempts=3
            attempt=0
            while attempt<maxAttempts:
                if attempt==0:
                    speak("Enter the operation (addition, subtraction, multiplication, or division..)")
                    while True:
                        Operation= input("Enter the opperation (addition, subtraction, multiplication, or division)..")
                        valid_operations = ["addition", "subtraction", "multiplication", "division"]
                        if Operation in valid_operations:
                            break
                        else:
                            print(Fore.RED + f"Please enter correct operation (addition, subtraction, multiplication, or division..)"+ Style.RESET_ALL)
                            speak("Please enter correct operation (addition, subtraction, multiplication, or division..)")
                    client_socket.sendto(Operation.encode(), server_address)
                    print(Fore.YELLOW + f"Client: The operation is {Operation}"+ Style.RESET_ALL)

                    message, _ = client_socket.recvfrom(1024)  
                    print(Fore.BLUE + "Server: ", message.decode() + Style.RESET_ALL)
                    speak(f"Received the message from server {message.decode()}")

                    speak("Enter the first number or type exit to quit")
                    num1 = getValidNumber("Enter the first number (or type 'exit' to quit): ")
                    client_socket.sendto(num1.encode(), server_address)
                    if num1.lower() == "exit":
                        print(Fore.RED + "exit" + Style.RESET_ALL)
                        speak("exit")
                        return
                    print(Fore.YELLOW + f"Client: the first number is {num1}" + Style.RESET_ALL)

                    time.sleep(1)
                    speak("Enter the second number or type exit to quit")
                    num2 = getValidNumber("Enter the second number (or type 'exit' to quit): ")

                    while True:
                        if Operation.lower()=="division" and num2=="0":
                            print(Fore.RED + "We can't divide by zero" + Style.RESET_ALL)
                            speak("We can't divide by zero")
                            speak("Enter the second number different from zero (or type 'exit' to quit)")
                            num2 = getValidNumber("Enter the second number different from zero '0'(or type 'exit' to quit)..")               
                        else:
                            break

                    client_socket.sendto(num2.encode(), server_address)
                    if num2.lower() == "exit":
                        print(Fore.RED + "exit" + Style.RESET_ALL)
                        speak("exit")
                        return
                    print(Fore.YELLOW + f"Client: the second number is {num2}" + Style.RESET_ALL)
                else:
                    print(f"Sending numbers to server... (Attempt {attempt + 1})")
                    speak(f"Sending numbers to server. Attempt {attempt + 1}")
                    client_socket.sendto(num1.encode(), server_address)
                    print(Fore.YELLOW + f"Client: the first number is {num1}" + Style.RESET_ALL)
                    time.sleep(1)
                    client_socket.sendto(num2.encode(), server_address)
                    print(Fore.YELLOW + f"Client: the second number is {num2}" + Style.RESET_ALL)

                try:
                    result, _ = client_socket.recvfrom(1024)  
                    print(Fore.BLUE + "Server: The result is", result.decode() + Style.RESET_ALL)
                    speak(f"Received the result from server {result.decode()}")
                    break
                except socket.timeout:
                    attempt += 1
                    print(Fore.RED + "No response from server. Retrying..." + Style.RESET_ALL)
                    speak("No response from server. Retrying...")

            if attempt == maxAttempts:
                print(Fore.RED + "Server did not respond after multiple attempts. Exiting." + Style.RESET_ALL)
                speak("Server did not respond after multiple attempts. Exiting.")

    except socket.error as e:
        print(Fore.RED + f"Socket error: {e}" + Style.RESET_ALL)
        speak("A socket error occurred")

    
    client_socket.close()

if __name__ == "__main__":
    client()

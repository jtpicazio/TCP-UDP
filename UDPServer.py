import socket
import random
import sys

# Static IP and PORT
IP = socket.gethostname()
PORT = 4545


# Check_valid checks the validity of the clients sent equation, if not a valid equation then return False, else True
def check_valid(eq):

    # Check to ensure there exists a proper OC
    if '+' not in eq and '-' not in eq and '*' not in eq and '/' not in eq: return False

    # Check that the equation sent doesn't contain more than 1 OC by checking the length or the array after splitting
    elif (len(eq.split('+')) > 2) or (len(eq.split('-')) > 2) or\
            (len(eq.split('*')) > 2) or (len(eq.split('/')) > 2): return False

    # Check that two numbers exist
    elif ('+' in eq) and (not eq.split('+')[0] or not eq.split('+')[1]): return False
    elif ('-' in eq) and (not eq.split('-')[0] or not eq.split('-')[1]): return False
    elif ('*' in eq) and (not eq.split('*')[0] or not eq.split('*')[1]): return False
    elif ('/' in eq) and (not eq.split('/')[0] or not eq.split('/')[1]): return False

    # Checks to make sure only one specific OC was sent
    elif ('+' in eq and '-' in eq) or ('+' in eq and '*' in eq) or ('+' in eq and '/' in eq) or\
            ('-' in eq and '*' in eq) or ('-' in eq and '/' in eq) or ('*' in eq and '/' in eq): return False

    # Check for non numeric input
    elif ('+' in eq) and (not eq.split('+')[0].isnumeric() or not eq.split('+')[1].isnumeric()): return False
    elif ('-' in eq) and (not eq.split('-')[0].isnumeric() or not eq.split('-')[1].isnumeric()): return False
    elif ('*' in eq) and (not eq.split('*')[0].isnumeric() or not eq.split('*')[1].isnumeric()): return False
    elif ('/' in eq) and (not eq.split('/')[0].isnumeric() or not eq.split('/')[1].isnumeric()): return False

    # Check if division by zero
    elif ('/' in eq) and (eq.split('/')[1] is '0'): return False

    # If all the checks pass then return True = equation is Valid
    else: return True

# calculate() will perform the proper operation specified by the client's OC, first it decides which OC,
#   then it extracts each number from the string and performs the operation. returns the results
def calculate(eq):
    if '+' in eq:
        num1 = int(eq.split('+')[0])
        num2 = int(eq.split('+')[1])
        return num1 + num2
    if '-' in eq:
        num1 = int(eq.split('-')[0])
        num2 = int(eq.split('-')[1])
        return num1 - num2
    if '*' in eq:
        num1 = int(eq.split('*')[0])
        num2 = int(eq.split('*')[1])
        return num1 * num2
    if '/' in eq:
        num1 = int(eq.split('/')[0])
        num2 = int(eq.split('/')[1])
        return num1 / num2

#Start of Server
def main(argv):
    # Check for argument, if none run with 50% drop rate (default)
    if len(argv) == 1: ran_drop = .5
    else: ran_drop = float(argv[1])
    print("Simulate a " + '\033[94m' + str(ran_drop * 100) + '\033[0m' + "% chance of dropping a packet")

    # Creating a Socket
    print("Creating socket for communication")
    sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind created socket to specified port
    print("Binding socket to Port")
    sckt.bind((IP, PORT))

    while True:

        # Wait for message and then store content in data, and ip/port in address
        print("Waiting for a message...")
        data, address = sckt.recvfrom(4096)

        # Decoding the bytes into a string
        received_equation = data.decode("utf-8")
        # " " is included between colors, to prevent color being added to future text with received_equation being empty
        print("Received message: " + '\033[94m' + " "+ received_equation + '\033[0m')

        # Check for quit from User
        if 'quit' in received_equation:
            print("Closing Socket And Shutting Down Server...")
            sckt.close()
            break
        # Simulate argv[1]*100% chance of dropping a packet by not doing anything and looping back to waiting for message
        elif random.random() >= ran_drop:

            # Call check_valid function, returns True xor False
            print("Checking for validity...")
            if check_valid(received_equation) is False:

                # Send answer = -1 and status code 300
                print("Sending a response to client" + '\033[94m' + str(address) + '\033[0m')
                server_message = str(300) + ':' + str(-1)
                sckt.sendto(bytes(server_message, "utf-8"), address)

            else:
                # Calculate answer by calling function calculate
                ans = calculate(received_equation)

                # Send calculated answer and status code 200
                print("Sending a response to client" + '\033[94m' + str(address) + '\033[0m')
                server_message = str(200) + ':' + str(ans)
                sckt.sendto(bytes(server_message, "utf-8"), address)


main(sys.argv)
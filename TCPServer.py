import socket

# Static IP and PORT
IP = socket.gethostname()
PORT = 4545

# check_valid() checks the validity of the clients sent equation, if not a valid equation then return False, else True
def check_valid(eq):
    # Check to ensure there exists a proper OC
    if '+' not in eq and '-' not in eq and '*' not in eq and '/' not in eq: return False

    # Check that the equation sent doesn't contain more than 1 OC by checking the length or the array after splitting
    elif (len(eq.split('+')) > 2) or (len(eq.split('-')) > 2) or \
            (len(eq.split('*')) > 2) or (len(eq.split('/')) > 2): return False

    # Check that two numbers exist
    elif ('+' in eq) and (not eq.split('+')[0] or not eq.split('+')[1]): return False
    elif ('-' in eq) and (not eq.split('-')[0] or not eq.split('-')[1]): return False
    elif ('*' in eq) and (not eq.split('*')[0] or not eq.split('*')[1]): return False
    elif ('/' in eq) and (not eq.split('/')[0] or not eq.split('/')[1]): return False

    # Checks to make sure only one specific OC was sent
    elif ('+' in eq and '-' in eq) or ('+' in eq and '*' in eq) or ('+' in eq and '/' in eq) or \
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

def main():

    # Create a socket
    print("Creating socket for communication")
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind created socket to specified port
    print("Binding socket to Port")
    sckt.bind((IP, PORT))

    # Listen for connections
    print("Listening for connections...")
    sckt.listen(5)

    while True:

        # Make a connection
        print("Waiting for a client to connect with...")
        client_socket, clients_address = sckt.accept()
        print("Connection made with " + '\033[94m' + str(clients_address) + '\033[0m')

        # Receive a message and decode it from bytes to string
        received_equation = client_socket.recv(4096).decode("utf-8")
        print("Received message: " + '\033[94m' + received_equation + '\033[0m')

        # Check for quit from User
        if 'quit' in received_equation:
            print("Closing Connection, Closing Socket, And Shutting Down Server...")
            client_socket.close()
            sckt.close()
            break

        # Call check_valid function, returns True xor False
        print("Checking for validity...")
        if check_valid(received_equation) is False:

            # Couldn't compute equation
            print("Sending a response to client")
            server_message = str(300) + ':' + str(-1)

            # Send answer = -1 and status code 300
            client_socket.send(bytes(server_message, "utf-8"))
        else:
            # Calculate answer by calling function calculate
            print("Sending a response to client")
            ans = calculate(received_equation)
            server_message = str(200) + ':' + str(ans)

            # Send calculated answer and status code 200
            client_socket.send(bytes(server_message, "utf-8"))

        print("Closing connection with client")
        client_socket.close()

main()
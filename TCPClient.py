import socket

# Static IP and PORT
IP = socket.gethostname()
PORT = 4545

def main():

    while True:
        # Create a socket
        print("Creating socket for communication...")
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the Server
        print("Connecting to server: " + str(IP) + ":" + str(PORT))
        sckt.connect((IP, PORT))

        # Receive input from user and remove whitespace
        input_str = input("Enter your simple equation, or enter \"quit\" to close: ").replace(" ", "")

        if not input_str:
            input_str += '0'

        # Check for 'quit' command, if True, then shutdown the server and close this program
        if 'quit' in input_str:
            print("Shutting Down Client And Server...")
            sckt.send(bytes(input_str, "utf-8"))
            print("Closing Socket...")
            sckt.close()
            break

        # Send Equation to Server
        print("Sending client input to Server...")
        sckt.send(bytes(input_str, "utf-8"))

        # Received msg in format "status code:result" so we can split the status code from the result easily
        print("Waiting for response...")
        rec_msg = sckt.recv(4096).decode("utf-8").split(':')

        # If any status code apart from 200 was received then an error occurred, else display the result
        if "200" not in rec_msg[0]: print("Error: Status Code: " + '\033[91m' + rec_msg[0] + '\033[0m')
        else: print("Result of equation is: " + '\033[94m' + rec_msg[1] + '\033[0m' + " Status Code: " + '\033[94m' + rec_msg[0] + '\033[0m')

        print("Closing Socket...")
        sckt.close()

main()
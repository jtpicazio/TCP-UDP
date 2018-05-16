import socket

# Static IP and PORT
IP = socket.gethostname()
PORT = 4545

# Start of client
def main():

    while True:

        # Creating a Socket
        print("Creating socket for communication...")
        sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Receive input from user and remove whitespace
        input_str = input("Enter your simple equation, or enter \"quit\" to close: ").replace(" ", "")

        # Check for 'quit' command, if True, then shutdown the server and close this program
        if 'quit' in input_str:
            print("Shutting Down Client And Server...")
            sckt.sendto(bytes(input_str, "utf-8"), (IP, PORT))
            print("Closing Socket...")
            sckt.close()
            break

        # Delay variable
        d = 0.1

        # Exponential Backoff Loop start
        while d >= 0:
            # Set how long to wait for a timeout
            sckt.settimeout(d)

            # Send msg
            print("Sending equation to " + str(IP) + ":" + str(PORT))
            sckt.sendto(bytes(input_str, "utf-8"), (IP, PORT))

            # Try to receive a msg before d seconds
            try:
                # Received msg in format "status code:result" so we can split the status code from the result easily
                print("Waiting for response...")
                data = sckt.recv(4096)
                # Decode data
                rec_msg = data.decode("utf-8").split(':')

                # If any status code apart from 200 was received then an error occurred, else display the result
                if "200" not in rec_msg[0]: print(  "Error: Status Code: " + '\033[91m' + rec_msg[0] + '\033[0m')
                else: print("Result of equation is: " + '\033[94m' + rec_msg[1] + '\033[0m' + " Status Code: " + '\033[94m' + rec_msg[0] + '\033[0m')
                d = - 1 # Used to break out of the Backoff loop

            # Catch the exception that a timeout happened
            except socket.timeout:
                # Increase timeout delay and inform User
                d = 2 * d
                print("Request " + '\033[91m' + "Timed Out" + '\033[0m' +", Trying again...")

                # If exceeding 2 seconds, then stop retrying
                if d > 2.0:
                    print('\033[91m' + "Error: Server failed to receive message" + '\033[0m')
                    d = - 1 # Used to break out of the Backoff loop

        print("Closing Socket...")
        sckt.close()

main()

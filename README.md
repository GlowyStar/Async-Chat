# Async Chat Server and Clients

## Overview
This repository contains an asynchronous chat server and client programs that allow multiple users to connect and communicate in real-time. The chat server manages connections, handles message forwarding, and maintains a list of connected clients. The clients can send and receive messages, providing a simple yet effective chat room experience.

## Technologies Used
- **Python**: The primary programming language used for both server and client code.
- **asyncio**: A Python library to write concurrent code using the async/await syntax.
- **StreamReader** and **StreamWriter**: asyncio classes that facilitate non-blocking network I/O.

## Getting Started

### Requirements
Before running the chat server and clients, ensure you have Python 3.7+ installed on your system. You can install all the necessary dependencies by running:

pip install -r requirements.txt


The `requirements.txt` file contains a list of Python packages required to run the chat programs.

### Running the Server
To start the chat server, navigate to the server directory and run:

python server.py


### Testing with Clients
In the `some_clients_for_tests` folder, you will find three test client files: `client_1.py`, `client_2.py`, and `client_3.py`. To test the chat functionality, open separate terminal windows for each client and run:

python client_1.py python client_2.py python client_3.py


You can then type messages in each client's terminal to see the communication between the clients in the chat room.

## Note on Error Handling
Please note that the current implementation does not handle errors that may occur during client connection termination. This is a known issue and will be addressed in future updates to ensure a more robust chat experience.

## Contributing
Contributions to improve the chat server and clients are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

<h1 align="center" style="text-shadow: 0 0 10px green;"><a href="https://github.com/GlowyStar" target="_blank" style="color: cyan; text-decoration: none;">🐍 Glowy Star</a></h1>


# A Peer-to-Peer Crypto Currency System

### Abstract:
Since crypto currency has been a hot topic in the recent years, it was crucial to study and learn how does it function. 
The project involved several topics such as peer to peer (P2P) network programming, blockchain structure, protocol
setup and software engineering.


### How To Run:
1. python3 -m src.tracker.tracker
2. python3 -m src.member.member <tracker_ip> <tracker_port> <listened_port>

If a tracker exists, you only need the second step. Indeed, you have to know the ip and the port of the tracker. 

### Description:
The project is broken down to two main parts which are the blockchain implementation and the peer-to-peer 
network design.
For sure, such a networks software product requires other tasks to be finished such as testing, debugging and parsing
protocol messages and project files.

Concerning the blockchain part, we following the widely known blockchain paradigm for creating a new currency for
educational purposes. Our blockchain is called a cheese stack because our software enables the user to mine blocks or
in our analogy 'Cheese' and add it to the 'Cheese Stack'. Such structure requires an initial block which is 
the 'Blue Cheese' as the oldest block and a connection between every block which is the 'Smell'. Regarding this 
customized blockchain, our implementation follows the normal basics of handling transactions in blockchains with 
encryption, data storage, hashes, money wallets and security of transactions.

Following, our other main part of the project is to share this blockchain using the peer-to-peer protocol for our
network. Such protocol fits our needs since it allows the users to save the blockchain data on their devices and 
share them securely without possible data loss the same way in real blockchain nowadays. Briefly, the protocol has
a Tracker that helps the users to connect, share and update their data. For more detailed information about
the protocol, please find the enclosed protocol.md file in the repository directory.

Other parts are included in the project to supervise and execute the main two parts. Those smaller parts include 
implementations of data and file parsers, extensive testing files for the network and blockchain model and 
the routine debugging tasks that are usually involved in software development.

¯\_(ツ)_/¯
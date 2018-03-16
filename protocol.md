The CheeseCoin Protocol
=======================

The CheeseCoin network is composed of a tracker and peers called members. 

The tracker is a server which contains a list of peers identified by an IP and a port. The members can ask the server for a list of members to communicate with them.

The members will synchronize the blockchain of transactions. 

The exchange
------------

A typical exchange between two members (__A__ and __B__) or a member (__A__) and a tracker (__B__) will be as follows:
```
A --> B
Request: SOMETHING REQUEST BODY
B --> A
Response: SOMETHING RESPONSE BODY
```
Indeed, __A__ will request something and __B__ will answer with the requested message. If the message requested is not correct, the receiver can send the following message:
```
A --> B
Request: SOMETHING ERROR _ERROR_
```
A member __A__ can notify something to another member __B__ by sending the message:
```
A --> B
Request: SOMETHING REPORT BODY
```

The Protocol
------------

1. [LIST_REQUEST](#LIST_REQUEST)
2. [LIST_ERROR](#LIST_ERROR)
3. [MEMBER_REPORT](#MEMBER_REPORT)
4. [TRANSACTION_REQUEST](#TRANSACTION_REQUEST)
5. [TRANSACTION_BROADCAST](#TRANSACTION_BROADCAST)
5. [TRANSACTION_ERROR](#TRANSACTION_ERROR)
6. [CHEESE_REQUEST](#CHEESE_REQUEST)
7. [CHEESE_BROADCAST](#TRANSACTION_BROADCAST)
8. [CHEESE_ERROR](#CHEESE_ERROR)

LIST_REQUEST
------------

A member can ask the tracker for a subset of the list of members. The tracker will reply with a message containing the list of members connected to the network.

```
Request: LIST REQUEST _PORT_\r\n
Response: LIST RESPONSE _LIST_\r\n
```
```
_PORT_: 2 Bytes 
_IP_: 4 Bytes
_LIST_ -> _IP_ _PORT_ | _IP_ _PORT_ _LIST_
```

| Field    | Description |
| -------- | -------- |
| `_IP_`   | IP of a member     |
| `_PORT_` | Port of a member where other members can connect to      |
| `_LIST_` | List of couples `(_IP_, _PORT_)` which represent a member    |




LIST_ERROR
----------

A member can send a message to inform the tracker that there is an error in the message. 
```
Response: LIST ERROR _ERROR_\r\n
````
```
_ERROR_: Nothing or a string without \r and \n
```
| Field | Description |
| -------- | -------- |
|`_ERROR_`  | The description of the error with regard to a requested list of members |

MEMBER_REPORT
-------------

If a member is logged out, a member can notify the tracker that he is not reachable.

```
Request: MEMBER REPORT _IP_ _PORT_\r\n
```
```
_PORT_: 2 Bytes 
_IP_: 4 Bytes
```
| Field | Description |
| -------- | -------- |
| `_IP_`     | IP of the disconnected member |
| `_PORT_` | Port of the disconnected member |


TRANSACTION_REQUEST
------------------

A member can request other members to send him a transaction. The receiver answers by sending back the requested transaction.

```
Request: TRANSACTION REQUEST\r\n
Response: TRANSACTION RESPONSE _TRANSACTION_\r\n
```
```
_TRANSACTION_ -> _LIST_INPUT_ _LIST_WALLET_ _LIST_AMOUNT_ _LIST_SIGN_
_LIST_INPUT_ -> _HASH_ _OUTPUT_NUMBER_ | _HASH_ _OUTPUT_NUMBER_ _LIST_INPUT_
_LIST_WALLET_ -> _WALLET_PUB_ | _WALLET_PUB_ _LIST_WALLET_
_LIST_AMOUNT_ -> _AMOUNT_ | _AMOUNT_ _LIST_AMOUNT_
_LIST_SIGN_ -> _SIGNATURE_ | _SIGNATURE_ _LIST_SIGN_
_HASH_: 32 Bytes
_OUTPUT_NUMBER_: 1 Bytes (0x00 or 0x01)
_WALLET_PUB_: 33 Bytes
_AMOUNT_: 4 Bytes
_SIGNATURE_: 71 Bytes
```

| Field           | Description |
| --------        | --------    |
| `_LIST_INPUT_`   | The list of all the previous transaction's hashes        |
| `_LIST_WALLET_` | The list of all the public keys involved in this transaction        |
| `_LIST_AMOUNT_` | The list of all the amounts involved in this transaction     |
| `_LIST_SIGN_`  | The list of signatures obtained with each creditor's private key and hash of the current transaction     |
| `_HASH_` | The hash (SHA256) of the previous transaction where the creditor is related |
| `_OUTPUT_NUMBER_` | The output number point the output out in the previous transaction |
| `_WALLET_PUB_` | This is the public key which represent the wallet |
| `_AMOUNT_` | We represent an amount by an integer |
| `_SIGNATURE_` | The signature is an encryption of the current transaction's hash  |
__NB__: All lists are indexed in the same way.

The transaction hash is computed with the SHA256 function in hashing the string `HASH_1|OUTPUT_NUMBER_1|...|HASH_N|OUTPUT_NUMBER_N|WALLET_1|...|WALLET_N|WALLET_OUTPUT1|WALLET_OUTPUT2|AMOUNT_1|...|AMOUNT_OUTPUT`

TRANSACTION_BROADCAST
---------------------

A member can broadcast a transaction to be mine by the others. 

```
Broadcast: TRANSACTION BROADCAST _TRANSACTION_\r\n
```
```
_TRANSACTION_ -> _LIST_INPUT_ _LIST_WALLET_ _LIST_AMOUNT_ _LIST_SIGN_
_LIST_INPUT_ -> _HASH_ _OUTPUT_NUMBER_ | _HASH_ _OUTPUT_NUMBER_ _LIST_INPUT_
_LIST_WALLET_ -> _WALLET_PUB_ | _WALLET_PUB_ _LIST_WALLET_
_LIST_AMOUNT_ -> _AMOUNT_ | _AMOUNT_ _LIST_AMOUNT_
_LIST_SIGN_ -> _SIGNATURE_ | _SIGNATURE_ _LIST_SIGN_
_HASH_: 32 Bytes
_OUTPUT_NUMBER_: 1 Bytes (0x00 or 0x01)
_WALLET_PUB_: 33 Bytes
_AMOUNT_: 4 Bytes
_SIGNATURE_: 71 Bytes
```

| Field           | Description |
| --------        | --------    |
| `_LIST_INPUT_`   | The list of all the previous transaction's hashes        |
| `_LIST_WALLET_` | The list of all the public keys involved in this transaction        |
| `_LIST_AMOUNT_` | The list of all the amounts involved in this transaction     |
| `_LIST_SIGN_`  | The list of signatures obtained with each creditor's private key and hash of the current transaction     |
| `_HASH_` | The hash (SHA256) of the previous transaction where the creditor is related |
| `_OUTPUT_NUMBER_` | The output number point the output out in the previous transaction |
| `_WALLET_PUB_` | This is the public key which represent the wallet |
| `_AMOUNT_` | We represent an amount by an integer |
| `_SIGNATURE_` | The signature is an encryption of the current transaction's hash  |
__NB__: All lists are indexed in the same way.

The transaction hash is computed with the SHA256 function in hashing the string `HASH_1|OUTPUT_NUMBER_1|...|HASH_N|OUTPUT_NUMBER_N|WALLET_1|...|WALLET_N|WALLET_OUTPUT1|WALLET_OUTPUT2|AMOUNT_1|...|AMOUNT_OUTPUT`


TRANSACTION_ERROR
-----------------

A member can send a message to inform the other member that there is an error in the message. 

```
Response: TRANSACTION ERROR _ERROR_\r\n
````
```
_ERROR_: Nothing or a string without \r and \n
```
| Field | Description |
| -------- | -------- |
|`_ERROR_`  | The description of the error with regard to a requested transaction |

CHEESE_REQUEST
--------------

A member can ask a cheese to another member. The member will respond in any cases.

```
Request: CHEESE REQUEST _PARENT_SMELL_\r\n
Response: CHEESE RESPONSE _LIST_TRANSACTION_ _NONCE_\r\n
```
```
_PARENT_SMELL_: 32 Bytes
_NONCE_: 4 Bytes
_LIST_TRANSACTION_ -> _TRANSACTION_ | _TRANSACTION_ _LIST_TRANSACTION_ 
```

| Field | Description |
| -------- | -------- |
|`_PARENT_SMELL_`  | The smell (SHA256) of the previous cheese requested |
|`_NONCE_`  | The nonce found by the miner |

The smell is computed with the SHA256 function by hashing the string `
PARENT_SMELL|TRANSACTION_1_HASH|TRANSACTION_2_HASH|...|NONCE`

CHEESE_BROADCAST
----------------

A miner can broadcast his mined cheese. The other member will not response to this message.
```
Broadcast: CHEESE BROADCAST _PARENT_SMELL_ _LIST_TRANSACTION_ _NONCE_\r\n
```

| Field | Description |
| -------- | -------- |
|`_PARENT_SMELL_`  | The smell (SHA256) of the previous cheese requested |
|`_NONCE_`  | The nonce found by the miner |

CHEESE_ERROR
------------

A member can send a message to inform the other member that there is an error in the message. 

```
Response: CHEESE ERROR _ERROR_\r\n
````
```
_ERROR_: Nothing or a string without \r and \n
```

| Field | Description |
| -------- | -------- |
|`_ERROR_`  | The description of the error with regard to a requested cheese |

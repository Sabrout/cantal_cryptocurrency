The grammar
===========

```
PACKET -> LIST_PACKET | MEMBER_PACKET | TRANSACTION_PACKET | CHEESE_PACKET.
END -> "\r\n".

IP_BYTE -> [0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]
IP -> IP_BYTE"."IP_BYTE".""."IP_BYTE"."IP_BYTE

DIGIT -> 0|[1-9][0-9]*
 
HASH -> [0-9a-z]{64}
PUBLIC_KEY -> [0-9a-z]{65}
SIGNATURE -> [0-9a-z]{63}
```

List Packet
-----------

```
LIST_PACKET -> "LIST" LIST_NEXT. 
LIST_NEXT -> LIST_REQUEST END | LIST_RESPONSE END | LIST_ERROR END.

LIST_REQUEST -> "REQUEST" DIGIT.
LIST_RESPONSE -> "RESPONSE" LIST_LIST.
LIST_ERROR -> "ERROR".

LIST_LIST -> IP DIGIT LIST_LIST_NEXT.
LIST_LIST_NEXT -> IP DIGIT LIST_LIST_NEXT | .
```

Member Packet
-------------

```
MEMBER_PACKET -> "MEMBER" MEMBER_NEXT.
MEMBER_NEXT -> MEMBER_REPORT END.

MEMBER_REPORT -> "REPORT" IP DIGIT.
```

Transaction Packet
------------------

```
TRANSACTION_PACKET -> "TRANSACTION" TRANSACTION_NEXT. 
TRANSACTION_NEXT -> TRANSACTION_REQUEST END | TRANSACTION_RESPONSE END | TRANSACTION_ERROR END.
TRANSACTION_REQUEST -> "REQUEST".
TRANSACTION_RESPONSE -> "RESPONSE" TRANSACTION.
TRANSACTION_ERROR -> "ERROR".
```
```
TRANSACTION -> LIST_INPUT LIST_WALLET LIST_AMOUNT LIST_SIGN.

LIST_INPUT -> HASH DIGIT LIST_INPUT_NEXT.
LIST_INPUT_NEXT -> HASH DIGIT LIST_INPUT_NEXT | .

LIST_WALLET -> PUBLIC_KEY LIST_WALLET_NEXT.
LIST_WALLET_NEXT -> PUBLIC_KEY LIST_WALLET_NEXT | .

LIST_AMOUNT -> DIGIT LIST_AMOUNT_NEXT. 
LIST_AMOUNT_NEXT -> DIGIT LIST_WALLET_NEXT |.

LIST_SIGN -> SIGNATURE LIST_SIGN_NEXT.
LIST_SIGN_NEXT -> SIGNATURE LIST_SIGN_NEXT | .
```

Cheese Packet
-------------

```
CHEESE_PACKET -> "CHEESE" CHEESE_NEXT.
CHEESE_NEXT -> CHEESE_REQUEST END | CHEESE_RESPONSE END | CHEESE_ERROR END.

CHEESE_ERROR -> "ERROR".
CHEESE_REQUEST -> "REQUEST" HASH.
CHEESE_RESPONSE -> "RESPONSE" LIST_TRANSACTION DIGIT.
```
```
LIST_TRANSACTION -> TRANSACTION LIST_TRANSACTION_NEXT.
LIST_TRANSACTION_NEXT -> TRANSACTION LIST_TRANSACTION_NEXT | .
```


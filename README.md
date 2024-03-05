# Protocol
As described by the instructions of the Homework assigment  We have implemented the protocol:

## 1. Ping request



| Type(1 Byte) | ID( 4 BYTE, unsinged integer) | Data |
| -------- | -------- | -------- |
| 0(request)     | the sequence number of the request    | the data sent with the request     |


## 2. Ping reply



| Type(1 Byte) | ID( 4 BYTE, unsinged integer) | Data |
| -------- | -------- | -------- |
| 1(reply)     | the sequence number of the request    | the data sent with the request     |


we send the packet, receive it on the agent and then replying it to the client, wich prints it(if within timeout)

the packets are sent one by one after each packet is received or timeouted.

If the the packet is lost, the reply will not be recieved and timeout will be printed

## Wireshark

we run the agent:
python3 udp_agent.py 127.0.0.1 (default port 1337)

and run the client:
python3 udp_client.py 127.0.0.1 -c 10 -s 10 

the 20 packets(10 request & reply)
![Screenshot 2024-03-05 at 2.32.25](https://hackmd.io/_uploads/B1F4OkVpT.png)

let's show the 3rd packet request:

![Screenshot 2024-03-05 at 2.33.53](https://hackmd.io/_uploads/SJIpukNpa.png)

we can see the that the first byte: 0(request)
and the next 4 bytes are 00 00 00 02 (hex), 
which is 2 (We start count from 0)

after that the data is 10 times 30(in hex) which is the ascii value of '0' which we send as the data.

the reply is:


![Screenshot 2024-03-05 at 2.43.20](https://hackmd.io/_uploads/HJEhqJ4aT.png)

we can see the that the first byte: 1(request)
and the next 4 bytes are 00 00 00 02 (hex), 
which is 2 (the sequence number of the request)

after that the data is 10 times 30(in hex) which is the ascii value of '0' which we reply as it was the sent data.

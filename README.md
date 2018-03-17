# Fapster

:books: Reti Peer To Peer - Università degli Studi di Ferrara :books:

A peer-to-peer server based on the Napster's approach:

> ### Centralized Directory Service
> **1. Client contacts Napster (via TCP)**
>   * Provides a list of files it will share
>   * ...and Napster’s central server updates the directory
>
> **2. Client searches on a title**
>   * Napster identifies online clients with the file
>   * ...and provides IP addresses
>
> **3. Client requests the file from the chosen supplier**  
>   * Supplier transmits the file to the client
>   * Both client and supplier report status to Napster
> ### Properties
> **1. Server’s directory continually updated**
>   * Always know what files are currently available
>   * Point of vulnerability for legal action
>
> **2. Peer-to-peer file transfer**
>   * No load on the server
>   * Plausible deniability for legal action (but not enough)

## Usage

```shell
python3 fapster_server.py
```
**_Note:_** Python 3.6.x or above is required

The server is now listening on port 3000.

Once a peer begins the communication, **the directory server _won't_ keep the connection open for further requests**, so keep in mind: 
* 1 request = 1 connection

### Client's supported commands:

[xxxB] = the parameter length in bytes
 
```shell
# Login the peer into the directory
LOGI[4B].IP_Peer[55B].Port_Peer[5B]
# Server response will be
ALGI[4B].SessionID[16B]

# Logout the peer from the directory
LOGO[4B].SessionID[16B]
# Server response will be
ALGO[4B].\#delete[3B]

# Add a file to the directory
ADDF[4B].SessionID[16B].Filemd5[32B].Filename[100B]
# Server response will be
AADD[4B].\#copy[3B]

# Delete a file from the directory
DELF[4B].SessionID[16B].Filemd5[32B]
# Server response will be
ADEL[4B].\#copy[3B]

# Find a file in the directory
FIND[4B].SessionID[16B].Ricerca[20B]
# Server response will be
AFIN[4B].\#idmd5[3B].{Filemd5_i[32B].Filename_i[100B].\#copy_i[3B].{IPP2P_i_j[55B].PP2P_i_j[5B]}}(j=1..\#copy_i)}(i=1..\#idmd5)

# Register a file download
DREG[4B].SessionID[16B].Filemd5[32B]
# Server response will be
ADRE[4B].\#download[5B]
```

## To-Do
- [x] Directory Server implementation
- [ ] Peer implementation

## Authors :rocket:
* [Federico Frigo](https://github.com/xBlue0)
* [Niccolò Fontana](https://github.com/NicFontana)
* [Giovanni Fiorini](https://github.com/GiovanniFiorini)
* [Marco Rambaldi](https://github.com/jhonrambo93)

Enjoy :sunglasses:

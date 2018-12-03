# model-caching
## Overview
The purpose of this project is to observe the cache efficiency between two different network architecture. The first one (Fig.1) is a centralize controller to store cache information and manage serval nodes. If nodes send a request to the controller, it would transmit the necessary part to nodes. The other one (Fig.2) is still a centralize architecture, but nodes can communicate with each other. They have serval ways to send/recieve cache information. We would discuss these two situation in the future.

* Fig.1
![](https://i.imgur.com/SKHIYvu.png)

* Fig.2
![](https://i.imgur.com/2LIE7Ss.png)

## Prerequisites
Prepare at least 3 raspberry pi 3B

* Multi-interfaceFileFetcher

1. Copy your ssh public key to `~/.ssh/authorized_keys
2. Establish a ftp service on one raspberry pi
`/etc/vsftpd.conf`
```shell
anonymous_enable=YES
anon_root=/home/pi
anon_max_rate=2048000
```

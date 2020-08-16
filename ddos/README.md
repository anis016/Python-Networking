# DDOS

DDOS stands for Distributed Denial of Service and it is an attack where the resources of a server is blocked by flooding it with huge amount of requests.
> Performing a DDOS attack onto any server that is not yours or you don't have permission to attack is highly illegal.

For testing the DDOS attack, either use
* Your own Router webpage
* Provision Apache server in your machine

For getting the Router IP Address use `ip route` command
```
$ ip route | grep default
default via 192.168.0.1 dev wlp2s0 proto dhcp metric 600
```

For creating apache server follow the below steps using Vagrant
* Provision using Vagrant
  ```
  $ vagrant --version
  Vagrant 2.2.9
  $ cd ./ddos/vagrants
  $ vagrant up # to create and provision
  $ vagrant destroy # to destroy
  ```
* Access the Apache server by visiting [localhost:8081](localhost:8081)

# LEGAL NOTICE
THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL USE ONLY! IF YOU ENGAGE IN ANY ILLEGAL ACTIVITY THE AUTHOR DOES NOT TAKE RESPONSIBILITY FOR IT. BY USING THIS 
SOFTWARE OR ANY PIECE OF THE SOFTWARE YOU AGREE WITH THESE TERMS.
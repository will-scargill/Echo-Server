<p align="center">
  <a href="https://github.com/will-scargill/echo">
    <img src="https://img.shields.io/github/workflow/status/will-scargill/echo-server/Python%20application" alt="Logo">
  </a>
  <a href="https://github.com/will-scargill/echo">
    <img src="https://img.shields.io/github/license/will-scargill/echo-server" alt="Logo">
  </a>
  <a href="https://github.com/will-scargill/echo">
    <img src="https://ghcr-badge.herokuapp.com/will-scargill/echo/latest_tag" alt="Logo">
  </a>
  <br>
  <br>
  <a href="https://github.com/will-scargill/echo-server">
    <img src="https://imgur.com/MSGdWAz.png" alt="Logo">
  </a>
  <br>
  <a href="https://github.com/will-scargill/echo">
    Echo Client
  </a>
  <a href="https://github.com/will-scargill/echo-server">
     | Echo Server
  </a>
</p>

## Getting started

To get an instance up and running follow these steps.
Recommended deployment method is via docker compose.

### Prerequisites

* [docker](https://docs.docker.com/engine/install/ubuntu/)
* [docker-compose](https://docs.docker.com/compose/install/)

### Installation

1. Create a docker-compose.yml file with the following template
   ```yaml
    version: '3.9'
    services:
      echo:
        container_name: echo
        image: ghcr.io/will-scargill/echo:latest
        environment:
          ECHO_LIVE: "true"
          ECHO_DB_TYPE: mysql
          ECHO_MYSQL_HOST: server-host
          ECHO_MYSQL_USER: username
          ECHO_MYSQL_PASS: password
          ECHO_MYSQL_DB: database_name
        ports:
            - 16000:16000
        volumes:
          - ./configs:/usr/src/app/configs
          - ./data:/usr/src/app/data
   ```
   ECHO_DB_TYPE can be:
   * mysql
   * sqlite
   
   If using sqlite, other MYSQL environment variables are not needed
2. Run the compose file
   ```sh
   docker-compose up
   ```
3. Verify connectivity using the [Echo Client](https://github.com/will-scargill/Echo)

4. Use the letmein command to give yourself administrator permissions
   ```
   /letmein [key]
   ```
   The key can be found in the data folder - data/key.txt

## Configuration

- ### [config.ini](https://github.com/will-scargill/Echo-Server/blob/master/configs/config.ini)

Most settings are self-explanatory.
<b> Do not change serverVersion and CompatibleClientVers. This will break your server. </b>

clientnum - the maximum number of clients that can connect at once

strictBanning - bans use IP as well as Echo IDs

useBlacklist - Enables/disables the word blacklist

kickOnUse - Kicks a user when they attempt to use a word on the blacklist

- ### [blacklist.txt](https://github.com/will-scargill/Echo-Server/blob/master/configs/blacklist.txt)

A very simple blacklist for words. One word per line. If any word in a user's message is in the file the message will not be sent to other clients. 

- ### [commands.json](https://github.com/will-scargill/Echo-Server/blob/master/configs/commands.json)

Do not change this file. More functionality to be added later.

- ### [roles.json](https://github.com/will-scargill/Echo-Server/blob/master/configs/roles.json)

New roles can be added in the following format


    "role_name": ["heirarchy_value", "command flag 1", "command flag 2"]

    
The heirarchy value determines which roles can target other roles. A lower heirarchy value cannot target a higher one. 
The command flags and their corresponding commands can be found in [roles.json](https://github.com/will-scargill/Echo-Server/blob/master/configs/roles.json).

The command flag * is special. It grants a role permission to use <b> any </b> commands the server has installed.
<br>
<b> This flag is only given to the "admin" role by default. Be careful when giving it to other roles! </b>

## Upgrading

TBA

## Misc

### regenerateRsaKeys.py

The RSA keys used by the server can be regenerated by running this script. Alternatively, you can delete the key files from the data folder and the server will regenerate them automatically.

## License

Distributed under the GPL-3.0 License.

## Contact

Twitter - [@willscargill](https://twitter.com/willscargill)

Project Link: [https://github.com/will-scargill/echo-server](https://github.com/will-scargill/echo-server)

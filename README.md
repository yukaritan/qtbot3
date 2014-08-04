## This is a bot
It connects to IRC. You need a couple more files for it to work.

1. "qtbot3_bot/settings.json":
    `{
        "server": "irc.freenode.net",
        "nick": "qtbot3",
        "port": 6667,
        "service_host": "localhost",
        "service_port": 4000
    }`

2. "qtbot3_service/settings.json":
    `{
        "master": "~you@your_host_here",
        "service_host": "localhost",
        "service_port": 4000,
        "identify": "bot_passphrase_goes_here_but_its_sent_to_nickserv_so_be_careful"
    }`


## Requirements
1. Python 3.4
2. Gunicorn
3. Flask
4. Other things. Please let me know what it has you install.


## Run
First start the service

    cd qtbot3_service
    ./run.sh

Then the client

    cd qtbot3_bot
    python3.4 main.py

This has only been tested on Python 3.4.


## License
Doubly licensed under GPL v3 and NBPL; see license1.txt and license2.txt.


## Enjoy
Satisfaction is mandatory and non-negotiable.

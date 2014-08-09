## This is a bot
It connects to IRC. You need a couple more files for it to work.

1. "qtbot3_bot/settings.json":

    ```json
    {
        "server": "irc.freenode.net",
        "nick": "qtbot3",
        "port": 6667,
        "service_host": "localhost",
        "service_port": 4000
    }
    ```

2. "qtbot3_service/settings.json":

    ```json
    {
        "master": "you@some_host",
        "service_host": "localhost",
        "service_port": 4000,
        "identify": "your_password_that_the_nickserv_module_sends_to_nickserv",
        "cmd_prefix": ";",
        "plugins": ["commands",
                    "nickserv",
                    "greetings",
                    "rainbow",
                    "test",
                    "currency",
                    "cleverbot"]
    }
    ```

## Requirements
1. Python 3.4
2. Requests
3. Gunicorn
4. Flask
5. Lupa
6. Cleverbot2
7. Other things. Please let me know what it has you install.


## Run
First start the services

    ```
    cd qtbot3_service
    ./run_storage.sh
    ./run_service.sh
    ```

Then the client

    ```
    cd qtbot3_bot
    python3.4 main.py
    ```

This has only been tested on Python 3.4.


## License
Doubly licensed under GPL v3 and NBPL; see license1.txt and license2.txt.


## Enjoy
Satisfaction is mandatory and non-negotiable.

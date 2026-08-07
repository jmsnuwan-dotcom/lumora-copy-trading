from client.ui.app import run
from client.start_client import start_client


def main():

    token = run()

    if token:
        start_client(token)


if __name__ == "__main__":
    main()
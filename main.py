import sys
from .server import start_server


def main():
    directory = None

    # Parse --directory flag
    if "--directory" in sys.argv:
        index = sys.argv.index("--directory")
        if index + 1 < len(sys.argv):
            directory = sys.argv[index + 1]

    start_server(host="localhost", port=4221, directory=directory)


if __name__ == "__main__":
    main()

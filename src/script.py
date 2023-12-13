import argparse


def process_arguments(args):
    result = f"Received string: {args.string}, Received integer: {args.integer}, Verbose: {'on' if args.verbose else 'off'}"
    return result


def main(args=None):
    parser = argparse.ArgumentParser(description="Example script.sh that accepts command-line arguments.")

    parser.add_argument("-s", "--string", type=str, default='', help="A string argument")
    parser.add_argument("-i", "--integer", type=int, default=0, help="An integer argument")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = parser.parse_args(args)

    return process_arguments(args)


if __name__ == "__main__":
    print(main())

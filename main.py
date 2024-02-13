# main.py

import argparse
from app import app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(description="Flask Server Configuration")
    parser.add_argument("--host", default="0.0.0.0", help="Host IP address")
    parser.add_argument("--port", default="1000", help="Port number")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app.run(host=args.host, port=args.port, debug=True)

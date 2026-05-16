#!/usr/bin/env python3
"""Simple server for the CNM graph visualizer."""

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler


class CNMServerHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    parser = argparse.ArgumentParser(description="CNM graph visualizer server")
    parser.add_argument(
        "-p", "--port", type=int, default=5733, help="Port to run on (default: 5733)"
    )
    args = parser.parse_args()

    try:
        server = HTTPServer(("0.0.0.0", args.port), CNMServerHandler)
    except OSError as e:
        if e.errno == 48:
            print(f"Error: port {args.port} is already in use")
            raise SystemExit(1)
        raise
    print(f"Server running on 0.0.0.0:{args.port} (all interfaces)")
    print(f"Open http://localhost:{args.port}/index.html in your browser")
    print("Press Ctrl+C to stop")
    server.serve_forever()


if __name__ == "__main__":
    main()

"""
This is very strange piece of code needed to simulate github pages serving behavior locally
url -> filepath
/ -> /docs/index.html
/about -> /docs/about.html
/about -> /docs/about/index.html
"""
import pathlib
import http.server
import os
from urllib.parse import unquote

PORT = 8000

CURRENT_DIR = pathlib.Path(__file__).parent
os.chdir(CURRENT_DIR / "docs")

class GitHubPagesLikeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = unquote(self.path)

        # Check if the path is a directory
        if os.path.isdir(self.path[1:]):  # Remove the leading '/' for os.path compatibility
            if not self.path.endswith('/'):
                # Redirect to the same path with a trailing '/' for directories
                self.send_response(301)
                self.send_header('Location', self.path + '/')
                self.end_headers()
                return
            else:
                # Serve index.html if it exists in the directory
                if os.path.exists(self.path[1:] + 'index.html'):
                    self.path += 'index.html'

        # Append '.html' if it's not a file request and the .html file exists
        elif not self.path.endswith('.html') and os.path.exists(self.path[1:] + '.html'):
            self.path += '.html'

        # Serve the rewritten URL path
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    http.server.test(HandlerClass=GitHubPagesLikeHandler, port=PORT)


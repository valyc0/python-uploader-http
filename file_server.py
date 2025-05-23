#!/usr/bin/env python3
"""
Simple HTTP Server for file upload and download
Usage: python3 file_server.py [--port PORT] [--directory DIR]
"""

import argparse
import http.server
import os
import socketserver
import cgi
import urllib.parse
import sys
import html


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for file uploads and downloads"""

    def do_GET(self):
        """Handle GET requests - list directory content or serve files"""
        # If path is root, show a nice directory listing with upload form
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Get files in the directory
            files = os.listdir(self.directory)
            files.sort()

            output = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>File Server</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    h1, h2 {{
                        color: #333;
                    }}
                    ul {{
                        list-style-type: none;
                        padding: 0;
                    }}
                    li {{
                        margin: 10px 0;
                        padding: 8px;
                        border-bottom: 1px solid #eee;
                    }}
                    a {{
                        text-decoration: none;
                        color: #0066cc;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                    .upload-form {{
                        background: #f9f9f9;
                        padding: 15px;
                        border-radius: 5px;
                        margin-top: 20px;
                    }}
                    .button {{
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 8px 16px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 14px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 4px;
                    }}
                </style>
            </head>
            <body>
                <h1>File Server</h1>
                <p>Current directory: {html.escape(os.path.abspath(self.directory))}</p>
                
                <h2>Files</h2>
                <ul>
            """
            
            for filename in files:
                filepath = os.path.join(self.directory, filename)
                filesize = os.path.getsize(filepath)
                size_str = self._format_size(filesize)
                
                output += f"""
                <li>
                    <a href="/{urllib.parse.quote(filename)}">{html.escape(filename)}</a> ({size_str})
                    <a href="/delete/{urllib.parse.quote(filename)}" 
                       onclick="return confirm('Are you sure you want to delete this file?')"
                       style="color: red; margin-left: 10px;">Delete</a>
                </li>
                """
                
            output += """
                </ul>
                
                <div class="upload-form">
                    <h2>Upload File</h2>
                    <form enctype="multipart/form-data" method="post">
                        <input type="file" name="file" required>
                        <input class="button" type="submit" value="Upload">
                    </form>
                </div>
            </body>
            </html>
            """
            
            self.wfile.write(output.encode())
            return
        
        # Handle file deletion requests
        if self.path.startswith("/delete/"):
            filename = urllib.parse.unquote(self.path[8:])
            filepath = os.path.join(self.directory, filename)
            
            # Security check - make sure the file is within the served directory
            if os.path.exists(filepath) and os.path.abspath(filepath).startswith(os.path.abspath(self.directory)):
                try:
                    os.remove(filepath)
                    # Redirect back to the main page
                    self.send_response(303)
                    self.send_header("Location", "/")
                    self.end_headers()
                except Exception as e:
                    self.send_error(500, f"Error deleting file: {str(e)}")
            else:
                self.send_error(404, "File not found")
            return
        
        # Default behavior for all other paths - serve files
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests - file uploads"""
        content_type = self.headers.get('Content-Type')
        
        # Check if the request contains a file upload
        if content_type and content_type.startswith('multipart/form-data'):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type
                }
            )
            
            # Check if the file field was submitted
            if 'file' in form and form['file'].filename:
                file_item = form['file']
                filename = os.path.basename(file_item.filename)
                filepath = os.path.join(self.directory, filename)
                
                # Save the file
                with open(filepath, 'wb') as f:
                    f.write(file_item.file.read())
                
                # Redirect back to the main page after successful upload
                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()
                return
        
        # If we get here, something went wrong with the upload
        self.send_response(400)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Upload failed!</h1></body></html>")
    
    def _format_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"


def run_server(port=8000, directory=os.getcwd()):
    """Run the HTTP server"""
    # Ensure directory exists
    directory = os.path.abspath(directory)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Change to the specified directory
    os.chdir(directory)
    
    # Create the server
    handler = lambda *args: CustomHTTPRequestHandler(*args, directory=directory)
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server started at port {port}")
        print(f"Serving files from: {directory}")
        print(f"Access the server at: http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def main():
    """Parse command line arguments and start the server"""
    parser = argparse.ArgumentParser(description="HTTP Server for file upload and download")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
    parser.add_argument("--directory", type=str, default=None, help="Directory to serve files from (default: 'uploads' folder in current directory)")
    
    args = parser.parse_args()
    
    # If no directory is specified, use 'uploads' folder in the current directory
    if args.directory is None:
        default_dir = os.path.join(os.getcwd(), "uploads")
        print(f"No directory specified. Using default: {default_dir}")
        args.directory = default_dir
        
    run_server(port=args.port, directory=args.directory)


if __name__ == "__main__":
    main()

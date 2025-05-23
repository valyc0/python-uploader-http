# Simple HTTP File Server

This is a simple HTTP server that allows you to upload and download files through a web interface.

## Features

- File listing with size information
- File upload via web interface
- File download by clicking on file names
- File deletion
- Configurable port and directory

## Usage

### Using the Start Script

The easiest way to start the server is by using the provided start script:

```bash
./start_server.sh
```

This will start the server on port 8000 and serve files from the current directory.

You can also specify a custom port and directory:

```bash
./start_server.sh 9000 /path/to/your/files
```

### Direct Usage

Alternatively, you can run the Python script directly:

```bash
python3 file_server.py
```

This will start the server on port 8000 and serve files from the current directory.

### Custom Port and Directory

```bash
python3 file_server.py --port 9000 --directory /path/to/your/files
```

### Command-line Options

- `--port PORT`: Specify the port to run the server on (default: 8000)
- `--directory DIR`: Specify the directory to serve files from (default: 'uploads' folder in current directory)

## Access the Server

Once the server is running, open a web browser and visit:

```
http://localhost:8000
```

(Replace 8000 with your chosen port if using a custom port)

## Requirements

- Python 3.x (tested with Python 3.6+)
- No external dependencies required (uses standard library only)

## Using with curl

You can also interact with the server using curl commands from the terminal:

### List Files

To retrieve the list of files (HTML output):

```bash
curl http://localhost:8000/
```

### Upload Files

To upload a file to the server:

```bash
curl -F "file=@/path/to/local/file.txt" http://localhost:8000/
```

### Download Files

To download a file from the server:

```bash
curl -O http://localhost:8000/filename.txt
```

Or save it with a different name:

```bash
curl -o new_name.txt http://localhost:8000/filename.txt
```

### Delete Files

To delete a file (note that this will return the main page as HTML):

```bash
curl http://localhost:8000/delete/filename.txt
```

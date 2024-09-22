import socket
import ssl
import sys


def sending_request(host, path, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    if port == 443:
        context = ssl.create_default_context()
        s = context.wrap_socket(s, server_hostname=host)

    request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection: Keep-Alive\r\n\r\n"
    s.send(request.encode())

    response = b''

    while True:
        data = s.recv(4096)
        response += data
        if not data:
            s.close()
            break

    print(response)

    return response

def web_tester(url):
    if url.startswith("https://"):
        cut_off_length = len("https://")
        port = 443
    elif url.startswith("http://"):
        cut_off_length = len("http://")
        port = 80
    else:
        print("The input format is not supported, please enter a URL with the https:// or https://")
        return
    
    url_segments = url[cut_off_length: ].split("/", 1)
    host = url_segments[0]
    path = "/" + url_segments[1] if len(url_segments) > 1 else "/"

    response = sending_request(host, path, port)

    print(response)



    


if __name__ == "__main__":
    web_tester(sys.argv[1])
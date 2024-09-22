import socket
import ssl
import sys


def processing_header(header):
    for header_line in header:
        if "Set-Cookie" in header_line:




def sending_request(host, path, port):
    context = ssl.create_default_context()
    context.set_alpn_protocols(['http/1.1', 'h2'])
    s = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)

    s.connect((host, port))

    alpn_protocol = s.selected_alpn_protocol()

    request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection: Keep-Alive\r\n\r\n"
    s.send(request.encode())

    response = b''

    data = s.recv(4096)
    response += data

    s.close()

    response_str = response.decode("utf-8", errors="ignore")
    header = response_str.split("\r\n\r\n", 1)[0]

    return header, alpn_protocol

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

    header, alpn_protocol = sending_request(host, path, port)

    processing_header(header)

    if alpn_protocol != None:
        if "h2" in alpn_protocol:
            h2_support = "Yes"
        else:
            h2_support = "No"
    else:
        h2_support = "No"

    print("Website: " + host)
    print("1. Supports http2: " + h2_support)


if __name__ == "__main__":
    web_tester(sys.argv[1])
import socket
import ssl
import sys


def checking_status(host, header, port):
    if "404" in header:
        print("Error: 404 \nThe requested document does not exist on the server, access attempt failed.")
        return False
    elif "505" in header:
        print("Error: 505 \nHTTP Version Not Supported, access attempt failed.")
        return False
    elif "302" or "301" in header:
        for line in header.splitlines():
            if line.startswith("Location") or line.startswith("location"):
                redirection_url = line.split(":", 1)[1].strip()
                if redirection_url.startswith("/"):
                    if port == 443:
                        new_url = "https://" + host + redirection_url
                    elif port == 80:
                        new_url = "http://" + host + redirection_url
                    web_tester(new_url)
                else:
                    web_tester(redirection_url)
                return False
    elif "401" in line:
        print("Error: 401 \nThe web page is password protected and cannot be accessed without proper credentials.")
        return False
    
    return True
        



def sending_request(host, path, port):
    context = ssl.create_default_context()
    s = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)

    try:
        proper_host_name = socket.gethostbyname(host)
    except socket.gaierror as e:
        print("Error, the URI address is invalid and its IP address cannot be found." )
        

    s.connect((host, port))

    request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection: Keep-Alive\r\n\r\n"
    s.send(request.encode())

    response = b''

    data = s.recv(4096)
    response += data

    s.close()

    response_str = response.decode("utf-8", errors="ignore")
    header = response_str.split("\r\n\r\n", 1)[0]

    return header

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

    header= sending_request(host, path, port)

    print(header + "\n\n")

    if not checking_status(host, header, port):
        return

    # if alpn_protocol != None:
    #     if "h2" in alpn_protocol:
    #         h2_support = "Yes"
    #     else:
    #         h2_support = "No"
    # else:
    #     h2_support = "No"

    print("Website: " + host)
    # print("1. Supports http2: " + h2_support)


if __name__ == "__main__":
    web_tester(sys.argv[1])
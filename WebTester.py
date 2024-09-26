import socket
import ssl
import sys

def check_cookies(header):
    cookie_array = list()
    for header_line in header.splitlines():
        if header_line.lower().startswith("set-cookie"):
            cookie_info = list()
            
            cookie = header_line.split(":", 1)[1]
            cookie_sections = cookie.split(";")
            
            cookie_name = "cookie name: "  + cookie_sections[0].split("=", 1)[0].strip()
            cookie_info.append(cookie_name)

            for section in cookie_sections:
                if section.lower().strip().startswith("expires"):
                    expire_time = "expire time: " + section.split("=", 1)[1]
                    cookie_info.append(expire_time)
                
                if section.lower().strip().startswith("domain"):
                    domain = "domain name: " + section.split("=", 1)[1]
                    cookie_info.append(domain)
            
            cookie_array.append(cookie_info)
    
    return cookie_array



def check_h2(host, port):
    #Because http does not support http/2, only https does
    if port == 80:
        return None

    context = ssl.create_default_context()
    context.set_alpn_protocols(['http/1.1', 'h2'])

    s = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
    s.connect((host, port))

    protocol = s.selected_alpn_protocol()

    return protocol
    

def checking_status(host, status_line, header, port):
    if "404" in status_line:
        print("Error: 404 \nThe requested document does not exist on the server, access attempt failed.")
        return 404
    elif "505" in status_line:
        print("Error: 505 \nHTTP Version Not Supported, access attempt failed.")
        return 505
    elif "302" in status_line or "301" in status_line:
        for line in header.splitlines():
            if line.lower().startswith("location"):
                redirection_url = line.split(":", 1)[1].strip()
                if redirection_url.startswith("/"):
                    if port == 443:
                        new_url = "https://" + host + redirection_url
                    elif port == 80:
                        new_url = "http://" + host + redirection_url
                    web_tester(new_url)
                else:
                    web_tester(redirection_url)
        
        return 302
    elif "401" in status_line:
        return 401
        



def sending_request(host, path, port):
    if (port == 443):
        context = ssl.create_default_context()
        s = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
    elif port == 80:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))
    request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection: Keep-Alive\r\n\r\n"
    s.send(request.encode())

    print("---Request begin---")
    print(request)
    print("---Request end---")
    print("HTTP request sent, awaiting response...\n")

    response = b''
    data = s.recv(4096)
    response += data

    s.close()

    response_str = response.decode("utf-8", errors="ignore")
    header = response_str.split("\r\n\r\n", 1)[0]

    print("---Response header ---")
    print(header + "\n\n")

    return header

def web_tester(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    if url.startswith("https://"):
        cut_off_length = len("https://")
        port = 443
    elif url.startswith("http://"):
        cut_off_length = len("http://")
        port = 80
    
    url_segments = url[cut_off_length: ].split("/", 1)
    host = url_segments[0]
    path = "/" + url_segments[1] if len(url_segments) > 1 else "/"

    header = sending_request(host, path, port)

    match checking_status(host, header.splitlines()[0], header, port):
        case 404:
            return
        case 505:
            return
        case 302:
            return
        case 401:
            password_protected = "Yes"
        case _:
            password_protected = "No"

    cookies = check_cookies(header)

    protocol = check_h2(host, port)
    if protocol != None and 'h2' in protocol:
        h2_support = "Yes"
    else:
        h2_support = "No"

    print("--- Output ---")
    print("Website: " + host)
    print("1. Supports http2: " + h2_support)
    print("2. List of Cookies:")


    if len(cookies) != 0:
        for cookie in cookies:
            match len(cookie):
                case 1:
                    print(cookie[0])
                case 2:
                    print(cookie[0] + ", " + cookie[1])
                case 3:
                    print(cookie[0] + ", " + cookie[1] + ", " + cookie[2])
    else:
        print("None")
    
    print("3. Password-protected: " + password_protected)


if __name__ == "__main__":
    web_tester(sys.argv[1])
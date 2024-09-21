import socket
import ssl
import sys

def web_tester(url):
    if url.startswith("https://"):
        port = 443
    elif url.startswith("http://"):
        port = 80
    else:
        print("Invalid URL format. Please use http:// or https://")
        return
    
    

    


if __name__ == "__main__":
    web_tester(sys.argv[1])
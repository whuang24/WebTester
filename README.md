
<a id="readme-top"></a>

<br />
<div align="center">

  <h3 align="center">WebTester</h3>

  <p align="center">
    A python built webpage url tester.
  </p>
</div>


## About The Project

This is a python software that allows the users to send HTTP requests to a webpage to fetch for some of its basic information.
It also organizes the information to identify whether the server in which the webpage is hosted on supports HTTP/2, whether the webpage is password-protected, able to list all of the cookies that exist on that webpage, and capable of redirecting itself to other host or paths if the requested webpage is temporarily or permanently moved.

The project defaults the header as "http://" if it is not specified at the beginning of the URL. Because of its redirecting capabilities, it would redirect the URL to "https://" if a status code 302 or 301 is received.


## Project Limitations

The following is a list of the limitations that the project currently contain

* It can only access webpages with URL that starts with http or https.
* It is not capable of properly detecting and reporting all errors while sending or receiving requests.
* It can only identify status codes of 200, 404, 505, 302, and 401. When receiving other status codes, it will not be able to identify if the request is successfully sent.


## Getting Started

Type inside the terminal
```
python WebTester.py <URL>
```

Example
```
python WebTester.py www.google.com/
```

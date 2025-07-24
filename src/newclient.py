#!/usr/bin/python3
import socket,math
import time
import hashlib
import os,sys






class Delivery:
    def clear_screen(self,retry_wait=1):
        os.system('clear')
    def __init__(self,filepath='./SnapNeo/data.zip',bs=512,no_wait=False,wait_file_path="./SnapNeo/data_ready",bluetooth_device='F4:4E:FC:A8:34:10'):
        #self.clear_screen()
        self.bluetooth_device=bluetooth_device
        self.filepath=filepath
        self.bs=bs
        self.no_wait=no_wait
        self.retry_wait=1
        self.wait_file_path=wait_file_path
        print("⏸️ Waiting until the package arrives...")
        if self.no_wait==False:
            while True:
                if os.path.isfile(self.wait_file_path):
                    self.size=os.path.getsize(self.filepath)
                    with open(self.filepath,"rb") as f:
                        self.data=f.read()
                    self.md5=hashlib.md5(open(self.filepath,'rb').read()).hexdigest()
                    break
                else:
                    time.sleep(1)
        else:
            print("💡 Using no wait option, skipping wait file.")
            self.size=os.path.getsize(self.filepath)
            with open(self.filepath,"rb") as f:
                self.data=f.read()
            self.md5=hashlib.md5(open(self.filepath,'rb').read()).hexdigest()
        print('➡️ The package is ready to be sent.')
        self.setup_socket()

    def setup_socket(self):
        try:
            print('⏸️ Establishing the connection to the following device:',self.bluetooth_device)
            self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.client.connect((self.bluetooth_device,4))
            print('➡️ CONNECTION ESTABLISHED ')
        except OSError as e:
            print('⛔ Failed to open up a socket.')
            try:
                self.client.close()
                print('✅ The previous socket closed successfully.')
            except AttributeError as nsa:
                print('⛔ No previous socket found but cannot create a socket.')
                sys.exit()

    def send_package(self):


        try:
            print('     💡 Sending file size:', self.size)
            print('     💡 Sending block size:',self.bs)
            print('     💡 Sending MD5 hash: ',self.md5)

            self.client.send(self.size.to_bytes(4,'big'))
            self.client.send(self.bs.to_bytes(4,'big'))
            self.client.send(self.md5.encode('UTF-8'))



            last_chunk=self.size%self.bs
            number_of_chunks=math.floor(self.size/self.bs)
            seek=0

            start=time.time()
            for _ in range(0,number_of_chunks):
                self.client.send(self.data[seek:seek+self.bs])
                print(seek,end='\r')
                seek+=self.bs
            self.client.send(self.data[seek:])
            #self.client.send('aaaaa'.encode('UTF-8'))
            end=time.time()
            print('     ✅ File has been sent within: '+str(math.floor(end-start))+" seconds")
            respond=self.client.recv(self.bs)
            print('     💡 Received response from the server:',respond)
            if respond.decode('UTF-8')=='OK':
                print('     💡 No resend requested.')
                print('     ✅ File has been sent successfully.')
                self.client.close()
            elif respond.decode('UTF-8')=='RESEND':
                print('     💡 Resend requested: ')
                raise Exception('⛔ Failed to send a package.')
            else:
                print('     💔 Failed to retrieve the message:',respond.decode('UTF-8'))
                raise Exception('⛔ Something went wrong.')
        except Exception as e:
            print(e)
            print('⛔ Sending a package failed. Retry in {} seconds.'.format(str(self.retry_wait)))
            time.sleep(self.retry_wait)
            #self.clear_screen()
            self.setup_socket()
            self.send_package()


if __name__=="__main__":
    print("⏸️ Self test")
    Delivery = Delivery(no_wait=True,filepath='./12.zip')
    Delivery.setup_socket()
    Delivery.send_package()

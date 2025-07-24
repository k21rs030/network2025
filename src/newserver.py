#!/usr/bin/python3
import socket,math
import os
import hashlib,sys
import time
import subprocess
import requests




# an external bluetooth device
bluetooth_device='F4:4E:FC:A8:34:10'
import shutil

class Mailbox:
    def clear_screen(self):
        os.system('CLS')
    def __init__(self,filename='data.zip',extract_dir='rsneo_images',retry_wait=1,skip_connectivity_test=False,retry_attempt=5):
        print('⏸️ Checking the connectivity to the compsys server...')        
        self.retry_count=0
        self.retry_attempt=retry_attempt
        if os.path.isfile(filename):
            os.remove(filename)
        if os.path.isdir(extract_dir):
            shutil.rmtree(extract_dir)
        print("✅ Previous data is gone now.")
        if skip_connectivity_test==False:
            print("🫸 Checking the connectivity to the comp sys raspberry pi.")
            while True:
                try:
                    response = requests.get('http://192.168.100.1/version',timeout=retry_wait)
                    if (response.status_code==200):
                        print("✅ Self connectivity test has succeeded:",response.text)
                        break
                except requests.exceptions.Timeout:
                    print("⛔ Failed to check the connectivity to the server due to the time out error, retry in {} second(s)".format(str(retry_wait)))
        else:
            print("🫡 Skipping connectivity test due to the option.")


        #self.clear_screen()
        self.extract_dir=extract_dir
        self.filename=filename
        # self.setup_socket()
        self.retry_wait=retry_wait
        self.image0_sent=False
        self.image1_sent=False
    def terminate_python(self):
        subprocess.run(['TASKKILL','/F','/IM','PYTHON.EXE'])

    def setup_socket(self):
        try:
            self.server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.server.bind((bluetooth_device,4))
            print('✅ Bluetooth device binded to the following device:', bluetooth_device)
            self.server.listen(1)
            print('⏸️ Waiting for the valid connection...')
            self.client, addr = self.server.accept()
            print('➡️ CONNECTION ESTABLISHED.')
        
        except OSError as e:
            print('⛔ Opening up socket failed.')
            print('➡️ Trying to close the previous socket.')
            try:
                self.client.close()
                self.server.close()
                print('✅ The previous socket closed successfully.')
            except AttributeError as nsa:
                print('⛔ Failed to close the previous socket.')
                print("⛔ Neither could open a socket nor close a socket. stuck.")
                print('⛔ Terminate all of the python process in 2 seconds.')
                print('⛔ Make sure that the bluetooth device:',bluetooth_device+' is connected and recognised by the OS properly.')
                time.sleep(2)
                self.terminate_python()
                sys.exit()


    def retrieve_package(self):
        try:
            self.size=int.from_bytes(self.client.recv(1024),'big')
            print('     💡 Received file size:', self.size)
            self.bs=int.from_bytes(self.client.recv(1024),'big')
            print('     💡 Received block size:', self.bs)
            self.md5=self.client.recv(1024).decode('UTF-8')
            print('     💡 Received MD5 hash: ',self.md5)
            self.last_chunk=self.size%self.bs
            self.number_of_chunks=math.floor(self.size/self.bs)
            
            received_data=b''
            rsize=0
            start=time.time()
            for _ in range(0,self.number_of_chunks):
                received_data+=self.client.recv(self.bs)
                print(rsize,end='\r')
                rsize+=self.bs
            received_data+=self.client.recv(self.last_chunk)
            with open(self.filename,'wb') as f:
                f.write(received_data)
            end=time.time()
            rhash=hashlib.md5(open(self.filename,'rb').read()).hexdigest()
            print('     💡 Calculated MD5 hash: ',rhash)
            print('     💡 The file has been received in: '+str(math.floor(end-start))+" second(s)")
            if rhash==self.md5:
                print("     ✅ MD5 validation confirmed.")
                self.client.send('OK'.encode('UTF-8'))
                print('✅ Sent the status: OK.')
            else:
                print("     💔 MD5 validation failed.")
                self.client.send('RESEND'.encode('UTF-8'))
                print('💔 Sent the status, RESEND')
                raise Exception('       ⛔ Failed to retrieve a package.')
        except Exception as e:
            #self.clear_screen()
            print('Failed to retrieve the package. Retry in {} seconds.'.format(str(self.retry_wait)))
            time.sleep(self.retry_wait)
            self.setup_socket()
            self.retrieve_package()

    def extract(self):
        if not os.path.exists(self.extract_dir):
            os.makedirs(self.extract_dir)
        # Extract the ZIP file to the output folder
        shutil.unpack_archive(self.filename, self.extract_dir)
    def upload(self):
        url = 'http://192.168.100.1/snap?id=164'
        image0 = self.extract_dir+'/'+'0.jpeg'
        image1 = self.extract_dir+'/'+'1.jpeg'
        image0_exists=os.path.isfile(image0)
        image1_exists=os.path.isfile(image1)
        sent_images=0
        while True:
            if image0_exists==True:
                try:
                    if self.image0_sent!=True:
                        with open(image0,'rb') as f:
                            response = requests.post(url, headers={'Content-Type': 'image/jpeg'}, data=f.read())
                        if  response.status_code==201:
                            self.image0_sent=True
                            sent_images+=1
                except Exception as e:
                    print('--- 💔 Failed to send an image to the comp sys, exception occurred!! --- ')
                    print(e)
                    print("--- 💔 Uploading exception log ended here ---")
            else:
                print("⚠️ Image 0 doesn't exists. Overwriting the flag to True.")
                self.image0_sent=True
            
            if image1_exists==True:
                try:
                    if self.image1_sent!=True:
                        with open(image1,'rb') as f:
                            response = requests.post(url, headers={'Content-Type': 'image/jpeg'}, data=f.read())
                        if response.status_code==201:
                            self.image1_sent=True
                            sent_images+=1
                except Exception as e:
                    print('--- 💔 Failed to send an image to the comp sys, exception occurred!! --- ')
                    print(e)
                    print("--- 💔 Uploading exception log ended here ---")
            else:
                print("⚠️ Image 1 doesn't exists. Overwriting the flag to True.")
                self.image1_sent=True
            

            if self.image1_sent==True and self.image0_sent==True:
                if sent_images==2:
                    print("✅ All images has been sent.")
                    input("🎉 All images has been sent, all good, all done, Yipee! (Enter to quit)")
                elif sent_images==1:
                    print("⚠️ 1 image has been sent.")
                    input("💡 1 image has been sent, uhm, what the sigma? (Enter to quit)")
                else:
                    print("😭 Seems like there are no images to be sent... 😭")
                    input("😭? Haiyaaa who was responsible for double loop... 😭?")
                
                break
            else:
                if self.retry_count<=self.retry_attempt:
                    print("⛔ Couldn't send images. retry in {} seconds, {} times remaining...".format(str(self.retry_wait),str(self.retry_attempt-self.retry_count)))
                    time.sleep(self.retry_wait)
                    self.retry_count+=1
                else:
                    print("💔 Unable to upload images to the server for {} times...".format(str(self.retry_attempt)))
                    print("😭 We had no luck... 😭")
                    break

if __name__=='__main__':
    Mailbox=Mailbox()
    #time.sleep(10)
    Mailbox.retrieve_package()
    Mailbox.extract()
    Mailbox.upload()
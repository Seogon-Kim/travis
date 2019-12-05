import os
import sys
from google.cloud import storage
from os.path import expanduser

class cloud_work:
    def __init__(self, instant_name = ""):

        self.upload_source_path = "io_test/upload"
        self.upload_destination = "~"
        self.download_source_path = "io_test/download"
        self.download_destination = "~"

        self._project_name = "cloud-sdk-project"
        self._zone = "us-east1-b"
        self._vm_instant_image = ""
        self._vm_instant_name = instant_name
        self._vm_instant_size = ""
        self._member_email = "user:theshawnsworld@gmail.com"
        self._member_name = ""
        self._role = "roles/compute.instanceAdmin"

        # self.vm_init()

    def waitforContinue(self):
        temp = input("Continue? [1. Yes; 2. No; q. Quit]    ")
        if (temp == "1"):
            return True
        elif (temp == "2"):
            return False
        else:
            sys.exit()

    def vm_init(self):
        os.system(
            "export GOOGLE_APPLICATION_CREDENTIALS='" + os.getcwd() + "/authKey.json'"
        )

    #-------------------------------Instance----------------------------------------------------------
    def vm_create(self):
        self._vm_instant_image = input("Which Operating System do you want to host on your Google Cloud VM: [1. Docker:BLAST  2. Ubuntu]]:    ")
        # self._vm_instant_size = input("Please Enter the size of disk you want to assign to:    ") 
        self._vm_instant_name = input("What do you want to call your Virtual Machine:    ")
        
        if (self._vm_instant_image == "1"):
            os.system(
                "gcloud compute instances create-with-container" + " " 
                + self._vm_instant_name + " " 
                + "--container-image" + " " 
                + "docker.io/biocontainers/blast:v2.2.31_cv2" + " "
                + "--container-restart-policy" + " " 
                + "on-failure" + " "
                + "--container-privileged" + " " 
                + "--zone" + " "
                + self._zone
            )
        elif (self._vm_instant_image == "2"):
            os.system(
                "gcloud compute instances create" + " " 
                + self._vm_instant_name + " "
                + "--image-family" + " "
                + "ubuntu-1804-lts" + " "
                + "--image-project" + " "
                + "gce-uefi-images" + " " 
                + "--zone" + " "
                + self._zone
            )
        else:
            print("Sorry, the seleting OS is currently not support yet")

    def vm_start(self, remote_instant_name):
        os.system(
            "gcloud compute instances start" + " "
            + remote_instant_name + " "
            + "--zone=" + self._zone
            )

    def vm_stop(self, remote_instant_name):
        os.system(
            "gcloud compute instances stop" + " "
            + remote_instant_name + " "
            + "--zone=" + "'"
            + self._zone + "'"
            )
    
    def vm_info(self):
        os.system(
            "gcloud compute instances describe" + " "
            + self._vm_instant_name + " "
            + "--zone=" + self._zone
            )
        os.system(
            "gcloud compute instances list"
            )

    #-------------------------------Instance----------------------------------------------------------

    #-------------------------------bucket----------------------------------------------------------

    def create_bucket(self, bucket_name):
        storage_client = storage.Client()
        bucket = storage_client.create_bucket(bucket_name)
    
    #-------------------------------bucket----------------------------------------------------------

    def user_update_info(self):
        self._member_name = input("**Please Enter your name**    ")
        self._member_email = "user:" + input("**Please Enter your email**    ")
        self._role = "roles/compute." + input("**who are you? [Such as: instanceAdmin; networkAdmin; networkUser]**    ")

        os.system(
            "gcloud compute instances add-iam-policy-binding" + " " 
            + self._vm_instant_name + " "
            + "--member=" + "'"
            + self._member_email + "'" + " "
            + "--role=" + "'"
            + self._role + "'" + " "
            + "--zone=" + "'"
            + self._zone + "'"
        )   

    def file_upload(self, local_path, remote_path, filetype = ""):
        if (filetype == "recurse"):
            os.system(
                "gcloud compute scp --recurse" + " " 
                + local_path + " " 
                + self._vm_instant_name + ":" 
                + remote_path + " "
                + "--zone=" + self._zone
            )
        else:
            os.system(
                "gcloud compute scp" + " " 
                + local_path + " " 
                + self._vm_instant_name + ":" 
                + remote_path + " "
                + "--zone=" + self._zone
            )

    def file_download(self, local_path, remote_path, filetype = ""):
        if (filetype == "recurse"):
            os.system(
                "gcloud compute scp --recurse" + " " 
                + self._vm_instant_name + ":"
                + remote_path + " " 
                + local_path + " "
                + "--zone=" + self._zone
            )
        else:
            os.system(
                "gcloud compute scp" + " " 
                + self._vm_instant_name + ":"
                + remote_path + " " 
                + local_path + " "
                + "--zone=" + self._zone
            )

    def ssh_control(self, remote_instant_name):
        os.system(
            "gcloud compute ssh --project" + " " 
            + self._project_name + " " 
            + "--zone" + " "
            + self._zone + " " 
            + remote_instant_name
        )

    def ssh_remote_exec(self, remote_instant_name, command):
        os.system(
            "gcloud compute ssh --project" + " " 
            + self._project_name + " " 
            + "--zone" + " "
            + self._zone + " " 
            + remote_instant_name + " "
            + "--command" + " "
            + "'" + command + "'"
        )

    def simple_command(self, command):
        os.system(
            command
        )

    ######################----------------TEST CODE----------------#####################

    def workflow(self):
        print("***********************************************")
        print("**************Welcome to workflow**************")
        print("***********************************************")

        print("")
        print("--------------Google Cloud VM Init--------------")
        print("")
        
        print("*")
        print("************You Will Create a VM Next***********")
        print("*")

        if (self.waitforContinue()):
            self.vm_create() #creat virturl machine

        print("*")
        print("************You will Start to the VM you just created***********")
        print("*")

        if (self.waitforContinue()):
            self.vm_start(self._vm_instant_name) #connect to VM

        print("*")
        print("************You will Display instance info***********")
        print("*")
        
        if (self.waitforContinue()):
            self.vm_info() # VM info

        print("*")
        print("************Above is Info on VM Instance***********")
        print("*")
        print("*")
        print("************" + self._vm_instant_name + " is successfully up and running!************")
        print("*")

        print("")
        print("--------------Bucket Init--------------")
        print("")

        print("*")
        print("************You Will be create a new bucket for storage***********")
        print("*")

        if (self.waitforContinue()):
            _bucket_name = input("What do you want to name your bucket:    ")
            self.create_bucket(_bucket_name) # create bucket
        
            print("*")
            print("************Bucket " + _bucket_name + " Successful Created***********")
            print("*")

        print("")
        print("--------------User authentication--------------")
        print("")

        print("*")
        print("************You Will be authorized to different role base on your choice***********")
        print("*")

        if (self.waitforContinue()):
            self.user_update_info() # user authentication

        print("")
        print("--------------File I/O Testing--------------")
        print("")

        print("*")
        print("************You will upload BLAST.py script to cloud for execution***********")
        print("*")

        if (self.waitforContinue()):
            # self.file_upload("io_test/upload/", "~/io_test/", "recurse") # upload test
            self.file_upload("blast.py", "~") #upload blast.py

        print("*")
        print("************Upload Successfully***********")
        print("*")

        print("*")
        print("************You will execute the blast workflow on cloud***********")
        print("*")

        if (self.waitforContinue()):
            self.ssh_remote_exec(self._vm_instant_name, "cd ~ && python blast.py")

        print("*")
        print("************You will download the BLAST result to your local folder***********")
        print("*")

        if (self.waitforContinue()):
            # self.file_download("io_test/download/", "~/io_test/", "recurse") # download test
            self.file_download("blast_result/", "~/blast_example/results.txt") # download result

        print("*")
        print("************Download Successfully***********")
        print("*")

        print("*")
        print("************you will print out the result.txt from BLAST execution***********")
        print("*")

        if (self.waitforContinue()):
            self.simple_command("cat blast_result/results.txt") # print result

        print("")
        print("--------------Remote SSH Control--------------")
        print("")

        print("*")
        print("************You will upload an script to VM for BLAST execution***********")
        print("*")
        # if (self.waitforContinue()):
            

        print("*")
        print("************You will SSH onto " + self._vm_instant_name + "***********")
        print("*")

        if (self.waitforContinue()):
            self.ssh_control(self._vm_instant_name) # remote SSH

    
    def ci_unit_test(self):
        print("------start")
        self.vm_start(self._vm_instant_name) #connect to VM
        print("------info")
        self.vm_info() # VM info
        print("------upload")
        self.file_upload(os.getcwd() + "/blast.py", "~") # upload blast script
        print("------exec0")
        self.ssh_remote_exec(self._vm_instant_name, "cd ~ && cat test.txt") # execute blast
        print("------exe1c")
        self.ssh_remote_exec(self._vm_instant_name, "cd ~ && python blast.py") # execute blast
        print("------download")
        self.file_download("blast_result/results.txt", "~/blast_example/results.txt") # download result
        print("------print")
        self.simple_command("cat blast_result/results.txt") # print result

    ######################^^^^^^^^^^^^^^^^^^^TEST CODE^^^^^^^^^^^^^^^^^^^#####################

if __name__ == '__main__':
    #############
    #   normal  #
    #############
    # workflow_obj = cloud_work()
    # workflow_obj.workflow()


    #############
    #  CI test  #
    #############
    workflow_obj = cloud_work("blast-vm")
    workflow_obj.ci_unit_test()
    
    #############
    # test code #
    #############

    # temp_name = "blast-vm"
    # workflow_obj._vm_instant_name = temp_name
    # workflow_obj.file_upload("io_test/upload/", "~/io_test/", "--recurse")
    # workflow_obj.ssh_control(temp_name)
    # workflow_obj.vm_connection_stop(temp_name)
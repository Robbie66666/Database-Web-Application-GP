#import cx_Oracle
import os
import sys 
import sshtunnel
import oracledb

class OracleDB(oracledb.Connection):
    oracle_instant_client_abs_path = r"C:\Users\14087\Desktop\WebClass\FinalProject\WebClass\flaskApp\instantclient_21_7"  # THIS HAS TO MATCH THE USERS

    try:
        if sys.platform.startswith("darwin"):
            lib_dir = os.path.abspath(oracle_instant_client_abs_path)
            oracledb.init_oracle_client(lib_dir=lib_dir)
        elif sys.platform.startswith("win32"):
            oracledb.init_oracle_client(lib_dir=oracle_instant_client_abs_path)
    except Exception as err:
        print(err)
        sys.exit(1)
    local_port = 1522
    ssh_username = 'psh9069'
    ssh_password = 'spsfall2022'
    remote_port = 1521
    remote_address = 'localhost'
    SID = 'app12c'
    db_username = 'MASY_PSH9069'
    db_password = 'MASY_PSH9069'
    #set the TNS
    dsn_tns = oracledb.makedsn(remote_address, local_port, SID)


    #create the ssh tunnel handler
    server = sshtunnel.SSHTunnelForwarder('workshop.sps.nyu.edu',##THIS IS THE SAME AS HAVING PUTTING AND YOUR ATTRIBUTES 
                                    ssh_username=ssh_username,
                                    ssh_password=ssh_password,
                                    remote_bind_address=(remote_address,
                                                        remote_port),
                                    local_bind_address=('', local_port))

    def __init__(self):
        self.server.start()##SAME AS RUNNING PUTTY
        super(OracleDB,self).__init__(user=self.db_username,password=self.db_password,dsn=self.dsn_tns)
    
    def get_connection(self):
        return self

    #when connection ends - stop ssh tunnel
    def __exit__(self, exc_type, exc_value, traceback):#THIS IS CLOSING OUT THE CONNECTION 
        self.server.stop()


    @staticmethod
    def test_connection():
        try:
            OracleDB().get_connection()
            return True
        except:
            return False
    
if __name__ =="__main__":
    with OracleDB().get_connection() as connection:##WITH CLAUSE OPENS THEN CLOSES,CALLS LINE 47 
        print('successs')
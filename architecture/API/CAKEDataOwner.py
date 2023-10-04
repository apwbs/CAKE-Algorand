    
from hashlib import sha512
from decouple import config
from CAKEBridge import CAKEBridge
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class CAKEDataOwner(CAKEBridge):
    """Tools to communicate from the API to the CAKE SDM server

    A class to manage the communication with the CAKE SDM server

    Attributes:
        manufacturer_address (str): manufacturer address
    """


    def __init__(self, process_instance_id = config('PROCESS_INSTANCE_ID'), row_id = -1):
        """Initialize the CAKEDataOwner class

        Args:
            process_instance_id (int, optional): process instance id. Defaults to config('PROCESS_INSTANCE_ID').
        """
        super().__init__("files/data_owner/data_owner.db", port=int(config('SDM_PORT')), process_instance_id=process_instance_id)
        self.manufacturer_address = config('ADDRESS_MANUFACTURER')
        self.row_id = row_id
        return
    
    def send(self, msg):
        """Send a message to the CAKE SDM server

        Send a message to the CAKE SDM server and receive a response

        Args:
            msg (str): message to send
        """
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)
        receive = self.conn.recv(6000).decode(self.FORMAT)
        if receive.startswith('Number to be signed: '):
            len_initial_message = len('Number to be signed: ')
            self.x.execute("INSERT OR IGNORE INTO handshake_number VALUES (?,?,?)",
                    (self.process_instance_id, self.manufacturer_address, receive[len_initial_message:]))
            self.connection.commit()
        if receive.startswith('Here is the message_id: '):
            received_messages =receive.split('\n')
            #print("received message: ", received_messages)
            len_initial_message = len('Here is the message_id: ')
            self.x.execute("INSERT OR IGNORE INTO messages VALUES (?,?,?)", (self.process_instance_id, self.manufacturer_address, received_messages[0][len_initial_message:]))
            self.connection.commit()
            #print("Received message_id: ", received_messages[0][len_initial_message:])
            if self.row_id != -1:
                message_id = received_messages[0][len_initial_message:]
                len_initial_message = len('Here is the ipfs_link: ')
                ipfs_link = received_messages[1][len_initial_message:]
                len_initial_message = len('Here are the slices: ')
                slices = received_messages[2][len_initial_message:]
                len_initial_message = len('Here is the tx_id: ')
                tx_id = received_messages[3][len_initial_message:]
                #return message_id, ipfs_link, slices, tx_id
                conn = psycopg2.connect(
                    host="172.18.0.3",
                    port = 5432,
                    database="postgres",
                    user="root",
                    password="root"
                )
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                curs = conn.cursor()
                print("Slices: ", slices)  
                curs.execute('UPDATE public."CAKE-1" SET "Message_id"=' + "'" + str(message_id) + "', " 
                            + '"IPFS link"=' + "'" + str(ipfs_link) + "', " 
                            + '"Slices"=' + "'" + str(slices) + "', " 
                            + '"TX_ID"=' + "'" + tx_id + "'" 
                            + ' WHERE "ID" =' +"'" + str(self.row_id) + "'")

                conn.commit()
                curs.close()

        #if receive.startswith('Here is the slices:'):

    def handshake(self):
        """Handshake with the CAKE SDM server"""
        self.send("Start handshake§" + self.manufacturer_address)
        self.disconnect()
        return
    
    def cipher_data(self, message_to_send, entries_string, policy_string):
        """Cipher a message and set the policy
        
        Args:
            message_to_send (str): message to send 
            entries_string (str): entries converted to string
            policy_string (str): policy converted to string"""
        signature_sending = self.sign_number()
        self.send("Cipher this message§" + message_to_send + '§' + entries_string + '§' + policy_string + '§' + self.manufacturer_address   + '§' + str(signature_sending))
        self.disconnect()
        return
    
    def sign_number(self):
        """Sign a number

        Sign a number and return the signature

        Returns:
            str: signature
        """
        #print("Process instance id:", self.process_instance_id)
        self.x.execute("SELECT * FROM handshake_number WHERE process_instance=?", (self.process_instance_id,))
        result = self.x.fetchall()
        number_to_sign = result[0][2]
        return super().sign_number(number_to_sign, self.manufacturer_address)
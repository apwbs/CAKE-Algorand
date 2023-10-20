message_id='12496037049958863058' #substitute with your message id
reader_address='Y7HF66E3VR2CE7A3MADJLUPWBMD423MKJ2WSAQ24NVIAIAW2PSCA3B6EGU' #substitute with your reader address
reader_address='JYMAAYEYFR3FJKNGKZPYXOG2KOUAGMAU2KFJHRAAZI3B3WNPQYM4MPQZFA'
slice_id='8042455261785484164' #subsitute with your slice id


python3 client.py --handshake --message_id $message_id --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -ad --message_id $message_id --reader_address $reader_address --slice_id $slice_id
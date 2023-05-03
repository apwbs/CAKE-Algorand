message_id='6124483552192210119'
reader_address='MEDEZGMMSDFUBBWSMVDNN3HGL44SS7OPIDAC4H6SMPRWRBAXIM2SHEN3Z4'
#reader_address='0x81215eEC040673dB5131f40184477091747ea4A8'
slice_id='15275063936807116589'


python3 client.py --handshake --message_id $message_id --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -ad --message_id $message_id --reader_address $reader_address --slice_id $slice_id

#slice id: 6678072391299123667
#slice id: 13635621019063986383
#slice id: 10450506680882014878
#message id: 6780287944816327166
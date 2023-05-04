message_id='15216642079681679070'
reader_address='S4HU4ZINJ5YHL2OBW3VM6S5HLKRSRR2XWPVDFMHGEKR5TVHV2VOFLOEWGE'
slice_id='10275806781444632806'


python3 client.py --handshake --message_id $message_id --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -ad --message_id $message_id --reader_address $reader_address --slice_id $slice_id

#slice id: 15172667245773369765
#slice id: 16409657303025412222
#slice id: 10275806781444632806
#message id: 15216642079681679070
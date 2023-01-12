CREATE TABLE decription_keys ( 
    process_instance TEXT,
    message_id TEXT,
    ipfs_message_link TEXT,
    decription_key TEXT,
    primary key (process_instance, message_id)
);

CREATE TABLE plaintext ( 
    process_instance TEXT,
    message_id TEXT,
    slice_id TEXT,
    plaintext TEXT,
    salt TEXT,
    primary key (process_instance, message_id)
);

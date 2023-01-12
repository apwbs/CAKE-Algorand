CREATE TABLE decription_keys ( 
    process_instance TEXT,
    decription_key TEXT,
    primary key (process_instance)
);

CREATE TABLE ipfs_links ( 
    process_instance TEXT,
    message_id TEXT,
    ipfs_link TEXT,
    primary key (process_instance, message_id)
);

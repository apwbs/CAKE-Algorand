CREATE TABLE rsa_public_key (
    reader_address TEXT,
    ipfs_file_link_hash TEXT,
    publicKey TEXT,
    primary key (reader_address)
);

CREATE TABLE rsa_private_key (
    reader_address TEXT,
    privateKey TEXT,
    primary key (reader_address)
);

CREATE TABLE generated_key_reader (
    process_instance_id TEXT,
    reader_address TEXT,
    secret_key TEXT,
    primary key (process_instance_id, reader_address)
);

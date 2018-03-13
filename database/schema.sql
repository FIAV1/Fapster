PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS peers;
CREATE TABLE peers (
    session_id char(16) PRIMARY KEY,
    ip char(55) NOT NULL,
    port char(5) NOT NULL
);

DROP TABLE IF EXISTS files;
CREATE TABLE files (
    id integer PRIMARY KEY,
    file_md5 char(32) NOT NULL,
    file_name char(100) NOT NULL,
    download_count integer DEFAULT 0
);

DROP TABLE IF EXISTS files_peers;
CREATE TABLE files_peers (
    file_id integer NOT NULL,
    peer_session_id char(16) NOT NULL,
    PRIMARY KEY (file_id, peer_session_id),
    FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE,
    FOREIGN KEY (peer_session_id) REFERENCES peers (session_id) ON DELETE CASCADE
);

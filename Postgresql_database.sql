-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2017-03-28 17:32:39.881

-- tables
-- Table: categories
CREATE TABLE categories (
    cat_id SERIAL  NOT NULL,
    cat_name varchar(255)  NOT NULL,
    CONSTRAINT categories_pk PRIMARY KEY (cat_id)
);

-- Table: comments
CREATE TABLE comments (
    comment_id SERIAL  NOT NULL,
    user_id int  NOT NULL,
    post_id int  NOT NULL,
    content text  NOT NULL,
    created timestamp  NOT NULL,
    CONSTRAINT comments_pk PRIMARY KEY (comment_id)
);

-- Table: posts
CREATE TABLE posts (
    post_id SERIAL  NOT NULL,
    title varchar(255)  NOT NULL,
    content text  NOT NULL,
    created timestamp  NOT NULL,
    updated timestamp  NULL,
    user_id int  NOT NULL,
    cat_id int  NOT NULL,
    CONSTRAINT posts_pk PRIMARY KEY (post_id)
);

-- Table: users
CREATE TABLE users (
    user_id SERIAL  NOT NULL,
    user_name varchar(255)  NOT NULL,
    hash_pwd char(255)  NOT NULL,
    full_name varchar(255)  NOT NULL,
    active int  NOT NULL,
    CONSTRAINT users_pk PRIMARY KEY (user_id)
);




-- foreign keys
-- Reference: comments_posts (table: comments)
ALTER TABLE comments ADD CONSTRAINT comments_posts
    FOREIGN KEY (post_id)
    REFERENCES posts (post_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: comments_users (table: comments)
ALTER TABLE comments ADD CONSTRAINT comments_users
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: posts_categories (table: posts)
ALTER TABLE posts ADD CONSTRAINT posts_categories
    FOREIGN KEY (cat_id)
    REFERENCES categories (cat_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: posts_users (table: posts)
ALTER TABLE posts ADD CONSTRAINT posts_users
    FOREIGN KEY (user_id)
    REFERENCES users (user_id)
    ON DELETE  CASCADE 
    ON UPDATE  CASCADE 
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.


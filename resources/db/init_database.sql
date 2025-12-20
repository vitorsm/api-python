
CREATE TABLE "user" (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,

    PRIMARY KEY (id)
);

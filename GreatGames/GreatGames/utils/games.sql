DROP TABLE IF EXISTS Games CASCADE;

CREATE TABLE IF NOT EXISTS Games(
    pk serial unique not null PRIMARY KEY,
    genre varchar(50),
    title varchar(100),
    edition varchar(30),
    description TEXT,
    release DATE,
    price float,
    rating DECIMAL(3, 1)
);

DELETE FROM Games;

CREATE INDEX IF NOT EXISTS games_index
ON Games (genre, title, edition);

DROP TABLE IF EXISTS Sell;

CREATE TABLE IF NOT EXISTS Sell(
    developer_pk int not null REFERENCES Developers(pk) ON DELETE CASCADE,
    games_pk int not null REFERENCES Games(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (developer_pk, games_pk)
);

CREATE INDEX IF NOT EXISTS sell_index
ON Sell (developer_pk, available);

DELETE FROM Sell;

DROP TABLE IF EXISTS GameOrder;

CREATE TABLE IF NOT EXISTS GameOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    developer_pk int not null REFERENCES Developers(pk) ON DELETE CASCADE,
    games_pk int not null REFERENCES Games(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM GameOrder;

CREATE OR REPLACE VIEW vw_games
AS
SELECT p.genre, p.title, p.edition,
       p.rating, p.price, s.available,
       p.description,
       p.pk as game_pk,
       f.full_name as developer_name,
       f.pk as developer_pk
FROM Games p
JOIN Sell s ON s.games_pk = p.pk
JOIN Developers f ON s.developer_pk = f.pk
ORDER BY available, p.pk;
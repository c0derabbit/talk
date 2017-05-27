drop table if exists messages;
create table messages(
  id serial primary key,
  sender text not null,
  receiver text not null,
  sent_at text not null,
  message text not null
);

drop table if exists users;
create table users(
  id serial primary key,
  username text not null,
  password bytea not null
);

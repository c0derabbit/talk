drop table if exists messages;
create table messages(
  id integer primary key autoincrement,
  sender text not null,
  receiver text not null,
  sent_at text not null,
  message text not null
);

drop table if exists users;
create table users(
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

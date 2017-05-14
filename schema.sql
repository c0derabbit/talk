drop table if exists messages;
create table messages(
  id integer primary key autoincrement,
  sender text not null,
  receiver text not null,
  sent_at text not null,
  message text not null
);

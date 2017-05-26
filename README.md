# talk
#### a chat app for two

---

##### To run locally:

```sh
. venv/bin/activate
pip install -r requirements.txt
sqlite3 /tmp/talk.db < schema.sql
export FLASK_APP=talk.py && export FLASK_DEBUG=1 && flask run
```

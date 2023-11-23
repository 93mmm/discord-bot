# discord-bot

### database structure
```SQL
CREATE TABLE "Users" (
	"UserID"	INTEGER NOT NULL UNIQUE,
  "SpecialSigns" TEXT DEFAULT "",
	"SocialPoints"	INTEGER DEFAULT 0,
  "PhotoCards" TEXT DEFAULT "",
	PRIMARY KEY("UserID")
);
```

### requirements:
```bash
pip3 install -r requirements.txt
```
get your token and server id, paste it into `src/const.py` folder

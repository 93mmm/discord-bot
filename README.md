# discord-bot

### configure environment
```bash
make env
```

### install:
```bash
make install
```

> **get your token and server id, paste it into** [`src/helpers/const.py`](https://github.com/93mmm/discord-bot/blob/main/src/helpers/const.py) **folder**

### run
```bash
make run
```

### database structure
```SQL
CREATE TABLE "Users" (
  "UserID"        INTEGER NOT NULL UNIQUE,
  "SpecialSigns"  TEXT DEFAULT "",
  "SocialCredits" INTEGER DEFAULT 0,
  "IsInfinity"    INTEGER DEFAULT 0,
  "Badges"        TEXT DEFAULT "",
  PRIMARY KEY("UserID")
);
```

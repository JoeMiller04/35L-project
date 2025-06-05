# 35L-project

UCLA CS 35L Project. Group members are Arian Dehnavizadeh, Johnny Duong, Samuel Oh, Joseph Miller, Kyle Reisinger.

## Getting Started

This project requires MongoDB to be installed and running.

**Clone with:**

```
git clone https://github.com/JoeMiller04/35L-project.git
cd 35L-project
git switch production
git pull origin
```

**Create Conda Environment**

```
conda create --name NAME python=3.13
conda activate NAME
pip install -r requirements.txt
```

**Set Up With Make**

To load python dependencies

```
make deps
```

To load data into MongoDB

```
make load-db
```

To start client and server

```
make start
```

To check, go to http://localhost:3000/

**App Information**
App information and functionality is described in `client/README.md`

**Backend Information**
See `server/README.md` for more info

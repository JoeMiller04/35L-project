# 35L-project

UCLA CS 35L Project. Group members are Arian Dehnavizadeh, Johnny Duong, Samuel Oh, Joseph Miller, Kyle Reisinger.

## Getting Started

Make sure you Docker installed.

**Clone with:**

```
git clone https://github.com/JoeMiller04/35L-project.git
cd 35L-project
```

**Build Backend Docker Image:**

```
docker build -t my-backend -f server/Dockerfile .
```

**Run Backend Container:**

```
docker run -d --name backend -p 8000:8000 my-backend
```

**To Check:**

```
docker logs backend
```

Should say: "Server.py ran"

**Build and Run Frontend:**

```
docker build -t my-frontend ./client
docker run -d --name frontend -p 3000:3000 my-frontend
```

**Create Conda Environment**

```
conda create --name NAME python=3.13
conda activate NAME
pip install -r requirements.txt
```

To check, go to http://localhost:3000/

**Backend Information**
See `server/README.md` for more info

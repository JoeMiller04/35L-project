# 35L-project
UCLA CS 35L Project. Group members are Arian Dehnavizadeh, Johnny Duong, Samuel Oh, Joseph Miller, Kyle Reisinger.

## Getting Started
Make sure you Docker installed.

**Clone with:**
```
git clone git@github.com:JoeMiller04/35L-project.git
cd 35L-project
```

**Build Docker Image:**
```
docker build -t my-backend ./server
```

**Run Container:**
```
docker run -d --name backend -p 5000:5000 my-backend
```

**To Check:**
```
docker logs backend
```

Should say:
```
Server.py ran
```

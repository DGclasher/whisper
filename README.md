# WhisPer!

## Description

Whisper is a chat application built using Flask and Socket.IO. It allows users to register and login, create and join chat rooms, and chat with other users in real-time. The application uses MongoDB as the backend database to store user information, chat messages, and room details.

## Deploy Locally

Make a `.env` file with contents
```
MONGO_URI=<MongoDB connection URL>
DB=<Database Name>
```

Pull image from docker hub
```
sudo docker pull dgclasher/whisper
```

Run the container
```
sudo docker run --rm --name whisper --env-file /path/to/.env -p 5000:5000 -d dgclasher/whisper
```

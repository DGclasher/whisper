# WhisPer!

## Description

Whisper is a chat application built using Flask and Socket.IO. It allows users to register and login, create and join chat rooms, and chat with other users in real-time. The application uses MongoDB as the backend database to store user information, chat messages, and room details.

## Deploy Locally

Make a `.env` at root of project, refer to [this](./.env.example) for creating `.env`.

Pull image from docker hub
```
sudo docker pull dgclasher/whisper
```

Run the container
```
sudo docker run --rm --name whisper --env-file /path/to/.env -p 5000:5000 -d dgclasher/whisper
```

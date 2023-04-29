# WhisPer!

## Description

Whisper is a chat application built using Flask and Socket.IO. It allows users to register and login, create and join chat rooms, and chat with other users in real-time. The application uses MongoDB as the backend database to store user information, chat messages, and room details.

Whisper also includes features such as password hashing for secure storage of user passwords, session management for user authentication, and error handling to provide a smooth user experience.

## Access the application

### The application is deployed [here](https://whisper-cq4x.onrender.com/)
Note: The deployed application deletes users after 24 hours, if you don't want that, you can spin this application in your local environment

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
sudo docker run --env-file /path/to/.env -p 5000:5000 -d dgclasher/whisper
```

# Big Brother's Watch
![image](https://github.com/user-attachments/assets/7ea38e44-a3e9-4f1e-be63-ff3970755a10)

This is a game that detects the user's face and allows them to control the movement of the player in the game using left/right head movements. I was inspired by the book 1984 by George Orwell as I was in the process of reading it at the time of the creation of this game. In this game, the player must avoid the 'eye', which symbolizes surveillance and capture the 'journal', which represents autonomy and freedom of thought. Hitting an eye will instantly end the game, while collecting journals increases the player's score. I implemented an object-oriented design for this project. 
___
## Libraries Used
- Mediapipe
- CV2
- Pygame
- Threading

___
## Methods

I utilized Mediapipe, a library containing various pre-trained models for major vision-related tasks. In my case, I used the short-range BlazeFace model for face detection. The model’s lightweight nature and high accuracy were ideal for my game, ensuring smooth and fast responses. I used CV2 for Python to get the user’s webcam information. This information was then passed on to the BlazeFace model, from which I continuously obtained the x-coordinates of the player’s head position.

Pygame was my main library for the game’s user interface and game mechanics.

Finally, I used threading to prevent latency and run the motion detection thread and game thread asynchronously.
 

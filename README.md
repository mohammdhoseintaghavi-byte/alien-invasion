\# Alien Invasion



A Python arcade game built with Pygame, based on the Alien Invasion project from \*Python Crash Course\* by Eric Matthes.



This project was developed as a learning exercise to practice Python programming, object-oriented programming, and game development. It also includes additional features and modifications beyond the original tutorial.



\## Features



\- Player-controlled spaceship

\- Alien enemies and projectile shooting

\- Boss enemy with a health bar

\- Three difficulty levels: Easy, Medium, and Hard

\- Score tracking and high-score saving

\- Multiple sound effects

\- Increasing game difficulty as levels progress



\## Controls



| Key | Action |

|---|---|

| Left Arrow | Move left |

| Right Arrow | Move right |

| Space | Shoot |

| P | Restart the game |

| Q | Quit the game |



\## Technologies



\- Python 3.12

\- Pygame 2.6.1

\- Object-Oriented Programming (OOP)



\## Installation



1\. Clone or download this repository.

2\. Make sure Python 3.12 or a compatible version is installed.

3\. Install the required dependency:



```bash

pip install -r requirements.txt

```



\## How to Run



Run the following command from the project directory:



```bash

python alien\\\_invasion.py

```



\## Project Structure



```text

alien-invasion-portfolio/

│

├── alien\\\_invasion.py

├── paths.py

├── settings.py

├── game\\\_stats.py

├── scoreboard.py

├── button.py

├── ship.py

├── bullet.py

├── alien.py

├── boss.py

├── boss\\\_bullet.py

│

├── assets/

│   ├── images/

│   │   ├── ship.bmp

│   │   ├── alien.bmp

│   │   └── boss.bmp

│   │

│   └── sounds/

│       ├── shoot.wav

│       ├── explosion.wav

│       ├── hit.wav

│       └── game\\\_over.wav

│

├── requirements.txt

├── .gitignore

└── README.md

```



\## Learning Objectives



Through this project, I practiced:



\- Organizing a Python application into multiple modules

\- Working with classes and object-oriented programming

\- Managing game events and user input

\- Handling images, sounds, and external assets

\- Using file paths to organize project resources

\- Saving and loading data using JSON

\- Structuring a project for version control and GitHub



\## Acknowledgment



This project is based on the Alien Invasion project from:



\*\*Python Crash Course, 3rd Edition\*\* by Eric Matthes.



The original book and tutorial provided the foundation for the project. Additional modifications include the boss enemy, difficulty selection, and sound effects.



This is an educational project and is not presented as an entirely original game developed from scratch.


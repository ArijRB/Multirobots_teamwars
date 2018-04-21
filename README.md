# General information

pySpriteWorld_multirobots: a multirobot simulation tools for Python. This is a fork from Yann Chevaleyre's pySpriteWorld. It is meant for quick and easy implementation of simplistic multi-robots experimental setup. It is also not particularly clean, but still remains very easy to understand and use.

The core is __exactly__ the same as Yann Chevaleyre's pySpriteWorld (as of march 2018), with files removed for clarity and with added files that wraps around pySpriteWorld to turn it into a multirobot simulator (mostly, this means writing an interface that looks like what you may expect from a (crude) robot simulator). That's all. This project is made available mostly for my students. 

Description of added content:

 * multirobots.py: a template for a multirobot setup. Each robot wanders randomly in the arena.

 * multirobots_teamwars.py: a capture-the-flag/patrolling challenge with two 4-robots teams playing against each other. Each robot explores the environment. 

 * robot_randomsearch.py: a template for implementing evolutionary robotics. Currently: super fast random exploration of a search space defined as motor outputs computed from a weighted combination of sensory inputs. Evaluate and store best candidate wrt to getting as far as possible from the center arena. Reinitialize (incl. reposition and reset parameters) inbetween each trial.

Contact author for robot modules: nicolas.bredeche(at)sorbonne-universite.fr

Original pySpriteWorld project: https://github.com/yannche/pySpriteWorld/ (author: Yann Chevaleyre). Note that pySpriteWorld also implement a discrete world setup. Check github project.

## Usage and dependances:

Dependencies:
 * python version 2.7 -> version 3.5
 * pygame

Usage: python multirobots.py (or: multirobots_teamwars.py, or: robot_randomsearch.py)

pySpriteWorld_multirobots uses Python 2.x, but can be easily ported to Python 3.x (the core is compatible with both versions)

## Additional information

Quoted (and translated) from the original pySpriteWorld README.md.

Graphics come from http://opengameart.org/content/tiny-16-basic and some code was taken from http://programarcadegames.com/index.php

Maps (i.e. arenas) must be build with Tiled software ( http://www.mapeditor.org ), and exported to json format.

A map is organized by layers. By convention, each layer must be named from one of the following: "bg1","bg2","obstacle","ramassable","joueur"

Each layer follows its own conventions:

  * "bg1" and "bg2" layers are background, and are just there to make things look nice (i.e. robots do not interact with these layers). bg1 is displayed before bg2.

  * the "obstacle" layer contains all objects that cannot be moved (or taken). e.g.: walls, water, etc.

  * the "ramassable" layer contains object that can be taken with the "ramasse" command (translation: "get_object"). Can later be "depose" in front of the robot (translation: "drop_object"). This is *not* used in pySpriteWorld_multirobots.

  * the "joueur" layer contains the robot(s). Robot cannot overlap.


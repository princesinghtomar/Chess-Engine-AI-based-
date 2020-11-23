# Chess Engine with AI bot

## Overview

The project is a chess game with where user can play Player vs Player or Player vs Computer chess. User can both the traditional chess or the Chess960 version of it. Both the engine and the AI is implemented by us with no chess libraries involved in our main project.

We also explored some naive algorithms of chess which are not meant to be used to play against a human but were tried for just analysis point of view. The `simple_algos` folder is for that side project only.

## Instructions to play main chess game

> `pygame` is required to run the code. Install it by : `pip3 install pygame`.

Main chess game is in the Chess directory.  
`cd` into it and then run:  
`python3 ChessMain.py`.

Follow the instructions on the screen and click on the options you want to select.

There are 5 options:

1. PvP Normal Chess
2. PvP Fischer Chess
3. Custom Board
4. PvC Normal Chess
5. PvC Fischer Chess

> Note: The Custom Board option is for debugging and not for playing. Don't select that.

+ You will be prompted to enter inputs in the command line in two scenarios:  
  + If a player has to promote it's pawn then the promoting piece type would be required to enter though terminal (Q/N/R/B).

Enjoy the game!!

> Some tweaks possible (one can find the variables at the top of the `minimax.py`):
>
> + `timeout`: It is the time which AI will generally take to calculate a move.
> + `initial_depth`: It is the initial depth of the decision tree which AI will calculate. If time permits then AI computes fruther depths. Keep it at `4` for best experience.

### Instructions to run side project

> `python-chess` is required to run the side project. Install it by : `pip3 install pygame`.

To run the side project, `cd` into `simple_algos` and run `python3 simulate.py`

It can take some time to run and will return win scores and elo ratings of the different algorithms.

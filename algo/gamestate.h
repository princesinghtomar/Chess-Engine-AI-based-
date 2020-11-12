#include "move.h"
#include <iostream>
#include <map>
#include <vector>
using namespace std;

class GameState;

class GameState {
public:
	char board[8][8][3];
	bool whiteToMove;
	vector<Move> moveLog;
	int wking_pos[2];
	int bking_pos[2];
	bool inCheck; // in check is a var

	/* For these vars i am not sure of the type so uncomment when need and fill inside <>
	vector<> pins;
	vector<> checks;
	vector<>enpassantPossible;
	 */

	//funcs
	vector<Move> get_legal_moves();
	vector<Move> get_all_poss_moves();
	bool is_game_over();
	void push(Move); // eq to makemove
	Move pop();		 // eq to undomove
	bool is_sq_under_attack(int row, int col);
	void getPawnMoves(int row, int col, vector<Move> &moves);
	void getRookMoves(int row, int col, vector<Move> &moves);
	void getKnightMoves(int row, int col, vector<Move> &moves);
	void getBishopMoves(int row, int col, vector<Move> &moves);
	void getKingMoves(int row, int col, vector<Move> &moves);
	void getQueenMoves(int row, int col, vector<Move> &moves);

	/* 
	void checkForPinsAndChecks(bool inCheck,vector<>& pins, vector<>&checks)
	 */
};
const map < char, void (*)(int, int, vector<Move> &) move_funcs = {
					  {'p' : GameState::getPawnMoves},
					  {'R' : GameState::getRookMoves},
					  {'N' : GameState::getKnightMoves},
					  {'B' : GameState::getBishopMoves},
					  {'K' : GameState::getKingMoves},
					  {'Q' : GameState::getQueenMoves}};

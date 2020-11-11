#include <climits>
#include <ctime>
#include <functional>
#include <iostream>
#include <vector>
using namespace std;

#define SCORE_MAX INT_MAX
#define SCORE_MIN INT_MIN

class Move {
public:
	int temp;
	bool is_null(){};
};

class Board {
public:
	int temp;
	vector<Move> legal_moves();
	bool is_game_over();
	void push(Move);
	Move pop();
};

Move final_move;
int timeout = 3 * CLOCKS_PER_SEC, stime;

int evaluate(const Board &board);

int minimax(Board &board, int alpha, int beta, bool maximizer, int cur_depth, int max_depth, Move &ret_move);

int next_move_restricted(Board &board, int max_depth, Move &ret_move);

Move next_move(Board &board);

Move next_move(Board &board) {
	int initial_depth = 4,
		max_depth_lim = 10;
	final_move = Move(); // a null move
	stime = clock();
	if (board.is_game_over()) {
		return Move();
	}
	Move final_move;
	int final_score = next_move_restricted(board, initial_depth, final_move);

	for (int depth = initial_depth + 1; depth <= max_depth_lim; depth++) {
		if (clock() - stime > timeout)
			break;
		Move move;
		int score = next_move_restricted(board, depth, move);
		if (!move.is_null() && score > final_score) {
			final_score = score;
			final_move = move;
		}
	}
	return final_move;
}

int next_move_restricted(Board &board, int max_depth, Move &ret_move) {
	int score = minimax(board, SCORE_MIN, SCORE_MAX, true, 0, max_depth, ret_move);
	if (ret_move.is_null())
		score = SCORE_MIN;
	return score;
}

int minimax(Board &board, int alpha, int beta, bool maximizer, int cur_depth, int max_depth, Move &ret_move) {
	if (board.is_game_over() || cur_depth == max_depth)
		return evaluate(board);

	//sending inf so that the branch is ignored by parent
	if (!final_move.is_null() && clock() - stime > timeout)
		return (maximizer ? SCORE_MAX : SCORE_MIN);

	auto moves = board.legal_moves();
	ret_move = Move();
	int best_score;
	bool (*is_better_score)(int, int);
	function<void(int)> update_AB;
	if (maximizer) {
		best_score = SCORE_MIN;
		is_better_score = [](int curr, int currbest) { return curr > currbest; };
		update_AB = [&](int score) { alpha = max(alpha, score); };
	} else {
		best_score = SCORE_MAX;
		is_better_score = [](int curr, int currbest) { return curr < currbest; };
		update_AB = [&](int score) { beta = min(beta, score); };
	}
	for (auto &move : moves) {
		board.push(move);
		Move temp;
		int score = minimax(board, alpha, beta, !maximizer, cur_depth + 1, max_depth, temp);
		board.pop();
		if (is_better_score(score, best_score)) {
			best_score = score;
			ret_move = move;
			update_AB(score);
			if (alpha >= beta)
				break;
		}
	}
	return best_score;
}

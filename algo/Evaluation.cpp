#include "Evaluation.h"
#include <string.h>

int pawn_value = 100;
int knight_value = 300;
int bishop_value = 300;
int rook_value = 500;
int queen_value = 900;
int king_value = 10000;

int pawn_phase_val = 0;
int knight_phase_val = 1;
int bishop_phase_val = 1;
int rook_phase_val = 2;
int queen_phase_val = 4;

struct eval_data
{
    char position[80];

    int wp, wr, wn, wb, wq;
    int bp, br, bn, bb, bq;
    int pos_wp[8];
    int pos_wr[8];

    // int BISHOP_PAIR;
    // int P_KNIGHT_PAIR;
    // int P_ROOK_PAIR;
    // int ROOK_OPEN;
    // int ROOK_HALF;
    // int P_BISHOP_TRAPPED_A7;
    // int P_BISHOP_TRAPPED_A6;
    // int P_KNIGHT_TRAPPED_A8;
    // int P_KNIGHT_TRAPPED_A7;
    // int P_BLOCK_CENTRAL_PAWN;
    // int P_KING_BLOCKS_ROOK;

    // int SHIELD_2;
    // int SHIELD_3;
    // int P_NO_SHIELD;

    // int RETURNING_BISHOP;
    // int P_C3_KNIGHT;
    // int P_NO_FIANCHETTO;
    // int FIANCHETTO;
    // int TEMPO;
    // int ENDGAME_MAT;
};
struct eval_data e;

int pawn_pcsq_mg[64] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    -6, -4, 1, 1, 1, 1, -4, -6,
    -6, -4, 1, 2, 2, 1, -4, -6,
    -6, -4, 2, 8, 8, 2, -4, -6,
    -6, -4, 5, 10, 10, 5, -4, -6,
    -4, -4, 1, 5, 5, 1, -4, -4,
    -6, -4, 1, -24, -24, 1, -4, -6,
    0, 0, 0, 0, 0, 0, 0, 0};

int pawn_pcsq_eg[64] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    -6, -4, 1, 1, 1, 1, -4, -6,
    -6, -4, 1, 2, 2, 1, -4, -6,
    -6, -4, 2, 8, 8, 2, -4, -6,
    -6, -4, 5, 10, 10, 5, -4, -6,
    -4, -4, 1, 5, 5, 1, -4, -4,
    -6, -4, 1, -24, -24, 1, -4, -6,
    0, 0, 0, 0, 0, 0, 0, 0};

int knight_pcsq_mg[64] = {
    -8, -8, -8, -8, -8, -8, -8, -8,
    -8, 0, 0, 0, 0, 0, 0, -8,
    -8, 0, 4, 4, 4, 4, 0, -8,
    -8, 0, 4, 8, 8, 4, 0, -8,
    -8, 0, 4, 8, 8, 4, 0, -8,
    -8, 0, 4, 4, 4, 4, 0, -8,
    -8, 0, 1, 2, 2, 1, 0, -8,
    -8, -12, -8, -8, -8, -8, -12, -8};

int knight_pcsq_eg[64] = {
    -8, -8, -8, -8, -8, -8, -8, -8,
    -8, 0, 0, 0, 0, 0, 0, -8,
    -8, 0, 4, 4, 4, 4, 0, -8,
    -8, 0, 4, 8, 8, 4, 0, -8,
    -8, 0, 4, 8, 8, 4, 0, -8,
    -8, 0, 4, 4, 4, 4, 0, -8,
    -8, 0, 1, 2, 2, 1, 0, -8,
    -8, -12, -8, -8, -8, -8, -12, -8};
int bishop_pcsq_mg[64] = {
    -4, -4, -4, -4, -4, -4, -4, -4,
    -4, 0, 0, 0, 0, 0, 0, -4,
    -4, 0, 2, 4, 4, 2, 0, -4,
    -4, 0, 4, 6, 6, 4, 0, -4,
    -4, 0, 4, 6, 6, 4, 0, -4,
    -4, 1, 2, 4, 4, 2, 1, -4,
    -4, 2, 1, 1, 1, 1, 2, -4,
    -4, -4, -12, -4, -4, -12, -4, -4};

int bishop_pcsq_eg[64] = {
    -4, -4, -4, -4, -4, -4, -4, -4,
    -4, 0, 0, 0, 0, 0, 0, -4,
    -4, 0, 2, 4, 4, 2, 0, -4,
    -4, 0, 4, 6, 6, 4, 0, -4,
    -4, 0, 4, 6, 6, 4, 0, -4,
    -4, 1, 2, 4, 4, 2, 1, -4,
    -4, 2, 1, 1, 1, 1, 2, -4,
    -4, -4, -12, -4, -4, -12, -4, -4};
int rook_pcsq_mg[64] = {
    5, 5, 5, 5, 5, 5, 5, 5,
    20, 20, 20, 20, 20, 20, 20, 20,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 2, 2, 0, 0, 0};

int rook_pcsq_eg[64] = {
    5, 5, 5, 5, 5, 5, 5, 5,
    20, 20, 20, 20, 20, 20, 20, 20,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 2, 2, 0, 0, 0};
int queen_pcsq_mg[64] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 0, 0,
    0, 0, 1, 2, 2, 1, 0, 0,
    0, 0, 2, 3, 3, 2, 0, 0,
    0, 0, 2, 3, 3, 2, 0, 0,
    0, 0, 1, 2, 2, 1, 0, 0,
    0, 0, 1, 1, 1, 1, 0, 0,
    -5, -5, -5, -5, -5, -5, -5, -5};

int queen_pcsq_eg[64] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 1, 1, 0, 0,
    0, 0, 1, 2, 2, 1, 0, 0,
    0, 0, 2, 3, 3, 2, 0, 0,
    0, 0, 2, 3, 3, 2, 0, 0,
    0, 0, 1, 2, 2, 1, 0, 0,
    0, 0, 1, 1, 1, 1, 0, 0,
    -5, -5, -5, -5, -5, -5, -5, -5};

int king_pcsq_mg[64] = {
    -40, -30, -50, -70, -70, -50, -30, -40,
    -30, -20, -40, -60, -60, -40, -20, -30,
    -20, -10, -30, -50, -50, -30, -10, -20,
    -10, 0, -20, -40, -40, -20, 0, -10,
    0, 10, -10, -30, -30, -10, 10, 0,
    10, 20, 0, -20, -20, 0, 20, 10,
    30, 40, 20, 0, 0, 20, 40, 30,
    40, 50, 30, 10, 10, 30, 50, 40};

int king_pcsq_eg[64] = {
    -72, -48, -36, -24, -24, -36, -48, -72,
    -48, -24, -12, 0, 0, -12, -24, -48,
    -36, -12, 0, 12, 12, 0, -12, -36,
    -24, 0, 12, 24, 24, 12, 0, -24,
    -24, 0, 12, 24, 24, 12, 0, -24,
    -36, -12, 0, 12, 12, 0, -12, -36,
    -48, -24, -12, 0, 0, -12, -24, -48,
    -72, -48, -36, -24, -24, -36, -48, -72};
int weak_pawn_pcsq[64] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    -10, -12, -14, -16, -16, -14, -12, -10,
    -10, -12, -14, -16, -16, -14, -12, -10,
    -10, -12, -14, -16, -16, -14, -12, -10,
    -10, -12, -14, -16, -16, -14, -12, -10,
    -8, -12, -14, -16, -16, -14, -12, -10,
    -8, -12, -14, -16, -16, -14, -12, -10,
    0, 0, 0, 0, 0, 0, 0, 0};

int passed_pawn_pcsq[64] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    100, 100, 100, 100, 100, 100, 100, 100,
    80, 80, 80, 80, 80, 80, 80, 80,
    60, 60, 60, 60, 60, 60, 60, 60,
    40, 40, 40, 40, 40, 40, 40, 40,
    20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20,
    0, 0, 0, 0, 0, 0, 0, 0};

void initialize()
{
    int len = strlen(e.position);
    for (int i = 0; i < len; i++)
    {
        switch (e.position[i])
        {
        case 'p':
            e.bp++;

            break;
        case 'n':
            e.bn++;
            break;
        case 'b':
            e.bb++;
            break;
        case 'r':
            e.br++;
            break;
        case 'q':
            e.bq++;
            break;

        case 'P':
            e.pos_wp[e.wp] = i;
            e.wp++;

            break;
        case 'N':
            e.wn++;
            break;
        case 'B':
            e.wb++;
            break;
        case 'R':
            e.wr++;
            break;
        case 'Q':
            e.wq++;
            break;

        default:
            break;
        }
    }
}

int calc_npm(char color)
{
    int ret = 0;
    if (color == 'b')
        ret = e.bb * bishop_value + e.bn * knight_value + e.br * rook_value + e.bq * queen_value;
    else
        ret = e.wb * bishop_value + e.wn * knight_value + e.wr * rook_value + e.wq * queen_value;
    return ret;
}

int middle_game()
{
}

int end_game()
{
}

int calc_phase()
{
    int tmax = 4 * (bishop_phase_val + knight_phase_val + rook_phase_val) + 2 * queen_phase_val, tmin = 0;
    int phase = (e.bb + e.wb) * bishop_phase_val + (e.bn + e.wn) * knight_phase_val;
    phase += (e.br + e.wr) * rook_phase_val + (e.bq + e.wq) * queen_phase_val;
    int ret = (phase * 128 + 8) / (tmax - tmin);
    return ret;
}

int evaluate(char *str)
{
    int ret = 0;
    strcpy(e.position, str);
    initialize();
    int phase = calc_phase();
    int mid_val = middle_game();
    int end_val = end_game();
    ret = (mid_val * phase + (128 - phase) * end_val) / 128;
    return ret;
}
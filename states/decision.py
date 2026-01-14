def decide_comment(state):
    score = state.score()

    if score >= 0.6:
        return "DITOLAK"

    if 0.2 <= score < 0.6:
        return "PERLU_REVIEW"

    return "DITERIMA"

def score_keyword(volume, difficulty):
    """
    Higher volume + lower difficulty = higher score
    """
    if volume == 0:
        return 0
    return volume / (1 + difficulty*100)


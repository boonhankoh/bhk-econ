import json, os, random

def get_box():
    boxes_keys = None
    with open("boxes_key.json", "r") as f:
        boxes_keys = json.loads(f.read())
    BOXES = '%s/_static/boxes/' % os.getcwd()
    list_images = os.listdir(path=(BOXES))
    img_name = random.choice(list_images)
    num_zeros = boxes_keys[img_name[:-4]][:-4].split('-')[1]
    return img_name, num_zeros

def get_game_score(game_name, player):
    game_score_key = get_game_score_key(game_name)
    score = player.participant.vars[game_score_key]
    return score

def get_game_group_scores(game_name, player, participants):
    game_score_key = get_game_score_key(game_name)
    game_group_scores_key = game_name + '_group_scores'
    if (game_group_scores_key) in player.participant.vars:
        return player.participant.vars[game_group_scores_key]
    group = random.sample(participants, k=3)
    group_scores = list(map(lambda p: p[game_score_key], group))
    group_scores.append(get_game_score(game_name, player))
    group_scores.sort()
    group_scores.reverse()
    player.participant.vars[game_group_scores_key] = group_scores
    return group_scores


def get_tiebreaker(game_name, player, participants):
    if get_game_place(game_name, player, participants) > 1:
        return None
    tiebreaker_key = game_name + '_won_tiebreaker'
    if tiebreaker_key in player.participant.vars:
        return player.participant.vars[tiebreaker_key]
    score = get_game_score(game_name, player)
    group_scores = get_game_group_scores(game_name, player, participants)
    num_ties = group_scores.count(score)
    if num_ties == 1:
        return None
    tiebreaker = random.randint(1,num_ties) == 1
    return tiebreaker

def get_game_stats(game_name, player, participants):
    return (
        get_game_score(game_name, player),
        get_game_group_scores(game_name, player, participants),
        get_game_place(game_name, player, participants),
        get_tiebreaker(game_name, player, participants)
    )

def get_game_place(game_name, player, participants):
    if player.place:
        return player.place
    score = get_game_score(game_name, player)
    group_scores = get_game_group_scores(game_name, player, participants)
    print(score, group_scores, group_scores.index(score))
    return group_scores.index(score) + 1

def set_score(game_name, player, score):
    game_score_key = get_game_score_key(game_name)
    prev_score = None
    if game_score_key in player.participant.vars:
        prev_score = player.participant.vars[game_score_key]
    # player.participant.vars[game_score_key] = score
    return prev_score

def get_game_score_key(game_name):
    return game_name + '_score'


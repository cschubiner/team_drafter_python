import yaml

from drafter import CURRENT_TEAM_FILENAME, read_yml


def draft(players_and_scores, pick_order, captain1, captain2):
    team1 = [captain1]
    team2 = [captain2]
    team1_score = players_and_scores[captain1]
    team2_score = players_and_scores[captain2]

    available_players = {player: score for player, score in players_and_scores.items() if
                         player != captain1 and player != captain2}

    for pick in pick_order:
        if not available_players:
            break

        highest_score_player = max(available_players, key=available_players.get)

        if pick == 1:
            team1.append(highest_score_player)
            team1_score += available_players[highest_score_player]
        else:
            team2.append(highest_score_player)
            team2_score += available_players[highest_score_player]

        del available_players[highest_score_player]

    return abs(team1_score - team2_score), team1, team2, team1_score, team2_score


def _generate_pick_orders(depth, team1_picks=0, team2_picks=0):
    if depth == 1:
        return [[1], [2]]

    pick_orders = []
    pick_orders += [[1] + order for order in _generate_pick_orders(depth - 1, team1_picks + 1, team2_picks)]
    pick_orders += [[2] + order for order in _generate_pick_orders(depth - 1, team1_picks, team2_picks + 1)]

    return pick_orders


def generate_pick_orders(depth, team1_picks=0, team2_picks=0):
    pick_orders = _generate_pick_orders(depth, team1_picks, team2_picks)

    return [pick_order for pick_order in pick_orders if abs(pick_order.count(1) - pick_order.count(2)) <= 1]


def find_fairest_draft_method(players_and_scores, captain1, captain2):
def find_fairest_draft_method(players_and_scores, captain1, captain2, prioritize_most_switch_offs=False):
    total_players = len(players_and_scores)
    min_score_difference = float('inf')
    best_pick_order = []
    optimal_switch_offs = 0 if prioritize_most_switch_offs else float('inf')

    def count_alternations(pick_order):
        alternations = 0
        for i in range(1, len(pick_order)):
            if pick_order[i] != pick_order[i - 1]:
                alternations += 1
        return alternations

    def compare_switch_offs(pick_order, optimal_switch_offs):
        switch_offs = count_alternations(pick_order)
        if prioritize_most_switch_offs:
            return switch_offs > optimal_switch_offs
        else:
            return switch_offs < optimal_switch_offs

    for pick_order in generate_pick_orders(total_players - 2):
        score_difference, team1, team2, team1_score, team2_score = draft(players_and_scores, pick_order, captain1, captain2)
        if (score_difference < min_score_difference or
            (score_difference == min_score_difference and compare_switch_offs(pick_order, optimal_switch_offs))):
                                                                        captain2)
        if (score_difference < min_score_difference or
            (score_difference == min_score_difference and compare_switch_offs(pick_order, optimal_switch_offs))):
            print()
            print(pick_order)
            print(f'team1 ({len(team1)}): {team1} - {team1_score}')
            print(f'team2 ({len(team2)}): {team2} - {team2_score}')

            min_score_difference = score_difference
            best_pick_order = pick_order
            optimal_switch_offs = count_alternations(pick_order)

    return best_pick_order


def print_fairest_draft_method_statements(fairest_draft_method):
    team1_picks = 0
    team2_picks = 0
    i = 0

    print("Fairest draft method:")

    while i < len(fairest_draft_method):
        current_pick = fairest_draft_method[i]
        num_picks = 1

        while i + 1 < len(fairest_draft_method) and fairest_draft_method[i + 1] == current_pick:
            num_picks += 1
            i += 1

        team = "Team 1" if current_pick == 1 else "Team 2"
        print(f" - {team} picks {num_picks} player{'' if num_picks == 1 else 's'}")

        i += 1


if __name__ == '__main__':
    # Example usage
    # players_and_scores = {'Alice': 100, 'Bob': 90, 'Carol': 80, 'David': 70, 'Eve': 60, 'Frank': 50}
    # captain1 = 'Alice'
    # captain2 = 'Bob'
    path = "text_files/" + CURRENT_TEAM_FILENAME
    with open(path, 'r') as stream:
        parsed = yaml.safe_load(stream)
        forced_team_to_player_names, player_to_score = read_yml(parsed)
    players_and_scores = sorted(player_to_score.items(), key=lambda x: x[1], reverse=True)
    players_and_scores = {(x.split(' ')[0] if ' ' in x else x):y for x, y in players_and_scores}

    # captain1 = 'craig_collins'
    captain1 = 'alex_b'
    # captain2 = 'michael_arbeed'
    captain2 = 'jason_leung'
    # captain2 = 'clayton_schubiner'

    fairest_draft_method = find_fairest_draft_method(players_and_scores, captain1, captain2)
    print("Fairest draft method:", fairest_draft_method)
    print("Note that a 1 means the player was picked by captain1, and a 2 means the player was picked by captain2. It's NOT the number of players picked")

    print_fairest_draft_method_statements(fairest_draft_method)
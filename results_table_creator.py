players = [
    "Alex_Mark", "craig_collins", "michael_arbeed", "andrew_carmine",
    "Zach_Costa", "liam_kinney", "jack_shepherd", "steven_safreno",
    "arthur_orchanian", "jeff_grimes", "clayton_schubiner", "jack_rogers",
    "jeremy_leff", "alex_b", "moe_koelueker", "jason_leung",
    "jake_leichtling"
]

matches = [
    # Match 1 (team 1, team 2, which team won, match score, match notes)
    (["Alex_Mark", "craig_collins", "michael_arbeed", "andrew_carmine", "Zach_Costa", "liam_kinney", "jack_shepherd",
      "steven_safreno"],
     ["arthur_orchanian", "jeff_grimes", "clayton_schubiner", "jack_rogers", "jeremy_leff", "alex_b",
      "moe_koelueker", "jason_leung"], 1, "1-0", ""),
    # Match 2
    (
    ["alex_b", "jeff_grimes", "clayton_schubiner", "arthur_orchanian", "jack_rogers", "steven_safreno",
     "liam_kinney", "jason_leung"],
    ["craig_collins", "jake_leichtling", "jeremy_leff", "Zach_Costa", "jack_shepherd", "Alex_Mark", "andrew_carmine",
     "moe_koelueker"], 1, "1-0", ""),

    # Match 3
    (["craig_collins", "clayton_schubiner", "jake_leichtling", "jack_rogers", "Alex_Mark", "steven_safreno",
      "liam_kinney", "moe_koelueker"],
     ["alex_b", "jeff_grimes", "michael_arbeed", "arthur_orchanian", "jeremy_leff", "jack_shepherd",
      "andrew_carmine", "jason_leung"], 0, "tie", ""),

    # Match 4
    (["craig_collins", "clayton_schubiner", "jake_leichtling", "jack_rogers", "Zach_Costa", "steven_safreno",
      "liam_kinney", "moe_koelueker"],
     ["alex_b", "jeff_grimes", "michael_arbeed", "arthur_orchanian", "jeremy_leff", "jack_shepherd",
      "andrew_carmine", "jason_leung"], 1, "1-0", ""),

    # Match 5
    (["clayton_schubiner", "arthur_orchanian", "michael_arbeed", "jake_leichtling", "jack_shepherd", "Alex_Mark",
      "andrew_carmine", "moe_koelueker"],
     ["alex_b", "craig_collins", "jeff_grimes", "Zach_Costa", "jack_rogers", "steven_safreno",
      "liam_kinney", "jason_leung"], 0, "1-1", ""),

    # Match 6
    (["alex_b", "jeff_grimes", "clayton_schubiner", "arthur_orchanian", "jack_shepherd",
      "steven_safreno", "andrew_carmine", "moe_koelueker"],
     ["craig_collins", "michael_arbeed", "jake_leichtling", "jeremy_leff", "Zach_Costa", "jack_rogers", "Alex_Mark",
      "liam_kinney"], 1, "1-0", "jeff w/ the quad kill rocket launcher"),

    # Match 7
    (["alex_b", "craig_collins", "arthur_orchanian", "michael_arbeed", "Zach_Costa", "steven_safreno",
      "andrew_carmine", "jason_leung"],
     ["jeff_grimes", "clayton_schubiner", "jake_leichtling", "jack_shepherd", "jack_rogers", "Alex_Mark", "liam_kinney",
      "moe_koelueker"], 1, "2-0", "wipeout"),

    # Match 8
    (["craig_collins", "alex_b", "clayton_schubiner", "arthur_orchanian", "Zach_Costa",
      "steven_safreno", "moe_koelueker", "jason_leung"],
     ["jeff_grimes", "michael_arbeed", "jack_shepherd", "jake_leichtling", "jack_rogers", "Alex_Mark", "liam_kinney",
      "andrew_carmine"], 0, "1-1", ""),

    # Match 9
    (["craig_collins", "alex_b", "clayton_schubiner", "arthur_orchanian", "Zach_Costa",
      "steven_safreno", "moe_koelueker", "jason_leung"],
     ["jeff_grimes", "michael_arbeed", "jack_shepherd", "jake_leichtling", "jack_rogers", "Alex_Mark", "liam_kinney",
      "andrew_carmine"], 0, "1-1", "team 2 parked vehicles on the flag in one round")
]


def match_results(players, matches):
    result = "player/match"

    for match in range(1, 10):
        result += f",{match}"
    result += "\n"

    for player in players:
        result += player

        for match in matches:
            team1, team2, outcome, score, notes = match
            if player in team1:
                if outcome == 1:
                    outcome = "win"
                elif outcome == 2:
                    outcome = "loss"
                else:
                    outcome = "tie"
            elif player in team2:
                if outcome == 1:
                    outcome = "loss"
                elif outcome == 2:
                    outcome = "win"
                else:
                    outcome = "tie"
            else:
                outcome = ""


            # if the outcome is a tie, change it to (tie team 1) or (tie team 2)
            if outcome == "tie":
                if player in match[0]:
                    outcome = "(tie team 1)"
                else:
                    outcome = "(tie team 2)"
            result += f",{outcome}"

        result += "\n"

    result += "match_notes"
    for match in matches:
        result += f",{match[3]} ({match[4]})"

    return result


if __name__ == "__main__":
    print(match_results(players, matches))
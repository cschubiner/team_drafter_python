import sys
import unittest
from contextlib import contextmanager
from io import StringIO

from find_fair_draft_order import print_fairest_draft_method_statements, find_fairest_draft_method, \
    generate_pick_orders, draft

@contextmanager
def capture_output():
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_stdout


class MyTestCase(unittest.TestCase):

    def test_draft(self):
        players_and_scores = {'Alice': 100, 'Bob': 90, 'Carol': 80, 'David': 70, 'Eve': 60, 'Frank': 50}
        pick_order = [1, 2, 1, 2, 1, 2]
        captain1 = 'Alice'
        captain2 = 'Bob'
        score_difference, team1, team2, team1_score, team2_score = draft(players_and_scores, pick_order, captain1,
                                                                         captain2)

        assert team1 == ['Alice', 'Carol', 'Eve']
        assert team2 == ['Bob', 'David', 'Frank']
        assert team1_score == 100+80+60
        assert team2_score == 90+70+50
        assert score_difference == team1_score - team2_score

    def test_generate_pick_orders(self):
        assert generate_pick_orders(2) == [[1, 2], [2, 1]]
        assert generate_pick_orders(3) == [[1, 1, 2], [1, 2, 1], [1, 2, 2], [2, 1, 1], [2, 1, 2], [2, 2, 1]]
        assert [1, 2, 2] in generate_pick_orders(3)
        assert [1, 1, 1, 2, 2] in generate_pick_orders(5)
        assert [1, 1, 1, 2, 2, 2] in generate_pick_orders(6)
        assert [1, 1, 1, 1, 2, 2, 2] in generate_pick_orders(7)
        assert [2, 2, 1, 1, 1, 2, 2] in generate_pick_orders(7)

    def test_find_fairest_draft_method(self):
        players_and_scores = {'Alice': 100, 'Bob': 90, 'Carol': 80, 'David': 70, 'Eve': 40}
        captain1 = 'Alice'
        captain2 = 'Carol'

        fairest_draft_method = find_fairest_draft_method(players_and_scores, captain1, captain2)

        assert fairest_draft_method == [1, 2, 2]

    def test_print_fairest_draft_method_statements(capsys):
        fairest_draft_method = [1, 1, 2, 2, 2, 1]

        with capture_output() as captured_output:
            print_fairest_draft_method_statements(fairest_draft_method)

        expected_output = "Fairest draft method:\n - Team 1 picks 2 players\n - Team 2 picks 3 players\n - Team 1 picks 1 player\n"

        assert captured_output.getvalue() == expected_output, f"Expected: {expected_output}, Actual: {captured_output.getvalue()}"


if __name__ == '__main__':
    unittest.main()

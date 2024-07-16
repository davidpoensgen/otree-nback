from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'n_back'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    N = 2  # the n in n-back
    trialDuration = 2000  # milliseconds per round
    intertrialDuration = 1000  # milliseconds between rounds

    item_styles = ["glyphicon-tree-deciduous", "glyphicon-fire", "glyphicon-tint", "glyphicon-certificate"]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # this is the item sequence; it is fixed here for demo purposes.
    # Usually, it should be set in creating_session or similar, and each round should use a different sequence.
    # While the example uses 0-3 only, it would be straightforward to extend it to e.g. 5 items.
    item_sequence = models.StringField(initial="121232132203013122201202313212113231213220302320")

    responses = models.StringField()
    correct = models.StringField()


# PAGES

class Instructions(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "length": len(player.item_sequence)
        }


class NBack(Page):
    form_model = 'player'
    form_fields = ['responses', 'correct']

    @staticmethod
    def js_vars(player):
        return {
            "item_sequence": [int(i) for i in player.item_sequence],
            "target_responses": [int(player.item_sequence[int(i)] == player.item_sequence[int(i)-C.N] and int(i) >= C.N) for i in range(len(player.item_sequence))]
        }


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "correct_count": sum([int(i) for i in player.correct[C.N:]]),
            "total_count": len(player.correct[C.N:])
        }

page_sequence = [Instructions, NBack, Results]

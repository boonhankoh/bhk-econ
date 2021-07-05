from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from django import forms

author = 'Nisvan Erkal, Lata Gangadharan, Boon Han Koh'

doc = """
Effort/Luck Experiment (Revision): Dictator Game
"""


class Constants(BaseConstants):
    name_in_url = 'el_dictator_task'
    players_per_group = 2
    num_rounds = 1
    # timeout (before default decisions recorded
    timeout_default = 15
    # endowment
    dg_endowment = 300


class Subsession(BaseSubsession):
    def creating_session(self):
        # divide subjects into groups
        # self.group_randomly()
        group_structure = []
        num_blocks = int(len(self.get_players())/6)
        print(num_blocks)
        for i in range(0, num_blocks):
            j1 = i*6+1
            j2 = j1+1
            j3 = j2+1
            group_structure.append([j1, j1+3])
            group_structure.append([j2, j2+3])
            group_structure.append([j3, j3+3])
            print(group_structure)
        self.set_group_matrix(group_structure)

        for player in self.get_players():
            # define roles
            if player.id_in_group == 1:
                player.dictator = True
                player.recipient = False
            else:
                player.dictator = False
                player.recipient = True


class Group(BaseGroup):
    dictator_amt = models.IntegerField()
    recipient_amt = models.IntegerField()

    def set_payoffs(self):
        players = self.get_players()
        # extract dictator's decisions at group level
        for p in players:
            if p.dictator:
                self.dictator_amt = p.kept
                self.recipient_amt = p.gave
        # determine individual payoffs
        for p in players:
            if p.dictator:
                p.task2payoff = self.dictator_amt
            else:
                p.task2payoff = self.recipient_amt
            # store payoffs and decisions
            p.participant.vars['dictator'] = p.dictator
            p.participant.vars['recipient'] = p.recipient
            p.participant.vars['dictatorendowment'] = Constants.dg_endowment
            p.participant.vars['dictator_amt'] = self.dictator_amt
            p.participant.vars['recipient_amt'] = self.recipient_amt
            p.participant.vars['task2payoff'] = p.task2payoff


class Player(BasePlayer):
    # function for dumping variables in participant vars field
    def participant_vars_dump(self, page):
        for field in page.form_fields:
            if Constants.num_rounds > 1:
                self.participant.vars[field + '_' + str(self.round_number)] = getattr(self, field)
            else:
                self.participant.vars[field] = getattr(self, field)

    # define roles
    dictator = models.BooleanField()
    recipient = models.BooleanField()
    # variables for storing decisions
    gave = models.IntegerField(min=0, max=Constants.dg_endowment)
    kept = models.IntegerField(min=0, max=Constants.dg_endowment)
    # variables to store payoffs
    task2payoff = models.IntegerField()

    # store whether subject drops out
    droppedoutDG = models.BooleanField()

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


author = 'Nisvan Erkal, Lata Gangadharan, Boon Han Koh'

doc = """
Effort/Luck Experiment (Revision): End of Experiment
"""


class Constants(BaseConstants):
    name_in_url = 'el_end'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # variable for dumping all participant variables
    participant_vars = models.LongStringField()
    # store treatment and role for data-cleaning purposes
    treatment = models.StringField(initial="Null")
    taskrole = models.StringField(initial="Null")


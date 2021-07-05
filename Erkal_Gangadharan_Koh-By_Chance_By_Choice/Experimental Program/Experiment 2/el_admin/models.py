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
Effort/Luck Experiment (Revision): Admin Page
"""


class Constants(BaseConstants):
    name_in_url = 'el_admin'
    players_per_group = None
    num_rounds = 1
    # timeout (before default decisions recorded
    timeout_default = 15


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.participant.vars['id'] = player.participant.id_in_session


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # function for dumping variables in participant vars field
    def participant_vars_dump(self, page):
        for field in page.form_fields:
            if Constants.num_rounds > 1:
                self.participant.vars[field + '_' + str(self.round_number)] = getattr(self, field)
            else:
                self.participant.vars[field] = getattr(self, field)

    consent = models.BooleanField(
        choices=[
            [True, "I agree"],
            [False, "I do not agree"],
        ],
        label="Accept:",
        widget=widgets.RadioSelect,
    )

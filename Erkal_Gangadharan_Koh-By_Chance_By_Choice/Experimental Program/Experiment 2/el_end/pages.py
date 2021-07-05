from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import json

class A_Dropout(Page):
    def is_displayed(self):
        return self.participant.vars['is_dropout'] is True

    def vars_for_template(self):
        parvars = self.participant.vars
        self.player.participant_vars = json.dumps(parvars)

        return dict(
            par_vars=parvars,
        )


class B_End(Page):
    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        self.player.participant_vars = json.dumps(parvars)

        if self.participant.vars['treatstrategy'] == 1:
            self.player.treatment = "SM"
        elif self.participant.vars['treatstrategy'] == 0:
            self.player.treatment = "NSM"

        if self.participant.vars['leader'] is True:
            self.player.taskrole = "Leader"
        elif self.participant.vars['leader'] is False:
            self.player.taskrole = "Member"

        return dict(
            par_vars=parvars,
        )


page_sequence = [A_Dropout, B_End]

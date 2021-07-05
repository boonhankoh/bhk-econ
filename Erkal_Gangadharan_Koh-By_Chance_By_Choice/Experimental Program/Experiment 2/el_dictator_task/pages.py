from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time


class A_Intro(Page):
    wait_for_all_groups = True

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1

    def before_next_page(self):
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.timeout_default * 60


class B_Decision(Page):
    form_model = 'player'
    form_fields = ['gave', 'kept']

    def error_message(self, values):
        if values['gave'] + values['kept'] != Constants.dg_endowment:
            return "Both amounts must add up to "+str(Constants.dg_endowment)+" ECU."

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1
        elif self.participant.vars['is_dropout'] is False:
            return self.participant.vars['expiry_timestamp'] - time.time()

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.gave = 150
            self.player.kept = 150
            self.player.droppedoutDG = True
            self.participant.vars['is_dropout'] = True

        self.player.participant_vars_dump(self)
        self.participant.vars['droppedoutDG'] = self.player.droppedoutDG


class C_WaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


page_sequence = [
    A_Intro,
    B_Decision,
    C_WaitPage,
]

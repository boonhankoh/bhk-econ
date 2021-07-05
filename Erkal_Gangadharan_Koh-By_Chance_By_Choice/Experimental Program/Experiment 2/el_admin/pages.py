from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class A_Welcome(Page):
    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )

    def before_next_page(self):
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.timeout_default * 60


class B_PLS_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    def before_next_page(self):
        self.player.participant_vars_dump(self)

        if self.player.consent is True:
            self.participant.vars['is_dropout'] = False

        if self.player.consent is False:
            self.participant.vars['is_dropout'] = True

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )

    def app_after_this_page(self, upcoming_apps):
        if self.timeout_happened:
            self.participant.vars['is_dropout'] = True
            return upcoming_apps[-1]


class E_Turnaway(Page):
    def is_displayed(self):
        return self.player.consent is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class TaskWaitPage(WaitPage):
    wait_for_all_groups = True


class D_Overview(Page):
    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


page_sequence = [
    A_Welcome,
    B_PLS_Consent,
    E_Turnaway,
    TaskWaitPage,
    D_Overview,
]

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time


class TaskWaitPage(WaitPage):
    wait_for_all_groups = True


class A_PracticeIntro(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class B_RoundIntro(Page):
    def is_displayed(self):
        return self.round_number != 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C_InvestmentInfo(Page):
    def before_next_page(self):
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.timeout_default * 60

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class D_Investment(Page):
    form_model = 'player'
    form_fields = ['higheffort']

    def is_displayed(self):
        return self.round_number == 1 or self.player.treatstrategy or (self.player.treatstrategy is False and self.player.leader)

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1
        elif self.participant.vars['is_dropout'] is False:
            return self.participant.vars['expiry_timestamp'] - time.time()

    def before_next_page(self):
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.timeout_default * 60

        if self.timeout_happened:
            self.player.higheffort = 1
            self.player.droppedouteffort = True
            self.participant.vars['is_dropout'] = True

            if self.player.leader is True:
                self.group.leaderdroppedout = True

        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class E_Prior(Page):
    form_model = 'player'
    form_fields = ['prior']

    def is_displayed(self):
        return self.round_number == 1 or self.player.treatstrategy or (self.player.treatstrategy is False and self.player.member)

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1
        elif self.participant.vars['is_dropout'] is False:
            return self.participant.vars['expiry_timestamp'] - time.time()

    def before_next_page(self):
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.timeout_default * 60

        if self.timeout_happened:
            self.player.prior = 50
            self.player.droppedoutprior = True
            self.participant.vars['is_dropout'] = True

        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class F_Posterior(Page):
    form_model = 'player'
    form_fields = ['posteriorsuccess', 'posteriorfailure']

    def is_displayed(self):
        return self.round_number == 1 or self.player.treatstrategy or (self.player.treatstrategy is False and self.player.member)

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1
        elif self.participant.vars['is_dropout'] is False:
            return self.participant.vars['expiry_timestamp'] - time.time()

    def before_next_page(self):
        if self.timeout_happened:
            self.player.posteriorsuccess = 50
            self.player.posteriorfailure = 50
            self.player.droppedoutposterior = True
            self.participant.vars['is_dropout'] = True

        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class G_InvestmentHypothetical(Page):
    form_model = 'player'
    form_fields = ['higheffort']

    def is_displayed(self):
        return self.round_number != 1 and self.player.treatstrategy is False and self.player.member

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1

    def before_next_page(self):
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class H_WaitPage(Page):
    wait_for_all_groups = True  # not needed? each group can proceed at their own pace

    def get_timeout_seconds(self):
        return 0.001

    def before_next_page(self):
        self.group.set_round_payoffs()
        self.participant.vars['droppedouteffort_' + str(self.round_number - Constants.num_prac_rounds)] = self.player.droppedouteffort
        self.participant.vars['leaderdroppedout_' + str(self.round_number - Constants.num_prac_rounds)] = self.group.leaderdroppedout
        self.participant.vars['groupreturnsuccess_' + str(self.round_number - Constants.num_prac_rounds)] = self.group.groupreturnsuccess
        self.participant.vars['groupreturnfailure_' + str(self.round_number - Constants.num_prac_rounds)] = self.group.groupreturnfailure
        self.participant.vars['droppedoutprior_' + str(self.round_number - Constants.num_prac_rounds)] = self.player.droppedoutprior
        self.participant.vars['droppedoutposterior_' + str(self.round_number - Constants.num_prac_rounds)] = self.player.droppedoutposterior


page_sequence = [
    TaskWaitPage,
    A_PracticeIntro,
    B_RoundIntro,
    C_InvestmentInfo,
    D_Investment,
    E_Prior,
    F_Posterior,
    G_InvestmentHypothetical,
    TaskWaitPage,
    H_WaitPage,
]

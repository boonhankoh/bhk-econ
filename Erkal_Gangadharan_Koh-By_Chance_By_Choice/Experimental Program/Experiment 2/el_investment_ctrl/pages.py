from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class A_Intro(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


# version below has all questions on the same page
class B_CtrlQnsIntro(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


# show each question on a separate page
class C1_CtrlQnsTaskPaid(Page):
    form_model = 'player'
    form_fields = ['ctrltaskpaid']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C2_CtrlQnsTask1RoundPaid(Page):
    form_model = 'player'
    form_fields = ['ctrltask1roundpaid']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C3_CtrlQnsGroup(Page):
    form_model = 'player'
    form_fields = ['ctrlgroup']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C4_CtrlQnsFeedback(Page):
    form_model = 'player'
    form_fields = ['ctrlfeedback']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C5_CtrlQnsPayoffMember(Page):
    form_model = 'player'
    form_fields = ['ctrlpayoffmember']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C6_CtrlQnsPayoffLeader(Page):
    form_model = 'player'
    form_fields = ['ctrlpayoffleader']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C7_CtrlQnsPaymentRole(Page):
    form_model = 'player'
    form_fields = ['ctrlpaymentrole']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C8_CtrlQnsBeliefPayment(Page):
    form_model = 'player'
    form_fields = ['ctrlbeliefpayment']

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C9_CtrlQnsTruthTelling(Page):
    form_model = 'player'
    form_fields = ['ctrltruthtelling']

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        pvars = self.participant.vars
        pvars['ctrl_errors_count'] = self.player.ctrl_errors_count
        pvars['ctrltaskpaid_errors_count'] = self.player.ctrltaskpaid_errors_count
        pvars['ctrltask1roundpaid_errors_count'] = self.player.ctrltask1roundpaid_errors_count
        pvars['ctrlgroup_errors_count'] = self.player.ctrlgroup_errors_count
        pvars['ctrlfeedback_errors_count'] = self.player.ctrlfeedback_errors_count
        pvars['ctrlpayoffmember_errors_count'] = self.player.ctrlpayoffmember_errors_count
        pvars['ctrlpayoffleader_errors_count'] = self.player.ctrlpayoffleader_errors_count
        pvars['ctrlpaymentrole_errors_count'] = self.player.ctrlpaymentrole_errors_count
        pvars['ctrlbeliefpayment_errors_count'] = self.player.ctrlbeliefpayment_errors_count
        pvars['ctrltruthtelling_errors_count'] = self.player.ctrltruthtelling_errors_count

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class TaskWaitPage(WaitPage):
    wait_for_all_groups = True


class D_Summary(Page):
    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


page_sequence = [
    A_Intro,
    B_CtrlQnsIntro,
    C1_CtrlQnsTaskPaid,
    C2_CtrlQnsTask1RoundPaid,
    C3_CtrlQnsGroup,
    C4_CtrlQnsFeedback,
    C5_CtrlQnsPayoffMember,
    C6_CtrlQnsPayoffLeader,
    C7_CtrlQnsPaymentRole,
    C8_CtrlQnsBeliefPayment,
    C9_CtrlQnsTruthTelling,
    TaskWaitPage,
    D_Summary,
]

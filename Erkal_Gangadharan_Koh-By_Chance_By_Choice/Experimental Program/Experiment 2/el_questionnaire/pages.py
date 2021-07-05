from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import time


class A_Intro(Page):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def before_next_page(self):
        self.participant.vars['survey_part'] = 1

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class B_General(Page):
    form_model = 'player'
    form_fields = [
        'comments_general',
        'comments_unclear',
                   ]

    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class C_Demographic(Page):
    form_model = 'player'
    form_fields = [
        'year_birth',
        'female',
        'study_field',
        'study_lvl',
        'gpa',
        'nationality',
        'other_nationality',
        'country_born',
        'other_country_born',
        'years_lived_australia',
        'past_experiments',
                   ]

    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def error_message(self, values):
        if (values['nationality'] != "OTHER" and type(values['other_nationality']) != type(None)) or (values['nationality'] == "OTHER" and type(values['other_nationality']) == type(None)):
            return "If you select 'other nationality', you must specify in the provided field. Otherwise, leave it blank."
        if (values['country_born'] != "OTHER" and type(values['other_country_born']) != type(None)) or (values['country_born'] == "OTHER" and type(values['other_country_born']) == type(None)):
            return "If you select 'other country', you must specify in the provided field. Otherwise, leave it blank."

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class D_EffortGeneral(Page):
    form_model = 'player'
    form_fields = ['reasons_effort_general']

    def is_displayed(self):
        return (self.participant.vars['leader'] is True or self.session.config['treatstrategy'] == 1) and self.participant.vars['is_dropout'] is False

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class E_EffortFactors(Page):
    form_model = 'player'
    form_fields = [
        'effort_fac_leader_payoff',
        'effort_fac_member_payoff',
        'effort_fac_diff_return',
        'effort_fac_zero',
        'effort_fac_none',
    ]

    def is_displayed(self):
        return (self.participant.vars['leader'] is True or self.session.config['treatstrategy'] == 1) and self.participant.vars['is_dropout'] is False

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1
        self.player.participant_vars_dump(self)

    def error_message(self, values):
        if (values['effort_fac_none'] is True and (values['effort_fac_leader_payoff'] or values['effort_fac_member_payoff'] or values['effort_fac_diff_return'] or values['effort_fac_zero'])) or (values['effort_fac_none'] is False and (values['effort_fac_leader_payoff'] is False and values['effort_fac_member_payoff'] is False and values['effort_fac_diff_return'] is False and values['effort_fac_zero'] is False)):
            return "If none of the above factors apply to you, please select only the last option."

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class F_BeliefsGeneral(Page):
    form_model = 'player'
    form_fields = ['reasons_beliefs_general']

    def is_displayed(self):
        return (self.participant.vars['member'] is True or self.session.config['treatstrategy'] == 1) and self.participant.vars['is_dropout'] is False

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1
        self.player.participant_vars_dump(self)

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class G_BeliefsFactors(Page):
    form_model = 'player'
    form_fields = [
        'belief_fac_leader_payoff',
        'belief_fac_strategy',
        'belief_fac_member_payoff',
        'belief_fac_diff_return',
        'belief_fac_zero',
        'belief_fac_none',
    ]

    def is_displayed(self):
        return (self.participant.vars['member'] is True or self.session.config['treatstrategy'] == 1) and self.participant.vars['is_dropout'] is False

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1
        self.player.participant_vars_dump(self)

    def error_message(self, values):
        if (values['belief_fac_none'] is True and (values['belief_fac_leader_payoff'] or values['belief_fac_strategy'] or values['belief_fac_member_payoff'] or values['belief_fac_diff_return'] or values['belief_fac_zero'])) or (values['belief_fac_none'] is False and (values['belief_fac_leader_payoff'] is False and values['belief_fac_strategy'] is False and values['belief_fac_member_payoff'] is False and values['belief_fac_diff_return'] is False and values['belief_fac_zero'] is False)):
            return "If none of the above factors apply to you, please select only the last option."

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class H_Dictator(Page):
    form_model = 'player'
    form_fields = ['belief_dictator_gave']

    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1
        self.player.participant_vars_dump(self)
        self.participant.vars['expiry_timestamp'] = time.time() + Constants.timeout_default * 60

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class I_RiskGame(Page):
    form_model = 'player'
    form_fields = [
        'risk_invest',
        'risk_keep',
    ]

    def error_message(self, values):
        if values['risk_invest'] + values['risk_keep'] != Constants.rg_endowment:
            return "Both amounts must add up to "+str(Constants.rg_endowment)+" ECU."

    def get_timeout_seconds(self):
        if self.participant.vars['is_dropout'] is True:
            return 1
        elif self.participant.vars['is_dropout'] is False:
            return self.participant.vars['expiry_timestamp'] - time.time()

    def before_next_page(self):
        self.participant.vars['survey_part'] += 1

        if self.timeout_happened:
            self.player.risk_invest = 25
            self.player.risk_keep = 25
            self.player.droppedoutRG = True
            self.participant.vars['is_dropout']=True

        self.player.participant_vars_dump(self)
        self.participant.vars['droppedoutRG'] = self.player.droppedoutRG
        self.player.set_risk_payoffs()

    def vars_for_template(self):
        parvars = self.participant.vars
        return dict(
            par_vars=parvars,
        )


class J_PayID(Page):
    form_model = 'player'
    form_fields = [
        'payID1',
        'payID2',
    ]

    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def error_message(self, values):
        if values['payID1'] != values['payID2']:
            return "The email address or phone number in both fields do not match."


class WaitScreen(WaitPage):
    pass
    # after_all_players_arrive = 'set_risk_payoffs'


page_sequence = [
    A_Intro,
    B_General,
    C_Demographic,
    D_EffortGeneral,
    E_EffortFactors,
    F_BeliefsGeneral,
    G_BeliefsFactors,
    H_Dictator,
    I_RiskGame,
    J_PayID,
    # WaitScreen,
    ]

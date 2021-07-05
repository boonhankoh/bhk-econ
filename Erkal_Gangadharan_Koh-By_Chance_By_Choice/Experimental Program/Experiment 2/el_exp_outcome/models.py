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
import math

author = 'Nisvan Erkal, Lata Gangadharan, Boon Han Koh'

doc = """
Effort/Luck Experiment (Revision): Experiment Outcome Screen
"""


class Constants(BaseConstants):
    name_in_url = 'el_exp_outcome'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.config['participation_fee'] = self.session.config['show_up']


class Group(BaseGroup):
    pass
    # def set_payoffs(self):
    #     for p in self.get_players():
    #         if p.participant.vars['is_dropout'] is False:
    #             if self.session.vars['taskpaid'] == 1:
    #                 p.paidtask_payoff = p.participant.vars['task1payoff']
    #             elif self.session.vars['taskpaid'] == 2:
    #                 p.paidtask_payoff = p.participant.vars['task2payoff']
    #
    #             p.riskpayoff = p.participant.vars['risk_payoff']
    #             p.exp_payoff_AUD = round((p.paidtask_payoff + p.riskpayoff) / self.session.config['dollar_convert'], 2) + self.session.config['show_up']
    #             # store payment variables for oTree output
    #             p.participant.payoff = round((p.paidtask_payoff + p.riskpayoff) / self.session.config['dollar_convert'], 2)


class Player(BasePlayer):
    paidtask_payoff = models.IntegerField()
    riskpayoff = models.IntegerField()
    exp_payoff_AUD = models.FloatField()

    # set final payoffs
    def set_payoffs(self):
        if self.participant.vars['is_dropout'] is False:
            if self.session.vars['taskpaid'] == 1:
                self.paidtask_payoff = self.participant.vars['task1payoff']
            elif self.session.vars['taskpaid'] == 2:
                self.paidtask_payoff = self.participant.vars['task2payoff']
            self.riskpayoff = self.participant.vars['risk_payoff']
            self.exp_payoff_AUD = round((self.paidtask_payoff + self.riskpayoff) / self.session.config['dollar_convert'], 2) + self.session.config['show_up']
            # store payment variables for oTree output
            self.participant.payoff = round((self.paidtask_payoff + self.riskpayoff) / self.session.config['dollar_convert'], 2)

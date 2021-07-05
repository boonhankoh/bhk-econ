from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import json

class MyPage(WaitPage):
    pass
    # after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def is_displayed(self):
        return self.participant.vars['is_dropout'] is False

    def vars_for_template(self):
        self.player.set_payoffs()
        leader = self.participant.vars['leader']
        member = self.participant.vars['member']
        investendowment = self.participant.vars['PR_investendowment']
        leaderhigheffort = self.participant.vars['PR_leaderhigheffort']
        costefforthigh = self.participant.vars['PR_costefforthigh']
        costeffortlow = self.participant.vars['PR_costeffortlow']
        prior = self.participant.vars['PR_prior']
        posteriorsuccess = self.participant.vars['PR_posteriorsuccess']
        posteriorfailure = self.participant.vars['PR_posteriorfailure']
        groupreturnsuccess = self.participant.vars['PR_groupreturnsuccess']
        groupreturnfailure = self.participant.vars['PR_groupreturnfailure']
        groupinvestsuccess = self.participant.vars['PR_groupinvestsuccess']
        bsrsuccessprior = self.participant.vars['PR_bsrsuccessprior']
        bsrsuccessposterior = self.participant.vars['PR_bsrsuccessposterior']
        payoffinvest = self.participant.vars['PR_payoffinvest']
        payoffbelief = self.participant.vars['PR_payoffbelief']
        beliefquestion = self.participant.vars['PR_beliefquestion']
        paidinvest = self.participant.vars['PR_paidinvest']
        task1payoff = self.participant.vars['task1payoff']
        dictator = self.participant.vars['dictator']
        recipient = self.participant.vars['recipient']
        dictatorendowment = self.participant.vars['dictatorendowment']
        dictator_amt = self.participant.vars['dictator_amt']
        recipient_amt = self.participant.vars['recipient_amt']
        task2payoff = self.participant.vars['task2payoff']
        taskpaid = self.session.vars['taskpaid']
        task1roundpaid = self.session.vars['task1roundpaid']
        show_up = self.session.config['show_up']
        parvars = self.participant.vars

        return dict(
            leader=leader,
            member=member,
            investendowment=investendowment,
            leaderhigheffort=leaderhigheffort,
            costefforthigh=costefforthigh,
            costeffortlow=costeffortlow,
            prior=prior,
            posteriorsuccess=posteriorsuccess,
            posteriorfailure=posteriorfailure,
            groupreturnsuccess=groupreturnsuccess,
            groupreturnfailure=groupreturnfailure,
            groupinvestsuccess=groupinvestsuccess,
            bsrsuccessprior=bsrsuccessprior,
            bsrsuccessposterior=bsrsuccessposterior,
            payoffinvest=payoffinvest,
            payoffbelief=payoffbelief,
            beliefquestion=beliefquestion,
            paidinvest=paidinvest,
            task1payoff=task1payoff,
            dictator=dictator,
            recipient=recipient,
            dictatorendowment=dictatorendowment,
            dictator_amt=dictator_amt,
            recipient_amt=recipient_amt,
            task2payoff=task2payoff,
            taskpaid=taskpaid,
            task1roundpaid=task1roundpaid,
            show_up=show_up,
            par_vars=parvars,
        )


page_sequence = [
    #MyPage,
    Results,
]

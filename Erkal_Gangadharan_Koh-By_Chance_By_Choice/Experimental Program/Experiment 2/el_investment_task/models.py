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
import random
import itertools
from django import forms
from django.utils.safestring import mark_safe

author = 'Nisvan Erkal, Lata Gangadharan, Boon Han Koh'

doc = """
Effort/Luck Experiment (Revision): Investment Task
"""


class Constants(BaseConstants):
    name_in_url = 'el_investment_task'
    players_per_group = 3
    num_paid_rounds = 3  # number of paid rounds
    num_prac_rounds = 1 # number of practice rounds
    num_rounds = num_prac_rounds + num_paid_rounds  # practice + paid rounds
    # timeout (before default decisions recorded
    timeout_default = 15
    # endowment
    endowment = 300
    # cost of effort
    costefforthigh = 250
    costeffortlow = 50
    # probability of success
    prsuccesseffhigh = 0.75
    prsuccessefflow = 0.25
    # payment for members' beliefs
    beliefpayment = 200
    # returns from investments
    returnsuccess = {
        1: 250,
        2: 200,
        3: 300,
    }
    returnfailure = {
        1: 50,
        2: 0,
        3: 50,
    }
    # define set of possible orders of parameters that groups will face (first round is always practice)
    order_set_fixed = [
        [2, 1, 2, 3],
        [2, 1, 3, 2],
        [2, 2, 1, 3],
        [2, 2, 3, 1],
        [2, 3, 1, 2],
        [2, 3, 2, 1],
    ]
    # print(order_set_fixed)


class Subsession(BaseSubsession):
    def creating_session(self):
        # determine order of treatments
        # order_set = Constants.order_set_fixed
        s = self.session.config['startingparam']
        n = len(Constants.order_set_fixed)
        order_set = []
        order_set.extend(Constants.order_set_fixed[s-1:n])
        order_set.extend(Constants.order_set_fixed[0:s-1])
        order = itertools.cycle(order_set)

        if self.round_number == 1:
            # divide subjects into groups
            # self.group_randomly()
            # die roll for task paid and round paid (fixed for entire session)
            self.session.vars['taskpaid'] = random.randint(1, 2)
            self.session.vars['task1roundpaid'] = random.randint(1, Constants.num_paid_rounds)
        else:
            # keep groups from round 1
            self.group_like_round(1)

        for player in self.get_players():
            # define round number (within paid rounds)
            player.paid_round_num = self.round_number - Constants.num_prac_rounds
            # define roles
            if player.id_in_group == 1:
                player.leader = True
                player.member = False
            else:
                player.leader = False
                player.member = True
            # update treatments and payment parameters at player level
            player.treatstrategy = self.session.config['treatstrategy']
            player.participant.vars['treatstrategy'] = player.treatstrategy
            player.taskpaid = self.session.vars['taskpaid']
            player.task1roundpaid = self.session.vars['task1roundpaid']

        for g in self.get_groups():
            orderlist = next(order)  # orderlist iterates over [1,2], [2,1], etc.
            for i in range(Constants.num_rounds):  # i = round_number - 1
                if self.round_number == i+1:
                    # print(i)
                    g.param = int(orderlist[i])  # extracts param # for this round
                    g.groupreturnsuccess = Constants.returnsuccess[g.param]  # extracts return for success
                    # print(Constants.returnsuccess[Constants.order_set[g.param-1][i]])
                    g.groupreturnfailure = Constants.returnfailure[g.param]  # extracts return for failure
                    # print(Constants.returnfailure[Constants.order_set[g.param-1][i]])
            # print(g.param1)
            # print(g.param2)

        if self.round_number == 1:
            print("Treat Strategy Method: " + str(self.session.config['treatstrategy']))
            print("Task Paid: " + str(self.session.vars['taskpaid']))
            print("Task 1 Round Paid: " + str(self.session.vars['task1roundpaid']))
            print(order_set)


class Group(BaseGroup):
    param = models.IntegerField()
    # variables for storing parameters of a given round
    groupreturnsuccess = models.IntegerField(initial=-1)
    groupreturnfailure = models.IntegerField(initial=-1)
    # variables for storing decisions and outcomes of the group
    leaderhigheffort = models.BooleanField()
    groupinvestsuccess = models.BooleanField()
    # die roll for investment outcome
    rollinvest = models.FloatField()
    # store whether leader drops out
    leaderdroppedout = models.BooleanField(initial=False)

    def set_round_payoffs(self):
        players = self.get_players()

        # die rolls at group level
        self.rollinvest = random.random()

        for p in players:

            # die rolls at individual levels
            p.rollbsrprior = random.random() * 100
            p.rollbsrposterior = random.random() * 100
            p.beliefquestion = random.randint(1, 2)
            if p.member:
                p.paidinvest = random.choice([True, False])
            else:
                p.paidinvest = True

            # extract leader's decision
            if p.leader:
                self.leaderhigheffort = p.higheffort

        # determine outcome of investment
        if self.rollinvest <= (
                self.leaderhigheffort * Constants.prsuccesseffhigh + (1 - self.leaderhigheffort) * (
        Constants.prsuccessefflow)):
            self.groupinvestsuccess = True
        else:
            self.groupinvestsuccess = False

        # determine individual payoffs
        for p in players:
            # payoffs from investments
            if p.leader:
                p.payoffinvest = Constants.endowment - (p.higheffort * Constants.costefforthigh + (
                            1 - p.higheffort) * Constants.costeffortlow) + (
                                             self.groupinvestsuccess * self.groupreturnsuccess + (
                                                 1 - self.groupinvestsuccess) * self.groupreturnfailure)
            else:
                p.payoffinvest = self.groupinvestsuccess * self.groupreturnsuccess + (
                            1 - self.groupinvestsuccess) * self.groupreturnfailure
            p.participant.vars['groupinvestsuccess_' + str(
                self.round_number - Constants.num_prac_rounds)] = self.groupinvestsuccess
            p.participant.vars[
                'payoffinvest_' + str(self.round_number - Constants.num_prac_rounds)] = p.payoffinvest

            # payoffs from beliefs
            if p.leader:
                p.payoffbelief = 0
            else:
                # calculate bsr scores
                p.bsrscoreprior = (1 - ((self.leaderhigheffort * 100 - p.prior) / 100) ** 2) * 100
                if self.groupinvestsuccess:
                    p.bsrscoreposterior = (1 - (
                                (self.leaderhigheffort * 100 - p.posteriorsuccess) / 100) ** 2) * 100
                else:
                    p.bsrscoreposterior = (1 - (
                                (self.leaderhigheffort * 100 - p.posteriorfailure) / 100) ** 2) * 100
                # determine whether BSR for priors and posteriors are successful
                if p.rollbsrprior <= p.bsrscoreprior:
                    p.bsrsuccessprior = True
                else:
                    p.bsrsuccessprior = False
                if p.rollbsrposterior <= p.bsrscoreposterior:
                    p.bsrsuccessposterior = True
                else:
                    p.bsrsuccessposterior = False
                # determine final beliefs payment based on question paid
                if p.beliefquestion == 1:
                    p.payoffbelief = p.bsrsuccessprior * Constants.beliefpayment
                elif p.beliefquestion == 2:
                    p.payoffbelief = p.bsrsuccessposterior * Constants.beliefpayment
            p.participant.vars[
                'payoffbelief_' + str(self.round_number - Constants.num_prac_rounds)] = p.payoffbelief

            # store round outcomes in parvars
            p.participant.vars['droppedouteffort_' + str(self.round_number - Constants.num_prac_rounds)] = p.droppedouteffort
            p.participant.vars['leaderdroppedout_' + str(self.round_number - Constants.num_prac_rounds)] = self.leaderdroppedout
            p.participant.vars['groupreturnsuccess_' + str(self.round_number - Constants.num_prac_rounds)] = self.groupreturnsuccess
            p.participant.vars['groupreturnfailure_' + str(self.round_number - Constants.num_prac_rounds)] = self.groupreturnfailure
            p.participant.vars['droppedoutprior_' + str(self.round_number - Constants.num_prac_rounds)] = p.droppedoutprior
            p.participant.vars['droppedoutposterior_' + str(self.round_number - Constants.num_prac_rounds)] = p.droppedoutposterior

            # final round payoffs
            if p.leader:
                p.roundpayoff = p.payoffinvest
            else:
                # if leader drops out, toggle paidinvest = 1
                if self.leaderdroppedout:
                    p.paidinvest = True
                p.roundpayoff = p.paidinvest * p.payoffinvest + (1 - p.paidinvest) * p.payoffbelief
            p.participant.vars['roundpayoff_' + str(self.round_number - Constants.num_prac_rounds)] = p.roundpayoff

            # store payoffs as participant variables if this is the paid round
            if self.session.vars['task1roundpaid'] >= self.round_number - Constants.num_prac_rounds:  # paid round = round_number - num_prac_rounds
                p.participant.vars['leader'] = p.leader
                p.participant.vars['member'] = p.member
                p.participant.vars['PR_investendowment'] = Constants.endowment
                p.participant.vars['PR_leaderhigheffort'] = self.leaderhigheffort
                p.participant.vars['PR_costefforthigh'] = Constants.costefforthigh
                p.participant.vars['PR_costeffortlow'] = Constants.costeffortlow
                p.participant.vars['PR_prior'] = p.prior
                p.participant.vars['PR_posteriorsuccess'] = p.posteriorsuccess
                p.participant.vars['PR_posteriorfailure'] = p.posteriorfailure
                p.participant.vars['PR_groupreturnsuccess'] = self.groupreturnsuccess
                p.participant.vars['PR_groupreturnfailure'] = self.groupreturnfailure
                p.participant.vars['PR_groupinvestsuccess'] = self.groupinvestsuccess
                p.participant.vars['PR_bsrsuccessprior'] = p.bsrsuccessprior
                p.participant.vars['PR_bsrsuccessposterior'] = p.bsrsuccessposterior
                p.participant.vars['PR_payoffinvest'] = p.payoffinvest
                p.participant.vars['PR_payoffbelief'] = p.payoffbelief
                p.participant.vars['PR_beliefquestion'] = p.beliefquestion
                p.participant.vars['PR_paidinvest'] = p.paidinvest
                p.participant.vars['task1payoff'] = p.roundpayoff


class Player(BasePlayer):
    # function for dumping variables in participant vars field
    def participant_vars_dump(self, page):
        for field in page.form_fields:
            if Constants.num_rounds > 1:
                self.participant.vars[field + '_' + str(self.round_number-Constants.num_prac_rounds)] = getattr(self, field)
            else:
                self.participant.vars[field] = getattr(self, field)

    # treatment variable
    treatstrategy = models.BooleanField()

    # variables to capture task payments
    taskpaid = models.IntegerField()
    task1roundpaid = models.IntegerField()

    # define roles
    leader = models.BooleanField()
    member = models.BooleanField()

    # round number (within the set of paid rounds)
    paid_round_num = models.IntegerField()

    # variables for storing decisions
    higheffort = models.BooleanField()
    prior = models.IntegerField(
        min=0,
        max=100,
    )
    posteriorsuccess = models.IntegerField(
        min=0,
        max=100,
    )
    posteriorfailure = models.IntegerField(
        min=0,
        max=100,
    )

    # store BSR scores
    bsrscoreprior = models.FloatField()
    bsrscoreposterior = models.FloatField()

    # die roll for BSR score
    rollbsrprior = models.FloatField()
    rollbsrposterior = models.FloatField()

    # whether BSR was successful
    bsrsuccessprior = models.BooleanField()
    bsrsuccessposterior = models.BooleanField()

    # die roll for:
    # (i) belief question paid for members and
    # (ii) whether paid for investment or belief (always true for leaders)
    beliefquestion = models.IntegerField()
    paidinvest = models.BooleanField()

    # variables to store payoffs
    payoffinvest = models.IntegerField()
    payoffbelief = models.IntegerField()
    roundpayoff = models.IntegerField()

    # store whether subject drops out
    droppedouteffort = models.BooleanField(initial=False)
    droppedoutprior = models.BooleanField(initial=False)
    droppedoutposterior = models.BooleanField(initial=False)

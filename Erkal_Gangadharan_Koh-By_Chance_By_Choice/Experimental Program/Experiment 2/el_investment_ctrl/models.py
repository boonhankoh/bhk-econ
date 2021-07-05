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
from django import forms
from django.utils.safestring import mark_safe

author = 'Nisvan Erkal, Lata Gangadharan, Boon Han Koh'

doc = """
Effort/Luck Experiment (Revision): Investment Task Control Questions
"""


class Constants(BaseConstants):
    name_in_url = 'el_investment_ctrl'
    players_per_group = None
    num_rounds = 1
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


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            player.treatstrategy = self.session.config['treatstrategy']
        # print("Treat Strategy Method: " + str(self.session.config['treatstrategy']))

        for g in self.get_groups():
            g.groupreturnsuccess = Constants.returnsuccess[1]  # extracts return for success
            # print(Constants.returnsuccess[Constants.order_set[g.param-1][i]])
            g.groupreturnfailure = Constants.returnfailure[1]  # extracts return for failure
            # print(Constants.returnfailure[Constants.order_set[g.param-1][i]])


class Group(BaseGroup):
    # variables for storing parameters of a given round
    groupreturnsuccess = models.IntegerField()
    groupreturnfailure = models.IntegerField()


class Player(BasePlayer):
    # function for dumping variables in participant vars field
    def participant_vars_dump(self, page):
        for field in page.form_fields:
            if Constants.num_rounds > 1:
                self.participant.vars[field + '_' + str(self.round_number)] = getattr(self, field)
            else:
                self.participant.vars[field] = getattr(self, field)

    # treatment variable
    treatstrategy = models.BooleanField()

    ## ctrl questions
    # counter for errors (aggregate, if all questions on one page)
    ctrl_errors_count = models.IntegerField(
        initial=0
    )

    # correct answer: False
    ctrltaskpaid = models.BooleanField(
        widget=widgets.RadioSelect,
        label="",
        choices=[
            [True, "True"],
            [False, "False"],
        ]
    )
    ctrltaskpaid_errors_count = models.IntegerField(initial=0)

    def ctrltaskpaid_error_message(self, value):
        if value is not False:
            self.ctrltaskpaid_errors_count += 1
            self.ctrl_errors_count += 1
            return "This statement is false. You will be paid for your decisions in either Task 1 or Task 2 in today's experiment."

    # correct answer: True
    ctrltask1roundpaid = models.BooleanField(
        widget=widgets.RadioSelect,
        label="",
        choices=[
            [True, "True"],
            [False, "False"],
        ]
    )
    ctrltask1roundpaid_errors_count = models.IntegerField(initial=0)

    def ctrltask1roundpaid_error_message(self, value):
        if value is not True:
            self.ctrltask1roundpaid_errors_count += 1
            self.ctrl_errors_count += 1
            return "This statement is true. You will participate in three rounds in Task 1, and you will be paid for the decisions in one of the three rounds."

    # correct answer: True
    ctrlgroup = models.BooleanField(
        widget=widgets.RadioSelect,
        label="",
        choices=[
            [True, "True"],
            [False, "False"],
        ]
    )
    ctrlgroup_errors_count = models.IntegerField(initial=0)

    def ctrlgroup_error_message(self, value):
        if value is not True:
            self.ctrlgroup_errors_count += 1
            self.ctrl_errors_count += 1
            if self.treatstrategy:
                return "This statement is true. One group member will be assigned the role of the leader, and you will remain in the same group for all rounds of Task 1."
            else:
                return "This statement is true. One group member will be assigned the role of the leader, and you will remain in the same group and role for all rounds of Task 1."

    # correct answer: 2
    ctrlfeedback = models.IntegerField(
        widget=widgets.RadioSelect,
        label="",
        choices=[
            (1, "The other group members will be informed of the investment chosen by the leader, but not the amount they have received from the investment."),
            (2,	"The other group members will be informed of the amount they have received from the investment chosen by the leader, but not the investment chosen by him/her."),
            (3,	"The other group members will be informed of the investment chosen by the leader, and the amount they have received from the investment."),
        ]
    )
    ctrlfeedback_errors_count = models.IntegerField(initial=0)

    def ctrlfeedback_error_message(self, value):
        if value != 2:
            self.ctrlfeedback_errors_count += 1
            self.ctrl_errors_count += 1
            return "Your answer is incorrect. Remember: The other group members will learn how much they have received from the chosen investment, but they will never learn the leader's investment decision."

    # correct answer: 250
    ctrlpayoffmember = models.IntegerField(label="")
    ctrlpayoffmember_errors_count = models.IntegerField(initial=0)

    def ctrlpayoffmember_error_message(self, value):
        if value != 250:
            self.ctrlpayoffmember_errors_count += 1
            self.ctrl_errors_count += 1
            return "Your answer is incorrect. Remember: If you are not the leader, then your payoff in Stage 1 will be equal to the return from the investment chosen by your leader."

    # correct answer: 100
    ctrlpayoffleader = models.IntegerField(label="")
    ctrlpayoffleader_errors_count = models.IntegerField(initial=0)

    def ctrlpayoffleader_error_message(self, value):
        if value != 100:
            self.ctrlpayoffleader_errors_count += 1
            self.ctrl_errors_count += 1
            return "Your answer is incorrect. Remember: If you are the leader, then your payoff in Stage 1 will be equal to (300 ECU - the cost of the investment you have chosen + the return from the investment)."

    # correct answer: 3
    ctrlpaymentrole = models.IntegerField(
        widget=widgets.RadioSelect,
        label="",
        choices=[
            (1,
             "If I am the leader, then I will be paid for my decisions in Stage 2."),
            (2, "If I am not the leader, then I will be paid for BOTH my leader's decision in Stage 1 AND my decisions in Stage 2."),
            (3,
             "If I am not the leader, then I will be paid for EITHER my leader's decision in Stage 1 OR my decisions in Stage 2."),
        ]
    )
    ctrlpaymentrole_errors_count = models.IntegerField(initial=0)

    def ctrlpaymentrole_error_message(self, value):
        if value != 3:
            self.ctrlpaymentrole_errors_count += 1
            self.ctrl_errors_count += 1
            return "Your answer is incorrect. Remember: If you are the leader, then you will be paid according to your decision in Stage 1. If you are not the leader, then you will be paid either according to your leader's decision in Stage 1 or your prediction of your leader's decision in Stage 2."

    # correct answer: False
    ctrlbeliefpayment = models.BooleanField(
        widget=widgets.RadioSelect,
        label="",
        choices=[
            [True, "True"],
            [False, "False"],
        ]
    )
    ctrlbeliefpayment_errors_count = models.IntegerField(initial=0)

    def ctrlbeliefpayment_error_message(self, value):
        if value is not False:
            self.ctrlbeliefpayment_errors_count += 1
            self.ctrl_errors_count += 1
            return "This statement is false. If you are paid for Stage 2, then you will be paid according to your answers to either Question 1 or Question 2."

    # correct answer: 2
    ctrltruthtelling = models.IntegerField(
        widget=widgets.RadioSelect,
        label="",
        choices=[
            (1, "It is in my best interest to choose a high number as my prediction of the chance that my leader has chosen investment X."),
            (2, "It is in my best interest to choose a low number as my prediction of the chance that my leader has chosen investment X."),
            (3, "It is in my best interest to choose 50 as my prediction of the chance that my leader has chosen investment X."),
        ]
    )
    ctrltruthtelling_errors_count = models.IntegerField(initial=0)

    def ctrltruthtelling_error_message(self, value):
        if value !=2:
            self.ctrltruthtelling_errors_count += 1
            self.ctrl_errors_count += 1
            return "Your answer is incorrect. Remember: As a member, the payoff structure used to determine your payment in Stage 2 is designed such that it is in your best interest to report your true belief about your leader’s decision."

    # # error message below is for the case where all questions are on the same page
    # def error_message(self, value):
    #     correct_answers = {
    #         "ctrltaskpaid": False,
    #         "ctrltask1roundpaid": True,
    #         "ctrlgroup": True,
    #         "ctrlfeedback": 2,
    #         "ctrlpayoffmember": 250,
    #         "ctrlpayoffleader": 100,
    #         "ctrlbeliefpayment": False,
    #         "ctrltruthtelling": 2
    #     }
    #     if self.treatstrategy:
    #         correct_answers["ctrlstrategy"] = 3
    #     # print(correct_answers)
    #
    #     list_answers = list(value.items())[0:]
    #     list_correct_answers = list(correct_answers.items())
    #     list_ctrl_errors_count = [0] * len(correct_answers)
    #
    #     if list_answers != list_correct_answers:
    #         self.ctrl_errors_count = self.ctrl_errors_count + 1
    #
    #         indices = list(range(len(list_correct_answers)))
    #
    #         for i in range(len(indices)):
    #             if list_answers[i] != list_correct_answers[i]:
    #                 indices[i] = i + 1
    #                 list_ctrl_errors_count[i] = list_ctrl_errors_count[i] + 1
    #             else:
    #                 indices[i] = None
    #
    #         self.participant.vars['error_questions'] = indices
    #         # print(indices)
    #         return 'Please check your answers.'
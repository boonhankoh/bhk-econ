from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,

)
from custom_templates.custom_funcs import get_game_stats
from django.forms.models import model_to_dict
import json

# adds common functionality to Player Models for Data Pages
class DataPlayer(BasePlayer):
    score = models.IntegerField()
    group_scores = models.StringField(max_length=16) # unless we have 3 figure scores, list string shouldn't exceed 16 chars
    place = models.IntegerField()
    won_tiebreaker = models.BooleanField()
    potential_payouts = models.LongStringField()
    payout = models.FloatField()
    scheme = models.StringField(max_length=10)
    class Meta:
        abstract = True
    
    def stats(self):
        return (
            self.score,
            self.group_scores,
            self.place,
            self.won_tiebreaker
        )
    def calc_stats(self, game_name, participants, source_game=None):
        (
            self.score,
            group_scores,
            self.place,
            self.won_tiebreaker
        ) = get_game_stats(
            source_game or game_name,
            self,
            participants)
        self.group_scores = json.dumps(group_scores)

    def calc_potential_payouts(self, round_values, lam=lambda a:a):
        potential_payouts = {}
        for i in round_values:
            potential_payouts[i] = round(lam(float(i)) * self.score, 2)
        self.potential_payouts = json.dumps(potential_payouts)
        return potential_payouts
    
    def data(self):
        data = model_to_dict(self)
        base_attrs = (
            'id',
            'id_in_group',
            '_payoff',    
            'participant',    
            'session',    
            'round_number',    
            '_gbat_arrived',    
            '_gbat_grouped',    
            'subsession',    
            'group',
        )
        data = dict(filter(lambda elem: elem[0] not in base_attrs, data.items()))
        return data

    def dump_vars(self, game_name, parvars):
        data = self.data()
        for key, val in data.items():
            game_key = '%s_%s' % (game_name, key)
            if ('group_scores' in key):
                val = json.loads(val)
            parvars[game_key] = val
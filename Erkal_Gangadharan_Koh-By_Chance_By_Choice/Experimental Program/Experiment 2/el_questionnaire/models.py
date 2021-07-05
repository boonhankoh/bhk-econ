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
from django import forms
from django.utils.safestring import mark_safe
import random


author = 'Nisvan Erkal, Lata Gangadharan, Boon Han Koh'

doc = """
Effort/Luck Experiment (Revision): Post-Experimental Questionnaire
"""


class Constants(BaseConstants):
    name_in_url = 'el_questionnaire'
    players_per_group = None
    num_rounds = 1
    # timeout (before default decisions recorded
    timeout_default = 15
    # risk game parameters
    rg_endowment = 50
    rg_multiplier = 3

    nationalities = [
        ['Australian', 'Australian'],
        ['New Zealander', 'New Zealander'],
        ['Afghan', 'Afghan'],
        ['Albanian', 'Albanian'],
        ['Algerian', 'Algerian'],
        ['American', 'American'],
        ['Andorran', 'Andorran'],
        ['Angolan', 'Angolan'],
        ['Anguillan', 'Anguillan'],
        ['Argentine', 'Argentine'],
        ['Armenian', 'Armenian'],
        ['Austrian', 'Austrian'],
        ['Azerbaijani', 'Azerbaijani'],
        ['Bahamian', 'Bahamian'],
        ['Bahraini', 'Bahraini'],
        ['Bangladeshi', 'Bangladeshi'],
        ['Barbadian', 'Barbadian'],
        ['Belarusian', 'Belarusian'],
        ['Belgian', 'Belgian'],
        ['Belizean', 'Belizean'],
        ['Beninese', 'Beninese'],
        ['Bermudian', 'Bermudian'],
        ['Bhutanese', 'Bhutanese'],
        ['Bolivian', 'Bolivian'],
        ['Botswanan', 'Botswanan'],
        ['Brazilian', 'Brazilian'],
        ['British', 'British'],
        ['British Virgin Islander', 'British Virgin Islander'],
        ['Bruneian', 'Bruneian'],
        ['Bulgarian', 'Bulgarian'],
        ['Burkinan', 'Burkinan'],
        ['Burmese', 'Burmese'],
        ['Burundian', 'Burundian'],
        ['Cambodian', 'Cambodian'],
        ['Cameroonian', 'Cameroonian'],
        ['Canadian', 'Canadian'],
        ['Cape Verdean', 'Cape Verdean'],
        ['Cayman Islander', 'Cayman Islander'],
        ['Central African', 'Central African'],
        ['Chadian', 'Chadian'],
        ['Chilean', 'Chilean'],
        ['Chinese', 'Chinese'],
        ['Citizen of Antigua and Barbuda', 'Citizen of Antigua and Barbuda'],
        ['Citizen of Bosnia and Herzegovina', 'Citizen of Bosnia and Herzegovina'],
        ['Citizen of Guinea-Bissau', 'Citizen of Guinea-Bissau'],
        ['Citizen of Kiribati', 'Citizen of Kiribati'],
        ['Citizen of Seychelles', 'Citizen of Seychelles'],
        ['Citizen of the Dominican Republic', 'Citizen of the Dominican Republic'],
        ['Citizen of Vanuatu', 'Citizen of Vanuatu'],
        ['Colombian', 'Colombian'],
        ['Comoran', 'Comoran'],
        ['Congolese (Congo)', 'Congolese (Congo)'],
        ['Congolese (DRC)', 'Congolese (DRC)'],
        ['Cook Islander', 'Cook Islander'],
        ['Costa Rican', 'Costa Rican'],
        ['Croatian', 'Croatian'],
        ['Cuban', 'Cuban'],
        ['Cymraes', 'Cymraes'],
        ['Cymro', 'Cymro'],
        ['Cypriot', 'Cypriot'],
        ['Czech', 'Czech'],
        ['Danish', 'Danish'],
        ['Djiboutian', 'Djiboutian'],
        ['Dominican', 'Dominican'],
        ['Dutch', 'Dutch'],
        ['East Timorese', 'East Timorese'],
        ['Ecuadorean', 'Ecuadorean'],
        ['Egyptian', 'Egyptian'],
        ['Emirati', 'Emirati'],
        ['English', 'English'],
        ['Equatorial Guinean', 'Equatorial Guinean'],
        ['Eritrean', 'Eritrean'],
        ['Estonian', 'Estonian'],
        ['Ethiopian', 'Ethiopian'],
        ['Faroese', 'Faroese'],
        ['Fijian', 'Fijian'],
        ['Filipino', 'Filipino'],
        ['Finnish', 'Finnish'],
        ['French', 'French'],
        ['Gabonese', 'Gabonese'],
        ['Gambian', 'Gambian'],
        ['Georgian', 'Georgian'],
        ['German', 'German'],
        ['Ghanaian', 'Ghanaian'],
        ['Gibraltarian', 'Gibraltarian'],
        ['Greek', 'Greek'],
        ['Greenlandic', 'Greenlandic'],
        ['Grenadian', 'Grenadian'],
        ['Guamanian', 'Guamanian'],
        ['Guatemalan', 'Guatemalan'],
        ['Guinean', 'Guinean'],
        ['Guyanese', 'Guyanese'],
        ['Haitian', 'Haitian'],
        ['Honduran', 'Honduran'],
        ['Hong Konger', 'Hong Konger'],
        ['Hungarian', 'Hungarian'],
        ['Icelandic', 'Icelandic'],
        ['Indian', 'Indian'],
        ['Indonesian', 'Indonesian'],
        ['Iranian', 'Iranian'],
        ['Iraqi', 'Iraqi'],
        ['Irish', 'Irish'],
        ['Israeli', 'Israeli'],
        ['Italian', 'Italian'],
        ['Ivorian', 'Ivorian'],
        ['Jamaican', 'Jamaican'],
        ['Japanese', 'Japanese'],
        ['Jordanian', 'Jordanian'],
        ['Kazakh', 'Kazakh'],
        ['Kenyan', 'Kenyan'],
        ['Kittitian', 'Kittitian'],
        ['Kosovan', 'Kosovan'],
        ['Kuwaiti', 'Kuwaiti'],
        ['Kyrgyz', 'Kyrgyz'],
        ['Lao', 'Lao'],
        ['Latvian', 'Latvian'],
        ['Lebanese', 'Lebanese'],
        ['Liberian', 'Liberian'],
        ['Libyan', 'Libyan'],
        ['Liechtenstein citizen', 'Liechtenstein citizen'],
        ['Lithuanian', 'Lithuanian'],
        ['Luxembourger', 'Luxembourger'],
        ['Macanese', 'Macanese'],
        ['Macedonian', 'Macedonian'],
        ['Malagasy', 'Malagasy'],
        ['Malawian', 'Malawian'],
        ['Malaysian', 'Malaysian'],
        ['Maldivian', 'Maldivian'],
        ['Malian', 'Malian'],
        ['Maltese', 'Maltese'],
        ['Marshallese', 'Marshallese'],
        ['Martiniquais', 'Martiniquais'],
        ['Mauritanian', 'Mauritanian'],
        ['Mauritian', 'Mauritian'],
        ['Mexican', 'Mexican'],
        ['Micronesian', 'Micronesian'],
        ['Moldovan', 'Moldovan'],
        ['Monegasque', 'Monegasque'],
        ['Mongolian', 'Mongolian'],
        ['Montenegrin', 'Montenegrin'],
        ['Montserratian', 'Montserratian'],
        ['Moroccan', 'Moroccan'],
        ['Mosotho', 'Mosotho'],
        ['Mozambican', 'Mozambican'],
        ['Namibian', 'Namibian'],
        ['Nauruan', 'Nauruan'],
        ['Nepalese', 'Nepalese'],
        ['Nicaraguan', 'Nicaraguan'],
        ['Nigerian', 'Nigerian'],
        ['Nigerien', 'Nigerien'],
        ['Niuean', 'Niuean'],
        ['North Korean', 'North Korean'],
        ['Northern Irish', 'Northern Irish'],
        ['Norwegian', 'Norwegian'],
        ['Omani', 'Omani'],
        ['Pakistani', 'Pakistani'],
        ['Palauan', 'Palauan'],
        ['Palestinian', 'Palestinian'],
        ['Panamanian', 'Panamanian'],
        ['Papua New Guinean', 'Papua New Guinean'],
        ['Paraguayan', 'Paraguayan'],
        ['Peruvian', 'Peruvian'],
        ['Pitcairn Islander', 'Pitcairn Islander'],
        ['Polish', 'Polish'],
        ['Portuguese', 'Portuguese'],
        ['Prydeinig', 'Prydeinig'],
        ['Puerto Rican', 'Puerto Rican'],
        ['Qatari', 'Qatari'],
        ['Romanian', 'Romanian'],
        ['Russian', 'Russian'],
        ['Rwandan', 'Rwandan'],
        ['Salvadorean', 'Salvadorean'],
        ['Sammarinese', 'Sammarinese'],
        ['Samoan', 'Samoan'],
        ['Sao Tomean', 'Sao Tomean'],
        ['Saudi Arabian', 'Saudi Arabian'],
        ['Scottish', 'Scottish'],
        ['Senegalese', 'Senegalese'],
        ['Serbian', 'Serbian'],
        ['Sierra Leonean', 'Sierra Leonean'],
        ['Singaporean', 'Singaporean'],
        ['Slovak', 'Slovak'],
        ['Slovenian', 'Slovenian'],
        ['Solomon Islander', 'Solomon Islander'],
        ['Somali', 'Somali'],
        ['South African', 'South African'],
        ['South Korean', 'South Korean'],
        ['South Sudanese', 'South Sudanese'],
        ['Spanish', 'Spanish'],
        ['Sri Lankan', 'Sri Lankan'],
        ['St Helenian', 'St Helenian'],
        ['St Lucian', 'St Lucian'],
        ['Stateless', 'Stateless'],
        ['Sudanese', 'Sudanese'],
        ['Surinamese', 'Surinamese'],
        ['Swazi', 'Swazi'],
        ['Swedish', 'Swedish'],
        ['Swiss', 'Swiss'],
        ['Syrian', 'Syrian'],
        ['Taiwanese', 'Taiwanese'],
        ['Tajik', 'Tajik'],
        ['Tanzanian', 'Tanzanian'],
        ['Thai', 'Thai'],
        ['Togolese', 'Togolese'],
        ['Tongan', 'Tongan'],
        ['Trinidadian', 'Trinidadian'],
        ['Tristanian', 'Tristanian'],
        ['Tunisian', 'Tunisian'],
        ['Turkish', 'Turkish'],
        ['Turkmen', 'Turkmen'],
        ['Turks and Caicos Islander', 'Turks and Caicos Islander'],
        ['Tuvaluan', 'Tuvaluan'],
        ['Ugandan', 'Ugandan'],
        ['Ukrainian', 'Ukrainian'],
        ['Uruguayan', 'Uruguayan'],
        ['Uzbek', 'Uzbek'],
        ['Vatican citizen', 'Vatican citizen'],
        ['Venezuelan', 'Venezuelan'],
        ['Vietnamese', 'Vietnamese'],
        ['Vincentian', 'Vincentian'],
        ['Wallisian', 'Wallisian'],
        ['Welsh', 'Welsh'],
        ['Yemeni', 'Yemeni'],
        ['Zambian', 'Zambian'],
        ['Zimbabwean', 'Zimbabwean'],
        ['OTHER', 'Other (please state below)'],
    ]
    nationality_list = nationalities.copy()

    countries = [
        ['AU', 'Australia'],
        ['NZ', 'New Zealand'],
        ['AF', 'Afghanistan'],
        ['AL', 'Albania'],
        ['DZ', 'Algeria'],
        ['AD', 'Andorra'],
        ['AO', 'Angola'],
        ['AG', 'Antigua and Barbuda'],
        ['AR', 'Argentina'],
        ['AM', 'Armenia'],
        ['AT', 'Austria'],
        ['AZ', 'Azerbaijan'],
        ['BS', 'Bahamas'],
        ['BH', 'Bahrain'],
        ['BD', 'Bangladesh'],
        ['BB', 'Barbados'],
        ['BY', 'Belarus'],
        ['BE', 'Belgium'],
        ['BZ', 'Belize'],
        ['BJ', 'Benin'],
        ['BT', 'Bhutan'],
        ['BO', 'Bolivia (Plurinational State of)'],
        ['BA', 'Bosnia and Herzegovina'],
        ['BW', 'Botswana'],
        ['BR', 'Brazil'],
        ['BN', 'Brunei Darussalam'],
        ['BG', 'Bulgaria'],
        ['BF', 'Burkina Faso'],
        ['BI', 'Burundi'],
        ['CV', 'Cabo Verde'],
        ['KH', 'Cambodia'],
        ['CM', 'Cameroon'],
        ['CA', 'Canada'],
        ['CF', 'Central African Republic'],
        ['TD', 'Chad'],
        ['CL', 'Chile'],
        ['CN', 'China'],
        ['CO', 'Colombia'],
        ['KM', 'Comoros'],
        ['CG', 'Congo'],
        ['CK', 'Cook Islands'],
        ['CR', 'Costa Rica'],
        ['HR', 'Croatia'],
        ['CU', 'Cuba'],
        ['CY', 'Cyprus'],
        ['CZ', 'Czechia'],
        ['CI', 'Côte d\'Ivoire'],
        ['KP', 'Democratic People\'s Republic of Korea'],
        ['CD', 'Democratic Republic of the Congo'],
        ['DK', 'Denmark'],
        ['DJ', 'Djibouti'],
        ['DM', 'Dominica'],
        ['DO', 'Dominican Republic'],
        ['EC', 'Ecuador'],
        ['EG', 'Egypt'],
        ['SV', 'El Salvador'],
        ['GQ', 'Equatorial Guinea'],
        ['ER', 'Eritrea'],
        ['EE', 'Estonia'],
        ['SZ', 'Eswatini'],
        ['ET', 'Ethiopia'],
        ['FO', 'Faroe Islands'],
        ['FJ', 'Fiji'],
        ['FI', 'Finland'],
        ['FR', 'France'],
        ['GA', 'Gabon'],
        ['GM', 'Gambia'],
        ['GE', 'Georgia'],
        ['DE', 'Germany'],
        ['GH', 'Ghana'],
        ['GR', 'Greece'],
        ['GD', 'Grenada'],
        ['GT', 'Guatemala'],
        ['GN', 'Guinea'],
        ['GW', 'Guinea-Bissau'],
        ['GY', 'Guyana'],
        ['HT', 'Haiti'],
        ['HN', 'Honduras'],
        ['HU', 'Hungary'],
        ['IS', 'Iceland'],
        ['IN', 'India'],
        ['ID', 'Indonesia'],
        ['IR', 'Iran (Islamic Republic of)'],
        ['IQ', 'Iraq'],
        ['IE', 'Ireland'],
        ['IL', 'Israel'],
        ['IT', 'Italy'],
        ['JM', 'Jamaica'],
        ['JP', 'Japan'],
        ['JO', 'Jordan'],
        ['KZ', 'Kazakhstan'],
        ['KE', 'Kenya'],
        ['KI', 'Kiribati'],
        ['KW', 'Kuwait'],
        ['KG', 'Kyrgyzstan'],
        ['LA', 'Lao People\'s Democratic Republic'],
        ['LV', 'Latvia'],
        ['LB', 'Lebanon'],
        ['LS', 'Lesotho'],
        ['LR', 'Liberia'],
        ['LY', 'Libya'],
        ['LT', 'Lithuania'],
        ['LU', 'Luxembourg'],
        ['MG', 'Madagascar'],
        ['MW', 'Malawi'],
        ['MY', 'Malaysia'],
        ['MV', 'Maldives'],
        ['ML', 'Mali'],
        ['MT', 'Malta'],
        ['MH', 'Marshall Islands'],
        ['MR', 'Mauritania'],
        ['MU', 'Mauritius'],
        ['MX', 'Mexico'],
        ['FM', 'Micronesia (Federated States of)'],
        ['MC', 'Monaco'],
        ['MN', 'Mongolia'],
        ['ME', 'Montenegro'],
        ['MA', 'Morocco'],
        ['MZ', 'Mozambique'],
        ['MM', 'Myanmar'],
        ['NA', 'Namibia'],
        ['NR', 'Nauru'],
        ['NP', 'Nepal'],
        ['NL', 'Netherlands'],
        ['NI', 'Nicaragua'],
        ['NE', 'Niger'],
        ['NG', 'Nigeria'],
        ['NU', 'Niue'],
        ['MK', 'North Macedonia'],
        ['NO', 'Norway'],
        ['OM', 'Oman'],
        ['PK', 'Pakistan'],
        ['PW', 'Palau'],
        ['PA', 'Panama'],
        ['PG', 'Papua New Guinea'],
        ['PY', 'Paraguay'],
        ['PE', 'Peru'],
        ['PH', 'Philippines'],
        ['PL', 'Poland'],
        ['PT', 'Portugal'],
        ['QA', 'Qatar'],
        ['KR', 'Republic of Korea'],
        ['MD', 'Republic of Moldova'],
        ['RO', 'Romania'],
        ['RU', 'Russian Federation'],
        ['RW', 'Rwanda'],
        ['KN', 'Saint Kitts and Nevis'],
        ['LC', 'Saint Lucia'],
        ['VC', 'Saint Vincent and the Grenadines'],
        ['WS', 'Samoa'],
        ['SM', 'San Marino'],
        ['ST', 'Sao Tome and Principe'],
        ['SA', 'Saudi Arabia'],
        ['SN', 'Senegal'],
        ['RS', 'Serbia'],
        ['SC', 'Seychelles'],
        ['SL', 'Sierra Leone'],
        ['SG', 'Singapore'],
        ['SK', 'Slovakia'],
        ['SI', 'Slovenia'],
        ['SB', 'Solomon Islands'],
        ['SO', 'Somalia'],
        ['ZA', 'South Africa'],
        ['SS', 'South Sudan'],
        ['ES', 'Spain'],
        ['LK', 'Sri Lanka'],
        ['SD', 'Sudan'],
        ['SR', 'Suriname'],
        ['SE', 'Sweden'],
        ['CH', 'Switzerland'],
        ['SY', 'Syrian Arab Republic'],
        ['TJ', 'Tajikistan'],
        ['TH', 'Thailand'],
        ['TL', 'Timor-Leste'],
        ['TG', 'Togo'],
        ['TK', 'Tokelau'],
        ['TO', 'Tonga'],
        ['TT', 'Trinidad and Tobago'],
        ['TN', 'Tunisia'],
        ['TR', 'Turkey'],
        ['TM', 'Turkmenistan'],
        ['TV', 'Tuvalu'],
        ['UG', 'Uganda'],
        ['UA', 'Ukraine'],
        ['AE', 'United Arab Emirates'],
        ['GB', 'United Kingdom of Great Britain and Northern Ireland'],
        ['TZ', 'United Republic of Tanzania'],
        ['US', 'United States of America'],
        ['UY', 'Uruguay'],
        ['UZ', 'Uzbekistan'],
        ['VU', 'Vanuatu'],
        ['VE', 'Venezuela (Bolivarian Republic of)'],
        ['VN', 'Viet Nam'],
        ['YE', 'Yemen'],
        ['ZM', 'Zambia'],
        ['ZW', 'Zimbabwe'],
        ['OTHER', 'Other (please state below)'],
    ]
    country_born_list = countries.copy()


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            # determine whether investment was successful
            p.risk_success = random.choice([True, False])
            # toggle survey part number
            p.participant.vars['survey_part'] = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # function for dumping variables in participant vars field
    def participant_vars_dump(self, page):
        for field in page.form_fields:
            if Constants.num_rounds > 1:
                self.participant.vars[field + '_' + str(self.round_number)] = getattr(self, field)
            else:
                self.participant.vars[field] = getattr(self, field)

    # variables to store inputs
    comments_general = models.LongStringField(
        label="In general, what do you think of the experiment today?",
    )

    comments_unclear = models.LongStringField(
        label="Were there any parts of the experiment that were not clear to you? If yes, please explain briefly.",
    )

    year_birth = models.IntegerField(
        label="What is your year of birth?",
        min=1900,
        max=2005,
    )

    female = models.IntegerField(
        label="What is your gender?",
        choices=[
            [0, 'Male'],
            [1, 'Female'],
            [-1, 'Trans/Intersex/Other'],
        ]
    )

    study_field = models.StringField(
        label="What is your main field of study at the University?",
        choices=[
            'Agriculture',
            'Arts/ Social Sciences',
            'Biomedicine',
            'Commerce (non-Economics)',
            'Commerce (Economics)',
            'Dentistry/ Oral Health',
            'Education',
            'Engineering',
            'Environments',
            'Fine Arts',
            'Law',
            'Medicine',
            'Music',
            'Nursing',
            'Pharmacy',
            'Psychology',
            'Science',
            'Veterinary Science',
            'Other',
            'Not a student',
        ]
    )

    study_lvl = models.StringField(
        label="Are you an undergraduate or a graduate student?",
        choices=[
            '1st-year undergraduate',
            '2nd-year undergraduate',
            '3rd-year undergraduate',
            '4th-year undergraduate',
            'Graduate student',
            'Not a student',
        ]
    )

    gpa = models.StringField(
        label="What is your (current) average GPA?",
        choices=[
            'H1 (80%-100%)',
            'H2A (75%-79%)',
            'H2B (70%-74%)',
            'H3 (65%-69%)',
            'P (50%-64%)',
            'N (0%-49%)',
            'Not applicable (first semester at University or not a student)',
        ]
    )

    nationality = models.StringField(
        label="What is your nationality?",
        choices=Constants.nationality_list,
    )
    other_nationality = models.StringField(
        label='',
        blank=True,
    )

    # def other_nationality_error_message(self, value):
    #     if self.nationality != "OTHER" and type(value) != type(None):
    #         return 'If you did not select Other, this field should be left blank.'
    #     if self.nationality == "OTHER" and type(value) == type(None):
    #         return 'If you select Other, you must specify in the provided field.'

    country_born = models.StringField(
        label="In what country were you born?",
        choices=Constants.country_born_list
    )
    other_country_born = models.StringField(
        label='',
        blank=True,
    )

    # def other_country_born_error_message(self, value):
    #     if self.country_born != "OTHER" and type(value) != type(None):
    #         return 'If you did not select Other, this field should be left blank.'
    #     if self.country_born == "OTHER" and type(value) == type(None):
    #         return 'If you select Other, you must specify in the provided field.'

    years_lived_australia = models.StringField(
        label="How long have you lived in Australia?",
        choices=[
            'Born in Australia',
            'More than 5 years',
            '2-5 years',
            '1-2 years',
            'Less than 1 year',
        ]
    )

    past_experiments = models.IntegerField(
        label="How many economics experiments have you participated in before this one?",
        min=0,
        max=999,
    )

    reasons_effort_general = models.LongStringField(
        label="What were the factors you considered when making your investment decisions?",
    )

    def reasons_effort_general_error_message(self, value):
        if len(value) < 5:
            return 'Your response to this question must be at least 5 characters long.'

    effort_fac_leader_payoff = models.BooleanField(
        label='I made my decisions based on the expected payoff that I will receive.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    effort_fac_member_payoff = models.BooleanField(
        label='I made my decisions based on the expected payoff that my members will receive.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    effort_fac_diff_return = models.BooleanField(
        label='I made my decisions based on the differences between the returns of the investment if it succeeds versus if it fails.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    # effort_fac_diff_cost = models.BooleanField(
    #     label='I made my decisions based on the differences in the costs of the investments.',
    #     widget=widgets.CheckboxInput,
    #     initial=False,
    #     blank=True,
    # )
    effort_fac_zero = models.BooleanField(
        label='I made my decisions based on the fact that my members will receive 0 ECU if the investment I choose fails.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    effort_fac_none = models.BooleanField(
        label='None of the above applies to me.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )

    reasons_beliefs_general = models.LongStringField(
        label="What were the factors you considered when stating your predictions of your leader's decisions?",
    )

    def reasons_beliefs_general_error_message(self, value):
        if len(value) < 5:
            return 'Your response to this question must be at least 5 characters long.'

    belief_fac_leader_payoff = models.BooleanField(
        label='I made my predictions based on the expected payoff that my leader will receive.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    belief_fac_strategy = models.BooleanField(
        label='I made my predictions based on what I would do if I were the leader.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    belief_fac_member_payoff = models.BooleanField(
        label='I made my predictions based on the expected payoff that I will receive.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    belief_fac_diff_return = models.BooleanField(
        label='I made my predictions based on the differences between the returns of the investment if it succeeds versus if it fails.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    # belief_fac_diff_cost = models.BooleanField(
    #     label='I made my predictions based on the differences in the costs of the investments.',
    #     widget=widgets.CheckboxInput,
    #     initial=False,
    #     blank=True,
    # )
    belief_fac_zero = models.BooleanField(
        label='I made my predictions based on the fact that I will receive 0 ECU if the investment chosen by my leader fails.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )
    belief_fac_none = models.BooleanField(
        label='None of the above applies to me.',
        widget=widgets.CheckboxInput,
        initial=False,
        blank=True,
    )

    belief_dictator_gave = models.IntegerField(
        label='Out of 300 ECU, how many ECU on average do you think the other participants in your session have transferred to their matched partner?',
        widget=widgets.RadioSelect,
        choices=[
            [0, '0 ECU'],
            [1, '1 to 50 ECU'],
            [2, '51 to 100 ECU'],
            [3, '101 to 149 ECU'],
            [4, '150 ECU'],
            [5, '151 to 200 ECU'],
            [6, '201 to 250 ECU'],
            [7, '251 to 300 ECU'],
        ],
    )

    risk_invest = models.IntegerField(
        label='How many ECU would you like to invest?',
        min=0,
        max=Constants.rg_endowment,
    )

    risk_keep = models.IntegerField(
        label='How many ECU would you like to keep?',
        min=0,
        max=Constants.rg_endowment,
    )

    risk_payoff = models.IntegerField()
    risk_success = models.BooleanField()

    droppedoutRG = models.BooleanField()

    # risk game payoffs
    def set_risk_payoffs(self):
        if self.participant.vars['is_dropout'] is False:
            if self.risk_success:
                self.risk_payoff = self.risk_invest * Constants.rg_multiplier + self.risk_keep
            else:
                self.risk_payoff = self.risk_keep
            self.participant.vars['risk_payoff'] = self.risk_payoff
            self.participant.vars['risk_success'] = self.risk_success

    payID1 = models.StringField(
        label='Please enter the email address or phone number you used to register for PayID.',
        initial="",
    )
    payID2 = models.StringField(
        label='Please confirm by entering the email address or phone number you used to register for PayID again.',
        initial="",
    )


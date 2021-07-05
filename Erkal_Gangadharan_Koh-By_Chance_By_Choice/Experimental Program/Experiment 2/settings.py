from os import environ

SESSION_CONFIGS = [
    dict(
        name='effort_luck_SM',
        display_name='Effort/Luck Experiment (Strategy Method)',
        num_demo_participants=12,
        app_sequence=['el_admin', 'el_investment_ctrl', 'el_investment_task', 'el_dictator_task', 'el_questionnaire', 'el_exp_outcome', 'el_end'],
        show_up=5,
        dollar_convert=20,
        treatstrategy=1,
        startingparam=2,
        task1link='https://docs.google.com/document/d/1c3xHILlgh0Bf2PxGvyw4mCsXp2HnvK06QBLS-gQFULU/edit?usp=sharing',
        task1summarylink='https://docs.google.com/document/d/1c3xHILlgh0Bf2PxGvyw4mCsXp2HnvK06QBLS-gQFULU/edit#bookmark=id.6wkihougyf1g',
        task2link='https://docs.google.com/document/d/1Vbe6ETKjGrCMZ58w7zsg-t9xhxMeQWu9VuxvTeztpXc/edit?usp=sharing',
    ),
    dict(
        name='effort_luck_NSM',
        display_name='Effort/Luck Experiment (Non-Strategy Method)',
        num_demo_participants=12,
        app_sequence=['el_admin', 'el_investment_ctrl', 'el_investment_task', 'el_dictator_task', 'el_questionnaire', 'el_exp_outcome', 'el_end'],
        show_up=5,
        dollar_convert=20,
        treatstrategy=0,
        startingparam=2,
        task1link='https://docs.google.com/document/d/1b2QtYacavB3X25fpSJuMTwkZQzXvmLESxFqk3c5lEVQ/edit?usp=sharing',
        task1summarylink='https://docs.google.com/document/d/1b2QtYacavB3X25fpSJuMTwkZQzXvmLESxFqk3c5lEVQ/edit#bookmark=id.p5z5186maqid',
        task2link='https://docs.google.com/document/d/1Vbe6ETKjGrCMZ58w7zsg-t9xhxMeQWu9VuxvTeztpXc/edit?usp=sharing',
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AUD'
USE_POINTS = False

ROOMS = [
    dict(
        name='el_1',
        display_name='Experiments in Group Decision Making 1',
        participant_label_file='_rooms/EMU.txt',
    ),
    dict(
        name='el_2',
        display_name='Experiments in Group Decision Making 2',
        participant_label_file='_rooms/EMU.txt',
    ),
    dict(
        name='el_3',
        display_name='Experiments in Group Decision Making 3',
        participant_label_file='_rooms/EMU.txt',
    ),
    dict(
        name='el_4',
        display_name='Experiments in Group Decision Making 4',
        participant_label_file='_rooms/EMU.txt',
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
    'custom_templates',
    'django.contrib.humanize',
    'otreeutils',
]

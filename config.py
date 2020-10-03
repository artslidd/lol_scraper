import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

name_to_contraction = {
    'DAMWON Gaming': 'DWG',
    'G2 Esports': 'G2',
    'Fnatic': 'FNC',
    'Rogue': 'RGE',
    'Gen.G': 'GEN',
    'DRX': 'DRX',
    'Top Esports': 'TES',
    'JD Gaming': 'JDG',
    'Suning': 'SN',
    'Machi Esports': 'MCX',
    'Team SoloMid': 'TSM',
    'FlyQuest': 'FLY',
    'LGD Gaming': 'LGD',
    'Team Liquid': 'TL',
    'Unicorns Of Love': 'UOL',
    'PSG Talon': 'PSG',
    'TBD': 'TBD'
}


def initialize_app():
    cred = credentials.Certificate("esport-data-firebase-adminsdk-szgs8-13acfca0b3.json")
    firebase_admin.initialize_app(cred)
    # db is the firestore database of hook up
    db = firestore.client()

    return db
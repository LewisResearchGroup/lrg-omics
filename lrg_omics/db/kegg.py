from Bio.KEGG import REST

def get(ID='K18766', db=None):
    db_keys = {
        'orthology': 'ko',
        'enzyme': 'ec',
        'compound': 'cpd',
        'reaction': 'rn'
    }
    if db is not None:
        db_key = db_keys[db]
    elif ID.startswith('C'):
        db_key = db_keys['compound']
    elif ID.startswith('K'):
        db_key = db_keys['orthology']
    elif ID.startswith('R'):
        db_key = db_keys['reaction']
    else:
        db_key = db_keys['enzyme']
    
    data = REST.kegg_get(f"{db_key}:{ID}").read().split('\n')
    return data
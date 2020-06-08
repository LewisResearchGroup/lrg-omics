from .config import ENGINE, ROOT
from sqlalchemy import create_engine


if ENGINE == 'postgres':
    # Postgres
    PGPW = os.getenv('POSTGRES')
    with open('/home/swacker/Documents/Postgres/postgres.txt') as file:
        PGPW = file.readline().split()[1]
    PGUSER = 'postgres'
    PGDB = 'proteomics'
    PGHOST = 'localhost'
    PGPORT = 5432

def get_engine():
    if ENGINE == 'postgres':
        engine = create_engine(f'postgresql://{PGUSER}:{PGPW}@{PGHOST}:{PGPORT}/{PGDB}')
    elif ENGINE == 'sqlite':
        engine = create_engine(ROOT/P('proteomics.db'), echo=False)
    return engine

def init_tables():
    setup_rawtoolsfiles()

def setup_rawtoolsfiles():
    engine = get_engine()
    tablename = 'RawToolsFiles'
    engine.execute("""DROP TABLE IF EXISTS "%s" """ % (tablename))
    engine.execute("""CREATE TABLE "%s" (
                  "RawFile" TEXT,
                  "RawToolsMetricsFile" TEXT,
                  "RawToolsMatrixFile" TEXT,
                  CONSTRAINT pk PRIMARY KEY ("RawFile"))
                  """ % (tablename))

def setup_maxquant_ms3_files():
    engine = get_engine()
    tablename = 'RawToolsFiles'
    engine.execute("""DROP TABLE IF EXISTS "%s" """ % (tablename))
    engine.execute("""CREATE TABLE "%s" (
                  "RawFile" TEXT,
                  "RawToolsMetricsFile" TEXT,
                  "RawToolsMatrixFile" TEXT,
                  CONSTRAINT pk PRIMARY KEY ("RawFile"))
                  """ % (tablename))

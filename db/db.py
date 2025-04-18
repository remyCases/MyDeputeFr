# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import DB_URL, DB_ECHO

from db.models import *

__engine = create_engine(DB_URL, echo=DB_ECHO)
__Session = sessionmaker(bind=__engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = __Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def init_db() -> None:
    from db.loader import load_from_json
    Base.metadata.drop_all(bind=__engine)
    Base.metadata.create_all(bind=__engine)
    load_from_json()


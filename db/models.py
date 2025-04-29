# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from typing import Callable, Any

from sqlalchemy import String, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
)
from unidecode import unidecode

from utils.utils import normalize_name


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def normalize_field(field_name: str) -> Callable:
    """
    Returns a function that normalizes a given field from the SQLAlchemy context.

    Args:
        field_name (str): The name of the field to normalize.

    Returns:
        Callable: A function usable as a SQLAlchemy default/onupdate callable.
    """

    def _normalize(context) -> str:
        original_value = context.current_parameters.get(field_name)
        if original_value is None:
            raise Exception("Invalid filed name")
        return normalize_name(original_value)

    return _normalize

class Depute(Base):
    """
    Represents a deputy (député) with identification, constituency, and group affiliations.

    Attributes:
        id (str): Unique identifier for the deputy.
        last_name (str): Deputy's last name.
        last_name_normalize (str): Normalized last name (lowercase, accent-free).
        first_name (str): Deputy's first name.
        first_name_normalize (str): Normalized first name (lowercase, accent-free).
        gp_id (int): Foreign key linking to the parliamentary group.
        gp (GroupParlementaire): Relationship to the deputy's group.
        circo_departement_code (str): Department number of the constituency.
        circo_code (int): Constituency number within the department.
        circo (Circonscription): Relationship to the constituency.
    """
    __tablename__ = "depute"

    id: Mapped[str] = mapped_column(String(), primary_key=True)

    last_name: Mapped[str] = mapped_column(String())
    last_name_normalize: Mapped[str] = mapped_column(
        String(), default=normalize_field('last_name'), onupdate=normalize_field('last_name'), index=True
    )

    first_name: Mapped[str] = mapped_column(String())
    first_name_normalize: Mapped[str] = mapped_column(
        String(), default=normalize_field('first_name'), onupdate=normalize_field('first_name'), index=True
    )

    gp_id: Mapped[int] = mapped_column(ForeignKey("groupe_parlementaire.id"))
    gp: Mapped["GroupParlementaire"] = relationship(back_populates="members")

    circo_departement_code: Mapped[str] = mapped_column(String())
    circo_code: Mapped[int] = mapped_column(Integer())
    circo: Mapped["Circonscription"] = relationship(back_populates="representative")

    __table_args__ = (ForeignKeyConstraint(
        ['circo_departement_code', 'circo_code'],
        ['circonscription.departement_code', 'circonscription.code']
    ), {})

    @property
    def url(self) -> str:
        """
        URL to the official page of the deputy.

        Returns:
            str: Web URL to the deputy's profile.
        """
        return f"https://www.assemblee-nationale.fr/dyn/deputes/{self.id}"

    @property
    def image(self) -> str:
        """
        URL to the deputy's official portrait image.

        Returns:
            str: Image URL of the deputy.
        """
        return f"https://www.assemblee-nationale.fr/dyn/static/tribun/17/photos/carre/{self.id[2:]}.jpg"


class GroupParlementaire(Base):
    """
    Represents a parliamentary group (groupe parlementaire).

    Attributes:
        id (str): Unique identifier of the group.
        name (str): Name of the parliamentary group.
        members (list[Depute]): Deputies associated with the group.
    """
    __tablename__ = "groupe_parlementaire"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String(), index=True)

    members: Mapped[list["Depute"]] = relationship(
        back_populates="gp"
    )


class Circonscription(Base):
    """
    Represents an electoral district (circonscription).

    Attributes:
        departement_code (str): Foreign key to the related department.
        departement (Departement): Department this constituency belongs to.
        code (int): Constituency number within the department.
        representative (Depute): Deputy representing this constituency.
    """
    __tablename__ = "circonscription"

    departement_code: Mapped[str] = mapped_column(ForeignKey("departement.code"), primary_key=True)
    departement: Mapped["Departement"] = relationship(back_populates="circonscriptions")

    code: Mapped[int] = mapped_column(Integer(), primary_key=True)

    representative: Mapped["Depute"] = relationship(
        back_populates="circo"
    )


class Departement(Base):
    """
    Represents a French administrative department.

    Attributes:
        code (str): Unique identifier for the department.
        name (str): Name of the department.
        region_id (int): Foreign key to the associated region.
        region (Region): Region this department belongs to.
        circonscriptions (list[Circonscription]): Constituencies in the department.
    """
    __tablename__ = "departement"

    code: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String(), index=True)

    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    region: Mapped["Region"] = relationship(back_populates="departements")

    circonscriptions: Mapped[list["Circonscription"]] = relationship(
        back_populates="departement"
    )


class Region(Base):
    """
    Represents a French administrative region.

    Attributes:
        id (int): Unique identifier of the region.
        name (str): Name of the region.
        departements (list[Departement]): Departments within the region.
    """
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True, index=True)

    departements: Mapped[list["Departement"]] = relationship(
        back_populates="region"
    )

# class SortEnum(enum.Enum):
#     """Enumeration of possible outcomes of a scrutiny (vote)."""
#     ADOPTE = "adopté"
#     REJETE = "rejeté"
#
#
# class Scrutin(Base):
#     """
#     Represents a parliamentary vote (scrutin).
#
#     Attributes:
#         id (int): Unique identifier of the vote.
#         titre (str): Title or description of the vote.
#         dateScrutin (datetime): Date when the vote took place.
#         sort (SortEnum): Outcome of the vote (adopted or rejected).
#     """
#     __tablename__ = "scrutin"
#
#     id: Mapped[int] = mapped_column(Integer(), primary_key=True)
#     titre: Mapped[str] = mapped_column(String())
#     dateScrutin: Mapped[datetime] = mapped_column(DateTime())
#     sort: Mapped[SortEnum] = mapped_column(Enum(SortEnum))

from datetime import date


def build_publication_date(
        year:int|None,
        month:int|None=None,
        day:int|None=None
)->date|None:
    if year is None:
        return None
    month=month or 1
    day=day or 1
    try:
        return date(year, month,day)
    except ValueError:
        return date(year,1,1)
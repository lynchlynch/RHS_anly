def month_abbr(year,month):
    year = int(year)
    month = int(month)
    if month == 1:
        year_month = str(year-2000) + '-Jan'
    elif month == 2:
        year_month = str(year-2000) + '-Feb'
    elif month == 3:
        year_month = str(year-2000) + '-Mar'
    elif month == 4:
        year_month = str(year-2000) + '-Apr'
    elif month == 5:
        year_month = str(year-2000) + '-May'
    elif month == 6:
        year_month = str(year-2000) + '-Jun'
    elif month == 7:
        year_month = str(year-2000) + '-Jul'
    elif month == 8:
        year_month = str(year-2000) + '-Aug'
    elif month == 9:
        year_month = str(year-2000) + '-Sep'
    elif month == 10:
        year_month = str(year-2000) + '-Oct'
    elif month == 11:
        year_month = str(year-2000) + '-Nov'
    else:
        year_month = str(year-2000) + '-Dec'
    return year_month
class Event:
    def __init__(
        self,
        event_id: str,
        sport: str,
        home_team_abbrev: str,
        away_team_abbrev: str,
        home_team_name: str,
        away_team_name: str,
        home_team_score: int,
        away_team_score: int,
        winning_team_abbrev: str,
        losing_team_abbrev: str,
        date: str
    ):
        self.event_id = event_id
        self.sport = sport
        self.home_team_abbrev = home_team_abbrev
        self.away_team_abbrev = away_team_abbrev
        self.home_team_name = home_team_name
        self.away_team_name = away_team_name
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.winning_team_abbrev = winning_team_abbrev
        self.losing_team_abbrev = losing_team_abbrev
        self.date = date
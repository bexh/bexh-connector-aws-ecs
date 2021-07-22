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


class ExecutedBet:
    def __init__(self, bet_id: int, brokerage_id: int, user_id: int, amount: float, status: str):
        """
        :param bet_id:
        :param brokerage_id:
        :param user_id:
        :param amount:
        :param status: BetStatus = Literal["EXECUTED", "PARTIALLY_EXECUTED", "CANCELLED", "EXPIRED_EVENT", "INSUFFICIENT_VOLUME"]
        """
        self.bet_id = bet_id
        self.brokerage_id = brokerage_id
        self.user_id = user_id
        self.amount = amount
        self.status = status


class Bet:
    def __init__(
        self,
        event_id: str,
        sport: str,
        execution_time: str,
        odds: int,
        winning_team_abbrev: str,
        bet_id: int,
        brokerage_id: int,
        user_id: int,
        amount: float,
        status: str
    ):
        self.event_id = event_id
        self.sport = sport
        self.execution_time = execution_time
        self.odds = odds
        self.winning_team_abbrev = winning_team_abbrev
        self.bet_id = bet_id
        self.brokerage_id = brokerage_id
        self.user_id = user_id
        self.amount = amount
        self.status = status


class ExecutedBets:
    def __init__(
            self,
            event_id: str,
            sport: str,
            bets: [dict],
            execution_time: str,
            odds: int = None,
            winning_team_abbrev: str = None
    ):
        self.event_id = event_id
        self.sport = sport
        self.odds = odds
        self.execution_time = execution_time
        self.bets: [ExecutedBet] = list(map(lambda bet: ExecutedBet(**bet), bets))
        self.winning_team_abbrev = winning_team_abbrev

    def to_bets(self) -> [Bet]:
        bets = []
        for bet in self.bets:
            bets.append(Bet(
                event_id=self.event_id,
                sport=self.sport,
                execution_time=self.execution_time,
                odds=self.odds,
                winning_team_abbrev=self.winning_team_abbrev,
                bet_id=bet.bet_id,
                brokerage_id=bet.brokerage_id,
                user_id=bet.user_id,
                amount=bet.amount,
                status=bet.status,
            ))
        return bets

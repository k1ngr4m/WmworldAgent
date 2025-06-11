from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class Player:
    playerId: str
    nickName: str
    team: str
    kills: int
    deaths: int
    assists: int
    headShot: Optional[str]
    headShotCount: Optional[int]
    headShotRatio: Optional[float]
    rating: float
    pwRating: float
    flash: int
    flashTeammate: int
    flashSuccess: int
    mvpValue: float
    twoKill: int
    threeKill: int
    fourKill: int
    fiveKill: int
    vs1: int
    vs2: int
    vs3: int
    vs4: int
    vs5: int
    dmgArmor: int
    dmgHealth: int
    adpr: float
    fireCount: int
    hitCount: int
    rws: float
    pvpTeam: str
    ranks: int
    we: float
    throwsCnt: int
    teamId: str
    snipeNum: int
    entryKill: int
    firstDeath: int
    mvp: int
    kast: float
    handGunKill: int
    awpKill: int
    entryDeath: int
    botKill: int
    negKill: int
    damage: int
    multiKills: int
    itemThrow: int
    score: int
    endGame: bool
    oldRank: str
    pvpScore: float
    pvpScoreChange: float
    matchScore: float
    kda: Optional[float] = None
    win: Optional[int] = None

    @classmethod
    def from_raw_data(cls, raw_data: Dict[str, Any]) -> "Player":
        return cls(
    playerId=raw_data.get('playerId'),
    nickName=raw_data.get('nickName', ''),
    team=raw_data.get('team', ''),
    kills=raw_data.get('kills'),
    deaths=raw_data.get('deaths'),
    assists=raw_data.get('assists'),
    headShot=raw_data.get('headShot'),
    headShotCount=raw_data.get('headShotCount'),
    headShotRatio=raw_data.get('headShotRatio'),
    rating=raw_data.get('rating', 0.0),
    pwRating=raw_data.get('pwRating', 0.0),
    flash=raw_data.get('flash', 0),
    flashTeammate=raw_data.get('flashTeammate', 0),
    flashSuccess=raw_data.get('flashSuccess', 0),
    mvpValue=raw_data.get('mvpValue', 0.0),
    twoKill=raw_data.get('twoKill', 0),
    threeKill=raw_data.get('threeKill', 0),
    fourKill=raw_data.get('fourKill', 0),
    fiveKill=raw_data.get('fiveKill', 0),
    vs1=raw_data.get('vs1', 0),
    vs2=raw_data.get('vs2', 0),
    vs3=raw_data.get('vs3', 0),
    vs4=raw_data.get('vs4', 0),
    vs5=raw_data.get('vs5', 0),
    dmgArmor=raw_data.get('dmgArmor', 0),
    dmgHealth=raw_data.get('dmgHealth', 0),
    adpr=raw_data.get('adpr', 0.0),
    fireCount=raw_data.get('fireCount', 0),
    hitCount=raw_data.get('hitCount', 0),
    rws=raw_data.get('rws', 0.0),
    pvpTeam=raw_data.get('pvpTeam', ''),
    ranks=raw_data.get('ranks', 0),
    we=raw_data.get('we', 0.0),
    throwsCnt=raw_data.get('throwsCnt', 0),
    teamId=raw_data.get('teamId', ''),
    snipeNum=raw_data.get('snipeNum', 0),
    entryKill=raw_data.get('entryKill', 0),
    firstDeath=raw_data.get('firstDeath', 0),
    mvp=raw_data.get('mvp', 0),
    kast=raw_data.get('kast', 0.0),
    handGunKill=raw_data.get('handGunKill', 0),
    awpKill=raw_data.get('awpKill', 0),
    entryDeath=raw_data.get('entryDeath', 0),
    botKill=raw_data.get('botKill', 0),
    negKill=raw_data.get('negKill', 0),
    damage=raw_data.get('damage', 0),
    multiKills=raw_data.get('multiKills', 0),
    itemThrow=raw_data.get('itemThrow', 0),
    score=raw_data.get('score', 0),
    endGame=raw_data.get('endGame', False),
    oldRank=raw_data.get('oldRank', ''),
    pvpScore=raw_data.get('pvpScore', 0.0),
    pvpScoreChange=raw_data.get('pvpScoreChange', 0.0),
    matchScore=raw_data.get('matchScore', 0.0),
    kda=raw_data.get('kda'),
    win=raw_data.get('win')
)


@dataclass
class MatchBase:
    match_id: int
    map_name: str
    map_en: str
    start_time: datetime
    end_time: datetime
    duration: int
    win_team: str
    score1: int
    score2: int
    team1_pvp_id: Optional[str] = None
    team2_pvp_id: Optional[str] = None
    pvp_ladder: Optional[str] = None
    mode: Optional[str] = None
    day_of_week: Optional[str] = None


@dataclass
class MatchDetail:
    base: MatchBase
    players: List[Player]

    def to_db_dict(self) -> List[Dict[str, Any]]:
        common_data = {
            "matchId": self.base.match_id,
            "map": self.base.map_name,
            "mapEn": self.base.map_en,
            "startTime": self.base.start_time,
            "endTime": self.base.end_time,
            "duration": self.base.duration,
            "winTeam": self.base.win_team,
            "score1": self.base.score1,
            "score2": self.base.score2,
            "team1PvpId": self.base.team1_pvp_id,
            "team2PvpId": self.base.team2_pvp_id,
            "pvpLadder": self.base.pvp_ladder,
            "mode": self.base.mode,
            "dayOfWeek": self.base.day_of_week,
        }

        result = []
        for raw_data in self.players:
            raw_data_data = {
                "playerId": raw_data.playerId,
                "nickName": raw_data.nickName,
                "team": raw_data.team,
                "kills": raw_data.kills,
                "deaths": raw_data.deaths,
                "assists": raw_data.assists,
                "headShot": raw_data.headShot,
                "headShotCount": raw_data.headShotCount,
                "headShotRatio": raw_data.headShotRatio,
                "rating": raw_data.rating,
                "pwRating": raw_data.pwRating,
                "flash": raw_data.flash,
                "flashTeammate": raw_data.flashTeammate,
                "flashSuccess": raw_data.flashSuccess,
                "mvpValue": raw_data.mvpValue,
                "twoKill": raw_data.twoKill,
                "threeKill": raw_data.threeKill,
                "fourKill": raw_data.fourKill,
                "fiveKill": raw_data.fiveKill,
                "vs1": raw_data.vs1,
                "vs2": raw_data.vs2,
                "vs3": raw_data.vs3,
                "vs4": raw_data.vs4,
                "vs5": raw_data.vs5,
                "dmgArmor": raw_data.dmgArmor,
                "dmgHealth": raw_data.dmgHealth,
                "adpr": raw_data.adpr,
                "fireCount": raw_data.fireCount,
                "hitCount": raw_data.hitCount,
                "rws": raw_data.rws,
                "pvpTeam": raw_data.pvpTeam,
                "ranks": raw_data.ranks,
                "we": raw_data.we,
                "throwsCnt": raw_data.throwsCnt,
                "teamId": raw_data.teamId,
                "snipeNum": raw_data.snipeNum,
                "entryKill": raw_data.entryKill,
                "firstDeath": raw_data.firstDeath,
                "mvp": raw_data.mvp,
                "kast": raw_data.kast,
                "handGunKill": raw_data.handGunKill,
                "awpKill": raw_data.awpKill,
                "entryDeath": raw_data.entryDeath,
                "botKill": raw_data.botKill,
                "negKill": raw_data.negKill,
                "damage": raw_data.damage,
                "multiKills": raw_data.multiKills,
                "itemThrow": raw_data.itemThrow,
                "score": raw_data.score,
                "endGame": raw_data.endGame,
                "oldRank": raw_data.oldRank,
                "pvpScore": raw_data.pvpScore,
                "pvpScoreChange": raw_data.pvpScoreChange,
                "matchScore": raw_data.matchScore,
                "kda": raw_data.kda,
                "win": raw_data.win,
            }
            result.append({**common_data, **raw_data_data})

        return result
from django.db import models


class CsMatchDetail(models.Model):
    # 基本信息
    playerId = models.CharField(max_length=100, verbose_name="玩家ID")
    nickName = models.CharField(max_length=100, verbose_name="昵称")
    matchId = models.CharField(max_length=100, verbose_name="比赛ID")
    startTime = models.DateTimeField(verbose_name="开始时间")
    endTime = models.DateTimeField(verbose_name="结束时间")
    map = models.CharField(max_length=50, verbose_name="地图")
    mapEn = models.CharField(max_length=50, verbose_name="地图英文")
    teamId = models.CharField(max_length=100, verbose_name="队伍ID")
    mode = models.CharField(max_length=50, verbose_name="游戏模式")
    dayOfWeek = models.IntegerField(verbose_name="星期几")

    # 游戏数据
    rating = models.FloatField(verbose_name="评分")
    pwRating = models.FloatField(verbose_name="完美评分")
    kills = models.IntegerField(verbose_name="击杀数")
    deaths = models.IntegerField(verbose_name="死亡数")
    assists = models.IntegerField(verbose_name="助攻数")
    rws = models.FloatField(verbose_name="回合贡献值")
    kast = models.FloatField(verbose_name="KAST")
    adpr = models.FloatField(verbose_name="每回合伤害")
    we = models.FloatField(verbose_name="武器效率")
    kda = models.FloatField(verbose_name="KDA")

    # 爆头数据
    headShot = models.BooleanField(verbose_name="是否爆头")
    headShotCount = models.IntegerField(verbose_name="爆头数")
    headShotRatio = models.FloatField(verbose_name="爆头率")

    # 武器使用数据
    fireCount = models.IntegerField(verbose_name="开火次数")
    hitCount = models.IntegerField(verbose_name="命中次数")
    handGunKill = models.IntegerField(verbose_name="手枪击杀")
    awpKill = models.IntegerField(verbose_name="AWP击杀")
    snipeNum = models.IntegerField(verbose_name="狙击击杀")

    # 游戏表现
    firstDeath = models.BooleanField(verbose_name="首杀")
    entryKill = models.IntegerField(verbose_name="突破击杀")
    entryDeath = models.IntegerField(verbose_name="突破死亡")
    botKill = models.IntegerField(verbose_name="机器人击杀")
    negKill = models.IntegerField(verbose_name="内格夫击杀")

    # 伤害数据
    damage = models.IntegerField(verbose_name="总伤害")
    dmgArmor = models.IntegerField(verbose_name="护甲伤害")
    dmgHealth = models.IntegerField(verbose_name="生命值伤害")

    # 多杀数据
    twoKill = models.IntegerField(verbose_name="双杀")
    threeKill = models.IntegerField(verbose_name="三杀")
    fourKill = models.IntegerField(verbose_name="四杀")
    fiveKill = models.IntegerField(verbose_name="五杀")
    multiKills = models.IntegerField(verbose_name="多杀次数")

    # 道具使用
    itemThrow = models.IntegerField(verbose_name="投掷物使用")
    flash = models.IntegerField(verbose_name="闪光弹")
    flashTeammate = models.IntegerField(verbose_name="闪队友")
    flashSuccess = models.IntegerField(verbose_name="有效闪光")

    # MVP和评分
    mvpValue = models.FloatField(verbose_name="MVP价值")
    score = models.IntegerField(verbose_name="分数")
    endGame = models.BooleanField(verbose_name="是否结束游戏")

    # 对战数据
    vs1 = models.IntegerField(verbose_name="1v1")
    vs2 = models.IntegerField(verbose_name="1v2")
    vs3 = models.IntegerField(verbose_name="1v3")
    vs4 = models.IntegerField(verbose_name="1v4")
    vs5 = models.IntegerField(verbose_name="1v5")

    # 团队和排名
    pvpTeam = models.CharField(max_length=100, verbose_name="PVP团队")
    ranks = models.IntegerField(verbose_name="排名")
    oldRank = models.IntegerField(verbose_name="旧排名")
    pvpScore = models.IntegerField(verbose_name="PVP分数")
    pvpScoreChange = models.IntegerField(verbose_name="PVP分数变化")

    # 比赛结果
    matchScore = models.IntegerField(verbose_name="比赛分数")
    throwsCnt = models.IntegerField(verbose_name="投掷次数")

    # 玩家状态
    greenUser = models.BooleanField(verbose_name="绿色用户")
    mvp = models.BooleanField(verbose_name="MVP")
    team = models.CharField(max_length=100, verbose_name="队伍")
    duration = models.IntegerField(verbose_name="比赛时长")

    # 比赛结果
    winTeam = models.CharField(max_length=100, verbose_name="获胜队伍")
    score1 = models.IntegerField(verbose_name="队伍1分数")
    score2 = models.IntegerField(verbose_name="队伍2分数")
    team1PvpId = models.CharField(max_length=100, verbose_name="队伍1 PVP ID")
    team2PvpId = models.CharField(max_length=100, verbose_name="队伍2 PVP ID")
    pvpLadder = models.CharField(max_length=50, verbose_name="PVP段位")
    win = models.BooleanField(verbose_name="是否获胜")

    class Meta:
        db_table = 'cs_matches_detail'
        verbose_name = 'CSGO比赛详情'
        verbose_name_plural = 'CSGO比赛详情'

    def __str__(self):
        return f"{self.nickName} - {self.matchId}"

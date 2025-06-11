import argparse
from concurrent.futures import ThreadPoolExecutor
from config.config import DBConfig, APIConfig, AppConfig
from common.services import APIService
from utils.repositories import MySQLRepository
from common.match_data_fetcher import MatchDataFetcher
from utils.log_util import logger


def main():
    # 初始化配置
    db_config = DBConfig()
    api_config = APIConfig()
    app_config = AppConfig(db_config, api_config)

    # 初始化服务
    api_service = APIService(app_config)
    db_repo = MySQLRepository(db_config)

    # 命令行解析
    args = parse_args(app_config)

    # 创建数据获取器
    fetcher = MatchDataFetcher(api_service, db_repo, app_config)

    # 并发处理
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for steam_id in args.targets:
            futures.append(executor.submit(process_summoner, fetcher, steam_id))

        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"处理失败: {e}")


def parse_args(config: AppConfig):
    parser = argparse.ArgumentParser(description="CS:GO比赛数据获取器")
    parser.add_argument("-u", "--users", default="all",
                        help="召唤师列表，逗号分隔或'all'")
    parser.add_argument("-t", "--threads", type=int, default=4,
                        help="并发线程数")
    args = parser.parse_args()

    if args.users.lower() == "all":
        args.targets = config.all_summoners_list
    else:
        args.targets = [s.strip() for s in args.users.split(",")]

    if not args.targets:
        logger.error("未指定有效的召唤师ID")
        exit(1)

    return args


def process_summoner(fetcher: MatchDataFetcher, steam_id: str):
    logger.info(f"开始处理 Steam ID: {steam_id}")
    fetcher.process_player(steam_id)
    logger.info(f"完成处理 Steam ID: {steam_id}")


if __name__ == "__main__":
    main()
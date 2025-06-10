import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.log_util import logger
from common.match_data_fetcher import new_fetcher
from config.config import userList, all_summoners_list

def process_summoner(fetcher, steam_id: str):
    try:
        logger.info(f"开始处理 Steam ID: {steam_id}")
        fetcher.process_player(steam_id)
        logger.info(f"完成处理 Steam ID: {steam_id}")
    except Exception as e:
        logger.error(f"处理 {steam_id} 时出错: {e}")

def parse_args():
    parser = argparse.ArgumentParser(
        description="批量拉取并处理 CS:GO 召唤师比赛数据"
    )
    parser.add_argument(
        "-u", "--users",
        help="要处理的召唤师列表，用逗号分隔；或使用'all'代表处理全部",
        default=userList
    )
    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=4,
        help="并发线程数 (默认: 4)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    raw = args.users.split(',')
    if raw[0].strip().lower() == 'all':
        targets = all_summoners_list
    else:
        targets = [s.strip() for s in raw if s.strip()]
    if not targets:
        logger.error("未指定任何要处理的召唤师。")
        sys.exit(1)
    fetcher = new_fetcher()
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_id = {executor.submit(process_summoner, fetcher, sid): sid for sid in targets}
        for future in as_completed(future_to_id):
            sid = future_to_id[future]
            if future.exception():
                logger.error(f"召唤师 {sid} 处理失败: {future.exception()}")
    logger.info("所有召唤师数据处理完成。")

if __name__ == '__main__':
    main()
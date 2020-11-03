import argparse
import os
from datetime import datetime, timedelta, timezone
import logging

from gcloud.storage import upload_blob
from radiko.recorder import record_time_free


def _get_args():
    parser = argparse.ArgumentParser(description='record radiko')
    parser.add_argument('station', type=str, help='radiko station')
    parser.add_argument('program', type=str, help='radiko program name')
    parser.add_argument('start', type=int, help='start time')
    parser.add_argument('end', type=int, help='end time')
    parser.add_argument('timeout',
                        type=float,
                        default=None,
                        nargs='?',
                        help='limit time of recording.(unit:miniutes)')
    parser.add_argument('-u',
                        '--uploadgcloud',
                        type=bool,
                        help='upload recorded file to gcloud storage')
    args = parser.parse_args()
    return args.station, args.program, args.start, args.end, args.timeout, args.uploadgcloud


if __name__ == "__main__":
    # ログ設定をする
    logging.basicConfig(filename=os.getenv('RADIKO_RECORDER_LOG_FILE',
                                           f'/var/log/record_radiko.log'),
                        level=logging.DEBUG)
    # 実行時パラメータを取得する
    station, program, start, end, timeout, uploads = _get_args()

    JST = timezone(timedelta(hours=+9), 'JST')
    current_time = datetime.now(tz=JST).strftime("%Y%m%d_%H%M")
    logging.debug(f'current time: {current_time}, '
                  f'station: {station}, '
                  f'program name: {program}, '
                  f'start: {start}, '
                  f'end: {end}, '
                  f'uploads: {uploads}')
    # 録音保存先を用意する
    outfilename = f'./tmp/{current_time}_{station}_{program}.aac'
    logging.debug(f'outfilename:{outfilename}')
    # 録音してアップロード
    record_time_free(station, outfilename, start, end, timeout)
    if uploads:
        upload_blob('radiko-recorder', outfilename,
                    f'{current_time}_{station}_{program}.aac')

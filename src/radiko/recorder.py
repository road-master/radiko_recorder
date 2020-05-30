import os
import time

# noinspection PyPackageRequirements
import ffmpeg

from radikoplaylist import MasterPlaylistClient, LiveMasterPlaylistRequest, TimeFreeMasterPlaylistRequest

ENVIRONMENT_VALIABLE_KEY_AREA_ID = "RADIKO_AREA_ID"
AREA_ID_DEFAULT = "JP13"


def record(station, rtime, outfilename):
    # 録音を実施する
    master_playlist_request = LiveMasterPlaylistRequest(station)
    master_playlist = MasterPlaylistClient.get(master_playlist_request,
                                               area_id=get_area_id())

    stream = ffmpeg.input(master_playlist.media_playlist_url,
                          headers=master_playlist.headers,
                          copytb='1')
    stream = ffmpeg.output(stream, outfilename, f='mp4', c='copy')
    record_stream(stream, rtime)


def record_time_free(station, outfilename, start_at, end_at, timeout=None):
    # 録音を実施する
    master_playlist_request = TimeFreeMasterPlaylistRequest(
        station, start_at, end_at)
    master_playlist = MasterPlaylistClient.get(master_playlist_request,
                                               area_id=get_area_id())

    stream = ffmpeg.input(master_playlist.media_playlist_url,
                          headers=master_playlist.headers,
                          copytb='1')
    stream = ffmpeg.output(stream, outfilename, f='mp4', c='copy')
    if timeout is None:
        ffmpeg.run(stream)
    else:
        record_stream(stream, timeout)


def get_area_id():
    return os.getenv(ENVIRONMENT_VALIABLE_KEY_AREA_ID, AREA_ID_DEFAULT)


def record_stream(stream, rtime):
    # Launch video recording
    popen = ffmpeg.run_async(stream, pipe_stdin=True)
    time.sleep(rtime * 60)
    # Stop video recording
    popen.communicate(str.encode("q"))  # Equivalent to send a Q
    # To be sure that the process ends I wait 3 seconds and then terminate de process (wich is more like kill -9)
    time.sleep(3)
    popen.terminate()

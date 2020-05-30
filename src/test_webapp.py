import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from callee import Regex
from radikoplaylist.master_playlist import MasterPlaylist

import webapp


@pytest.fixture
def api():
    return webapp.api


class TestWebApp:
    @staticmethod
    def test(mocker, api, caplog):
        # Patches by mocker since webapp.api from Responder will break when use request_mock.
        #
        # > raise exceptions.NoMockAddress(request)
        # E requests_mock.exceptions.NoMockAddress:
        #   No mock address:
        #     GET http://;/record?station=TBS&program=hoge&rtime=1
        #
        # And, patches in method body since side_effect will be recognize as generator when patch by annotation.
        #
        # File "/app/radiko/recorder.py", line 56, in _get_media_playlist_url
        #   if r.status_code != 200:
        # AttributeError: 'generator' object has no attribute 'status_code'
        mock_ffmpeg_run = mocker.patch('ffmpeg.run_async')
        mock_popen = MagicMock()
        mock_popen.communicate = MagicMock()
        mock_popen.terminate = MagicMock()
        mock_ffmpeg_run.side_effect = AacFileCreator(mock_popen).create
        mocker.patch(
            'radikoplaylist.MasterPlaylistClient.get',
            return_value=MasterPlaylist(
                "https://rpaa.smartstream.ne.jp/medialist?session=Q3fHC9Smzp8x49j9AqicBL",
                {
                    'User-Agent': 'python3.7',
                    'Accept': '*/*',
                    'X-Radiko-App': 'pc_html5',
                    'X-Radiko-App-Version': '0.0.1',
                    'X-Radiko-User': 'dummy_user',
                    'X-Radiko-Device': 'pc',
                    'X-Radiko-AuthToken': 'bPtaETzKFkrriQ_YOKkBSw',
                    'X-Radiko-Partialkey': b'ZDY2YzMyMjA5ZGE5Y2EwYQ==',
                    'X-Radiko-AreaId': "JP13",
                    'Connection': 'keep-alive',
                },
            )
        )
        mock_upload = mocker.patch('gcloud.storage.upload_blob')
        response = api.requests.get("/record",
                                    params={
                                        "station": "TBS",
                                        "program": "hoge",
                                        "rtime": "0.25",
                                    })
        assert response.text == "{\"success\": true}"
        time.sleep(20)
        assert 'WARNING' not in caplog.text
        mock_popen.communicate.assert_called_once_with(str.encode("q"))
        mock_popen.terminate.assert_called_once_with()
        mock_upload.assert_called_once_with(
            'radiko-recorder',
            Regex(r'\./tmp/\d{8}_\d{4}_TBS_hoge.aac'),
            Regex(r'\d{8}_\d{4}_TBS_hoge.aac'),
        )


class AacFileCreator:
    def __init__(self, mock_popen):
        self.mock_popen = mock_popen

    # noinspection PyUnusedLocal
    def create(self, _stream, pipe_stdin):
        Path('./tmp/20200518_0106_TBS_hoge.aac').write_bytes(b'')
        return self.mock_popen

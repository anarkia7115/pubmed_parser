import gzip
from gzip import GzipFile

import logging
logging.basicConfig(level=logging.INFO)


class GzReader(object):

    @staticmethod
    def read(gz_file_path):
        """
        read gz file line by line
        :param gz_file_path:
        :return:
        """
        with gzip.open(gz_file_path, 'rt') as f:
            for content in f:
                yield content

    @staticmethod
    def read_stream(data):
        return gzip.decompress(data)

    @staticmethod
    def read_obs_stream(obs_key, ak, sk):
        from stream_reader.obs_reader import ObsReader
        obs_reader = ObsReader(ak, sk)
        data = obs_reader.read_obj(obs_key)
        with GzipFile(fileobj=data) as obs_stream:
            return obs_stream

    @staticmethod
    def read_obs_line(obs_key, ak, sk):

        logging.info("start download {} from obs".format(obs_key))
        from stream_reader.obs_reader import ObsReader
        obs_reader = ObsReader(ak, sk)
        data = obs_reader.read_obj(obs_key)
        with GzipFile(fileobj=data) as f:
            for content in f:
                yield content



class AbrBase:

    def __init__(self, config):
        pass

    def get_quality_delay(self, segment_index):
        raise NotImplementedError

    def get_first_quality(self):
        return 0

    def report_delay(self, delay):
        pass

    def report_download(self, metrics, is_replacment):
        pass

    def report_seek(self, where):
        pass

    def check_abandon(self, progress, buffer_level):
        return None

    def quality_from_throughput(self, tput):
        global manifest
        global throughput
        global latency

        p = manifest.segment_time

        quality = 0
        while (quality + 1 < len(manifest.bitrates) and
               latency + p * manifest.bitrates[quality + 1] / tput <= p):
            quality += 1
        return quality


a = 0
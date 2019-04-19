from .AbrInterface import AbrBase
import json


class ThroughputRule(AbrBase):
    safety_factor = 0.9
    low_buffer_safety_factor = 0.5
    low_buffer_safety_factor_init = 0.9
    abandon_multiplier = 1.8
    abandon_grace_time = 500

    def __init__(self, config):
        self.bitrate_count = config['bitrate_count']
        self.bitrate_list = config['bitrate_list']

    def get_quality_delay(self, segment_index):
        global manifest

        quality = self.quality_from_throughput(throughput * ThroughputRule.safety_factor)

        if not self.no_ibr:
            # insufficient buffer rule
            safe_size = self.ibr_safety * (get_buffer_level() - latency) * throughput
            self.ibr_safety *= ThroughputRule.low_buffer_safety_factor_init
            self.ibr_safety = max(self.ibr_safety, ThroughputRule.low_buffer_safety_factor)
            for q in range(quality):
                if manifest.bitrates[q + 1] * manifest.segment_time > safe_size:
                    quality = q
                    break

        return (quality, 0)

    def check_abandon(self, progress, buffer_level):
        global manifest

        quality = None # no abandon

        dl_time = progress.time - progress.time_to_first_bit
        if progress.time >= ThroughputRule.abandon_grace_time and dl_time > 0:
            tput = progress.downloaded / dl_time
            size_left = progress.size - progress.downloaded
            estimate_time_left = size_left / tput
            if (progress.time + estimate_time_left >
                ThroughputRule.abandon_multiplier * manifest.segment_time):
                quality = self.quality_from_throughput(tput * ThroughputRule.safety_factor)
                estimate_size = (progress.size *
                                 manifest.bitrates[quality] / manifest.bitrates[progress.quality])
                if quality >= progress.quality or estimate_size >= size_left:
                    quality = None

        return quality

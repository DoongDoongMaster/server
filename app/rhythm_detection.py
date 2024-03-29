import math
from typing import List


BIOS = 64


class RhythmDetection:
    """
    onset을 기반으로 마디 별 박자를 계산하는 클래스
    """

    @staticmethod
    def _calculate_onset_per_bar(
        onset_full_audio: List[float], sec_of_bar: float, bar_num: int
    ) -> List[List[float]]:
        """
        마디 단위별로 온셋 포인트 구하는 함수
        @param onset_full_audio: 전체 wav에 대한 onset time
        @param sec_of_bar: 한 마디가 몇 초인지
        @param bar_num: 마디 총 개수

        return 마디 단위별로의 온셋 time (마디의 처음 시작을 0, 끝을 1로 했을 때 기준으로)
        """
        onset_per_bar = []  # 마디 개수만큼 row 초기화

        # 전체 wav에 대한 onset
        for onset in onset_full_audio:
            idx = math.floor(onset / sec_of_bar)  # 몇 번째 마디인지
            pos_on_bar = (onset - sec_of_bar * idx) / sec_of_bar
            pos_on_bar = int(pos_on_bar * BIOS)
            pos_on_bar = float(pos_on_bar) / float(BIOS)
            onset_point_in_bar = (
                idx + pos_on_bar
            )  # idx 마디에서 몇 박자 뒤에 등장하는지. (0 ~ 1) 마디 누적
            onset_per_bar.append(onset_point_in_bar)

        return onset_per_bar

    @staticmethod
    def _rhythm_detection(
        bpm: int, audio_total_sec: float, onset_full_audio: List[float]
    ) -> List[List[float]]:
        """
        전체 wav와 bpm이 주어졌을 때, rhythm을 계산하는 함수
        @param audio_wav: wav array
        @param bpm: 분당 음표 개수 (4/4박자 기준)
        """
        rhythm_per_bar = 4.0  # 한 마디에 4분음표가 몇 개 들어가는지
        rhythm_per_sec = float(bpm) / 60.0  # 한 초당 몇 박 나오는지
        sec_of_bar = (1.0 / rhythm_per_sec) * rhythm_per_bar  # 한 마디가 몇 초인지
        bar_num = math.ceil(audio_total_sec / sec_of_bar)  # 총 마디 개수
        print(f"-- ! 한 마디당 초: {sec_of_bar}, 마디 개수: {bar_num} ! --")

        onset_per_bar = RhythmDetection._calculate_onset_per_bar(
            onset_full_audio, sec_of_bar, bar_num
        )  # 한 마디당 rhythm 정보

        return onset_per_bar

    @staticmethod
    def get_rhythm(
        bpm: int,
        audio_total_sec: float,
        onsets_arr: List[float],
    ) -> List[List[float]]:
        """
        전체 wav와 bpm이 주어졌을 때, 마디 별 음표의 박자를 계산하는 함수
        @param audio_wav: wav array
        @param bpm: 분당 음표 개수 (4/4박자 기준)
        """
        if onsets_arr is None:
            print("-- ! There is not exist onsets ! --")
            return

        return RhythmDetection._rhythm_detection(bpm, audio_total_sec, onsets_arr)

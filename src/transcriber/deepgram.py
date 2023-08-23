"""
Transcribers perform voice to text transcription

This file contains the configuration for the Deepgram transcriber
"""
from vocode.streaming.transcriber.base_transcriber import BaseTranscriber
from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
from vocode.streaming.input_device.base_input_device import BaseInputDevice
from vocode.streaming.models.transcriber import (
    TranscriberConfig,
    DeepgramTranscriberConfig,
    PunctuationEndpointingConfig,
)


def cnf_for_device(input_device: BaseInputDevice) -> TranscriberConfig:
    return DeepgramTranscriberConfig.from_input_device(
        input_device,
        endpointing_config=PunctuationEndpointingConfig(),
    )


def cnf_for_telephone() -> TranscriberConfig:
    return DeepgramTranscriberConfig.from_telephone_input_device(
        endpointing_config=PunctuationEndpointingConfig(),
    )


def transcriber(cnf: TranscriberConfig) -> BaseTranscriber:
    return DeepgramTranscriber(
        transcriber_config=cnf,
    )

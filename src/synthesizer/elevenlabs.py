"""
Synthesizers perform text to voice transcription

This file contains the configuration for the Eleven Labs synthesizer
"""
from vocode.streaming.synthesizer.base_synthesizer import BaseSynthesizer
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizer
from vocode.streaming.output_device.base_output_device import BaseOutputDevice
from vocode.streaming.models.synthesizer import (
    SynthesizerConfig,
    ElevenLabsSynthesizerConfig,
)


class Voices:
    # Could read directly from https://api.elevenlabs.io/v1/voices
    fin = "D38z5RcWu1voky8WS1ja"


def cnf_for_device(output_device: BaseOutputDevice) -> SynthesizerConfig:
    return ElevenLabsSynthesizerConfig.from_output_device(
        output_device,
        voice_id=Voices.fin,
    )


def cnf_for_telephone() -> SynthesizerConfig:
    return ElevenLabsSynthesizerConfig.from_telephone_output_device(
        voice_id=Voices.fin,
    )


def synthesizer(cnf: SynthesizerConfig) -> BaseSynthesizer:
    return ElevenLabsSynthesizer(
        synthesizer_config=cnf,
    )

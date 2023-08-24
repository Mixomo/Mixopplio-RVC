from pedalboard import Pedalboard, Compressor, Reverb, NoiseGate
from pedalboard.io import AudioFile
import sys
import os
now_dir = os.getcwd()
sys.path.append(now_dir)
import i18n
from pydub import AudioSegment
import numpy as np
import soundfile as sf
from pydub.playback import play

def process_audio(input_path, output_path, reverb_enabled, compressor_enabled, noise_gate_enabled, ):
    print(reverb_enabled)
    print(compressor_enabled)
    print(noise_gate_enabled)
    effects = []
    if reverb_enabled:
        effects.append(Reverb(room_size=0.01))
    if compressor_enabled:
        effects.append(Compressor(threshold_db=-10, ratio=25))
    if noise_gate_enabled:
        effects.append(NoiseGate(threshold_db=-16, ratio=1.5, release_ms=250))

    board = Pedalboard(effects)

    with AudioFile(input_path) as f:
        with AudioFile(output_path, 'w', f.samplerate, f.num_channels) as o:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                effected = board(chunk, f.samplerate, reset=False)
                o.write(effected)


    print(i18n("Processed audio saved at: "), output_path)
    return output_path
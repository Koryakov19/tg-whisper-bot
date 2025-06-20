from pydub import AudioSegment

def convert_ogg_to_wav(ogg_path: str) -> str:
    wav_path = ogg_path.replace(".ogg", ".wav")
    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format="wav")
    return wav_path

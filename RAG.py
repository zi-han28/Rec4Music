from llama_cpp import Llama

llm = Llama(model_path="Llama-3.2-1B-Instruct-Q6_K.gguf", n_ctx=2048, verbose=False)

def humanize_taste_profile(profile: dict) -> dict:
    """Convert normalized (0-1) taste-profile values back to real-world units."""

    return {
        'danceability': round(profile['danceability'], 2),
        'energy': round(profile['energy'], 2),
        'valence': round(profile['valence'], 2),
        'tempo_bpm': round(profile['tempo'] * 250, 1),
        'loudness_db': round(profile['loudness'] * 60 - 60, 1),
        'acousticness': round(profile['acousticness'], 2),
        'instrumentalness': round(profile['instrumentalness'], 3),
        'liveness': round(profile['liveness'], 2),
        'speechiness': round(profile['speechiness'], 2),
        'key': max(0, min(11, round(profile['key']*11))),
        'mode': 'major' if profile['mode'] == 1 else 'minor',
    }


SYSTEM_PROMPT = (
    "You are a music analyst. You'll be given the taste profile of the user's favourited songs Write 3-4 warm, natural sentences. \n"
    "summarising their overall taste — you're describing a listener's preferences, not a single song. \n\n"
    "The taste_profile is the sum average of all the favourite songs' audio features.\n"
    "generate the text in first person, like you are talking to a human being.\n"
    "Context:\n"
    "- danceability (0-1):Danceability is a measure of how suitable a song is for dancing, ranging from 0 to 1. A score of 0 means the song is not danceable at all, while a score of 1 indicates it is highly danceable. This score takes into account factors like tempo, rhythm, beat consistency, and energy, with higher scores indicating stronger, more rhythmically engaging tracks.\n"
    "- energy (0-1): Energy in music refers to the intensity and liveliness of a track, with a range from 0 to 1. A score of 0 indicates a very calm, relaxed, or low-energy song, while a score of 1 represents a high-energy, intense track. It’s influenced by elements like tempo, loudness, and the overall drive or excitement in the music.\n"
    "- valence (0-1): Valence in music measures the emotional tone or mood of a track, with a range from 0 to 1. A score of 0 indicates a song with a more negative, sad, or dark feeling, while a score of 1 represents a more positive, happy, or uplifting mood. Tracks with a high valence tend to feel joyful or energetic, while those with a low valence may evoke feelings of melancholy or sadness.\n"
    "- tempo_bpm: Estimated tempo in beats per minute (BPM). Typically ranges between 0 and 250.\n"
    "- loudness_db: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.\n"
    "- acousticness (0-1): Acousticness refers to how much of a song or piece of music is made up of natural, organic sounds rather than synthetic or electronic elements. In other words, it's a measure of how 'acoustic' a piece of music sounds. A confidence measure from 0.0 to 1.0, greater value represents higher confidence the track is acoustic.\n"
    "- instrumentalness (0-1): Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.\n"
    "- liveness (0-1): Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.\n"
    "- speechiness (0-1): Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.\n"
    "- mode: Mode indicates the modality (major or minor) of a track. Major is represented by 1 and minor is 0. \n"
    "- key: The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1. \n\n"
    "Never list the raw numbers back — translate them into natural, descriptive language."
)

# Two anchor examples spanning contrasting listener profiles, to teach tone and structure.
ANCHOR_EXAMPLES = [
    {
        "role": "user",
        "content": "danceability: 0.4, energy: 0.35, valence: 0.55, tempo_bpm: 88, "
                    "loudness_db: -13.0, acousticness: 0.7, instrumentalness: 0.04, "
                    "liveness: 0.1, speechiness: 0.04, key: D, mode: major"
    },
    {
        "role": "assistant",
        "content": "Your taste favours warm, unhurried music — soft tempos, natural "
                    "instrumentation, and a gentle emotional lift rather than a loud one. "
                    "It's the kind of taste that leans toward feeling over spectacle: "
                    "mellow, intimate, and quietly uplifting. There's a comfort in songs "
                    "that don't need to shout to be felt."
    },
    {
        "role": "user",
        "content": "danceability: 0.55, energy: 0.9, valence: 0.3, tempo_bpm: 152, "
                    "loudness_db: -3.5, acousticness: 0.05, instrumentalness: 0.18, "
                    "liveness: 0.3, speechiness: 0.07, key: E, mode: minor"
    },
    {
        "role": "assistant",
        "content": "You have a taste built for intensity — driving tempos, dense "
                    "production, and a minor-key edge that trades warmth for tension "
                    "and drive. It suggests that you prefer complexity and impact "
                    "over comfort, the kind of music that rewards close attention and "
                    "hits hardest at full volume."
    },
]

def describe_track(taste_profile: dict) -> str:
    deNormalise = humanize_taste_profile(taste_profile)
    profile_str = ", ".join(f"{k}: {v}" for k, v in deNormalise.items())

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        # One few-shot example to anchor style and length
        # The real request
        {"role": "user", "content": profile_str},
    ]

    output = llm.create_chat_completion(messages=messages, max_tokens=200, temperature=0.7)
    return output["choices"][0]["message"]["content"]

if __name__ == "__main__":
    audio_features = {
        'danceability': 0.6915, 'energy': 0.6955, 'valence': 0.64725, 'tempo': 0.553146, 'loudness': 0.9279666666666666, 'acousticness': 0.2318225, 'instrumentalness': 0.00027635, 'liveness': 0.1827, 'speechiness': 0.06737499999999999, 'key': 0.3958333333333333, 'mode': 1
    }
    print(describe_track(taste_profile=audio_features))

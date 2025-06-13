from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatRequest(_message.Message):
    __slots__ = ("user_id", "message", "session_id", "agent_id", "context", "tts_settings")
    class ContextEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    TTS_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    message: str
    session_id: str
    agent_id: str
    context: _containers.ScalarMap[str, str]
    tts_settings: TTSSettings
    def __init__(self, user_id: _Optional[str] = ..., message: _Optional[str] = ..., session_id: _Optional[str] = ..., agent_id: _Optional[str] = ..., context: _Optional[_Mapping[str, str]] = ..., tts_settings: _Optional[_Union[TTSSettings, _Mapping]] = ...) -> None: ...

class TTSSettings(_message.Message):
    __slots__ = ("enable_tts", "voice_id", "voice_settings")
    ENABLE_TTS_FIELD_NUMBER: _ClassVar[int]
    VOICE_ID_FIELD_NUMBER: _ClassVar[int]
    VOICE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    enable_tts: bool
    voice_id: str
    voice_settings: VoiceSettings
    def __init__(self, enable_tts: bool = ..., voice_id: _Optional[str] = ..., voice_settings: _Optional[_Union[VoiceSettings, _Mapping]] = ...) -> None: ...

class VoiceSettings(_message.Message):
    __slots__ = ("stability", "similarity_boost", "style", "use_speaker_boost", "speed")
    STABILITY_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_BOOST_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    USE_SPEAKER_BOOST_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    stability: float
    similarity_boost: float
    style: float
    use_speaker_boost: bool
    speed: float
    def __init__(self, stability: _Optional[float] = ..., similarity_boost: _Optional[float] = ..., style: _Optional[float] = ..., use_speaker_boost: bool = ..., speed: _Optional[float] = ...) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ("response", "session_id", "user_id", "type", "metadata", "audio_content")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    AUDIO_CONTENT_FIELD_NUMBER: _ClassVar[int]
    response: str
    session_id: str
    user_id: str
    type: str
    metadata: MetadataMessage
    audio_content: bytes
    def __init__(self, response: _Optional[str] = ..., session_id: _Optional[str] = ..., user_id: _Optional[str] = ..., type: _Optional[str] = ..., metadata: _Optional[_Union[MetadataMessage, _Mapping]] = ..., audio_content: _Optional[bytes] = ...) -> None: ...

class MetadataMessage(_message.Message):
    __slots__ = ("intent", "turn_count", "additional_data")
    class AdditionalDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    INTENT_FIELD_NUMBER: _ClassVar[int]
    TURN_COUNT_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_DATA_FIELD_NUMBER: _ClassVar[int]
    intent: str
    turn_count: int
    additional_data: _containers.ScalarMap[str, str]
    def __init__(self, intent: _Optional[str] = ..., turn_count: _Optional[int] = ..., additional_data: _Optional[_Mapping[str, str]] = ...) -> None: ...

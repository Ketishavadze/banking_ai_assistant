# Voice Evaluation

## Objective

The voice pipeline was evaluated manually to test whether spoken banking
requests could successfully travel through the complete system:

Microphone → Speech-to-Text → LangGraph → MCP → Response → Text-to-Speech

The goal was not only to evaluate transcription quality, but also to determine
whether transcription errors affected downstream intent routing and task
completion.


## Test Setup

- Microphone input through `sounddevice`
- 5-second WAV recordings
- 16 kHz mono audio
- OpenAI speech-to-text
- LangGraph intent routing
- MCP banking tools
- OpenAI text-to-speech
- Audio playback through `pygame`

Tests included:

- clearly spoken queries
- naturally phrased queries
- improvised wording
- noisier speech
- longer conversational phrasing


### Example Voice Run

Spoken query:

> Someone took my card and now I can't find it.

STT transcription:

> Someone took my card and now I can't find it.

Result:

- Route: `stolen_card`
- MCP tool: `get_card_procedure`
- Task result: Successful
- Safety behavior: The assistant explicitly stated that it had not frozen,
  blocked, or cancelled the card.

Latency:

| Stage | Time |
|---|---:|
| Recording | 5.17 s |
| STT | 1.14 s |
| Agent | 3.73 s |
| TTS | 5.37 s |
| System latency | 10.24 s |
| Total including recording | 15.41 s |

In this run, TTS was the largest contributor to response latency.

## Observations

The speech-to-text component generally produced usable transcriptions for
banking queries.

Some transcription errors occurred during noisier or more naturally phrased
speech.

For example:

**Intended speech:**

> I was wondering what is the status of my card?

**STT transcription:**

> I was wondering what is the status of my car?

Despite the word `card` being transcribed as `car`, the LangGraph router still
correctly inferred that the user was asking about card status.

The system therefore followed the correct path:

```text
Speech
↓
STT transcription containing a minor error
↓
card_status intent
↓
get_card_status MCP tool
↓
correct customer card information
↓
assistant response
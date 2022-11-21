# speech-translation

### What?
Flask based platform to record, transcribe and translate audio file with concurrency.
The final goal would consist of having a working html platform on which you can see real-time captions of a conversation, of a speech... in a foreign language.
(think of it as real-life captions and auto-translation).

### Why?
This idea originated from international students that, sometimes, need to communicate with people that don't know how to speak English, making the interactions far from desirable.

### How?
The platform is based on Flask (python), the speech-to-text translation is done using OpenAi's Whisper model; the model is also used to detect the language and translating the content.
The real-time captions are obtained through multiprocessing, a technique that allows the script to run on multiple processors allowing more operations to happen at the same time (concurrency).



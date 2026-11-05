# My-Jarvis

পাইথনে তৈরি একটি সহজ ভয়েস-অ্যাসিস্ট্যান্ট। "Jarvis" বলে ডাকলে সে আপনার কমান্ড শোনে ও উত্তর দেয়।

## কী কী করতে পারে

| বলুন | ফল |
|---|---|
| "Jarvis, what time is it" | এখনকার সময় বলবে |
| "Jarvis, what's the date" | আজকের তারিখ বলবে |
| "Jarvis, open youtube" | ব্রাউজারে সাইট খুলবে (youtube, google, github, gmail, facebook, whatsapp, wikipedia) |
| "Jarvis, search for python tutorials" | গুগলে সার্চ করবে |
| "Jarvis, who is Rabindranath Tagore" | উইকিপিডিয়া থেকে সংক্ষিপ্ত তথ্য বলবে |
| "Jarvis, tell me a joke" | একটি জোক বলবে |
| "Jarvis, goodbye" | বন্ধ হবে |

## ইনস্টল

Python 3.9 বা নতুন লাগবে।

```bash
git clone https://github.com/salam161632-ai/My-Jarvis.git
cd My-Jarvis
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

PyAudio ইনস্টল না হলে:

- Windows: `pip install pipwin` তারপর `pipwin install pyaudio`
- macOS: `brew install portaudio` তারপর `pip install pyaudio`
- Ubuntu/Debian: `sudo apt install portaudio19-dev python3-pyaudio espeak`

## চালানো

```bash
python main.py                 # মাইক্রোফোন দিয়ে
python main.py --lang bn-BD    # বাংলা স্পিচ রিকগনিশন
python main.py --text          # মাইক ছাড়া, টাইপ করে
python main.py --wake-word computer   # অন্য ওয়েক ওয়ার্ড
```

স্পিচ রিকগনিশনের জন্য ইন্টারনেট লাগে (Google Web Speech API)।

## নিজের কমান্ড যোগ করা

`jarvis/commands.py` ফাইলের `handle()` ফাংশনে নতুন শর্ত যোগ করুন। নতুন সাইট যোগ করতে একই ফাইলের `SITES` ডিকশনারিতে একটি লাইন যোগ করুন।

## প্রজেক্টের গঠন

```
My-Jarvis/
├── main.py              # এন্ট্রি পয়েন্ট ও মেইন লুপ
├── requirements.txt
└── jarvis/
    ├── commands.py      # কমান্ড বোঝা ও উত্তর তৈরি
    └── voice.py         # শোনা (মাইক) ও বলা (TTS)
```

## সীমাবদ্ধতা

- বাংলা কথা চেনা যায় (`--lang bn-BD`), কিন্তু বাংলায় উত্তর শোনাতে আপনার কম্পিউটারে বাংলা TTS ভয়েস ইনস্টল থাকতে হবে। না থাকলে উত্তর টেক্সটে দেখা যাবে।
- বাংলায় ওয়েক ওয়ার্ড চিনতে সমস্যা হলে `--wake-word` দিয়ে লিপ্যন্তরিত শব্দ (যেমন `জার্ভিস`) দিন।

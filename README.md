# Call Center POC

This application was made to accomplish the following requirements

- Receive a caller
- Collect the following
    - (Demographics) Patient's name, DOB, contact information, and address
    - (Insurance Coverage) Payer name and ID
    - (opt) Referral (yes/no and to whom)
    - Chief medical complaint / the reason they are coming in
- Respond with fake providers and availabilities
- Text the caller their selected appointment date, time, and which doctor they'll see


# Telephony

This project was build off of the Vocode Telephony tutorial.

* [docs](https://docs.vocode.dev/open-source/telephony)
* [github](https://github.com/vocodedev/vocode-python/tree/main/apps/telephony_app)


[See also the python quickstart](https://docs.vocode.dev/open-source/python-quickstart)
  
## Run the self-hosted application

### Prerequisites

* Twilio number, SID, and key 
* Deepgram API key
* Elevenlabs API key
* OpenAI API key
* Docker
* (opt) Poetry

### Docker

Install docker and run

`make up`

If you want the CLI of the same docker env for easy scripting / testing, while the application is running, use

`make enter`

### Poetry

Install poetry to help add requirements to the project OR use poetry inside the docker.

`pip install --upgrade poetry`

### Twilio

So far I haven't looked into getting a stable ngrok address. 

If you don't have one you'll need to copy the tunnel URL into Twilio every time you spin the application up as it changes.

Save your current Ngrok address to the Twilio phone number.

### Test it

Call the Twilio number on your phone once your Twilio setting is updated.

You can alternatively try out the testing scripts in `script` like `script/call.py` or `script/conv.py`

Use python or use poetry like so `poetry run python /script/conv.py`

# TODOs

- Agent texting - eventmanager or action?
- Fix call-out script?

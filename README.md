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

Install docker.

`docker-compose up --build`

### Poetry

Install poetry OR use poetry inside the docker.

`docker exec -it vocode-telephony-app /bin/bash`

or

TODO - this may require more venv setup, not sure if poetry uses the docker magically. It seems to? how is it getting the docker compose env var otherwise...

`pip install --upgrade poetry`

### Twilio

So far I haven't looked into getting as table ngrok address. If you don't have one you'll need to copy the tunnel URL into Twilio every time you spin the application up as it changes.


### Start it

`make up`

### Test it

Call the Twilio number

also try out the testing scripts in `script` like `script/call.py` or `script/conv.py`

If you want to have docker handle the env for the scripts, use `make enter`

Use python or use poetry like however this works `poetry run python /script/conv.py`

# TODOs

- Agent texting - eventmanager or action?
- Fix call-out script?

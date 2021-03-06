#!/usr/bin/env python

import settings.emulationstationSettings as esSettings
import settings.recalboxSettings as recalSettings
import settings.libretroSettings as libretroSettings


def loadEnvConfig(system):
        smooth = esSettings.load("Smooth")
        shaders = esSettings.load("Shaders")
        ratio = esSettings.load("GameRatio")
        video_mode = recalSettings.load(system + "_video_mode")
        custom_emulator = recalSettings.load(system + "_emulator")
        if shaders == "true":
            smooth = False
        return {
            'smooth': smooth,
            'shaders': shaders,
            'ratio': ratio,
            'video_mode': video_mode,
            'custom_emulator': custom_emulator
        }

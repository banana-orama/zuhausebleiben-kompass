#!/usr/bin/env python3
"""Kontextfenster: Welcher Absatz enthaelt die 10-Arbeitstage-Kurzzeitpflege-Klausel?"""
import pathlib, re
t = pathlib.Path('research/evidence/krankenhaus-121126/sgb11-18a.html').read_text(encoding='utf-8')
i = t.find('zehnten Arbeitstag')
print(t[max(0, i - 750):i + 60])

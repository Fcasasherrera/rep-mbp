import pretty_midi
import random

midi = pretty_midi.PrettyMIDI()
piano = pretty_midi.Instrument(program=0)

def add_note(pitch, start, duration, velocity=85):
    piano.notes.append(pretty_midi.Note(velocity=velocity, pitch=pitch, start=start, end=start + duration))

def add_chord(notes, start, duration, velocity=50):
    for n in notes:
        add_note(n, start, duration, velocity)

def add_pedal(start, end):
    piano.control_changes.append(pretty_midi.ControlChange(number=64, value=127, time=start))
    piano.control_changes.append(pretty_midi.ControlChange(number=64, value=0, time=end))

bpm = 60
beat = 60.0 / bpm
time = 0.0

# Definir acordes ricos con bajo profundo (octava 1 y 2 para graves y cuerpo)
chords = {
    "Bm": [35, 47, 59, 62, 66, 69],   # B1, B2, B3, D4, F#4, A4
    "A": [33, 45, 57, 61, 64, 66],    # A1, A2, A3, C#4, E4, F#4
    "F#": [30, 42, 54, 58, 63, 66],   # F#1, F#2, F#3, A#3, D4, F#4
    "G": [31, 43, 55, 59, 62, 66],    # G1, G2, G3, B3, D4, F#4
}

# Línea de bajo para la mano izquierda (octava 1)
bass_line = {
    "Bm": [35, 35, 47, 47],   # Repetición para ritmo
    "A": [33, 33, 45, 45],
    "F#": [30, 30, 42, 42],
    "G": [31, 31, 43, 43],
}

# Melodía para mano derecha en rango medio-alto, con fraseos y saltos
melody_map = {
    "Bm": [71, 74, 76, 78, 79, 81],  
    "A": [69, 71, 74, 76, 77, 79],
    "F#": [66, 68, 71, 73, 74, 76],
    "G": [67, 69, 71, 74, 76, 78],
}

# Progresión simple para demo extendida
progression = [
    ("Bm", 6), ("A", 6), ("Bm", 6),
    ("F#", 3), ("Bm", 3), ("A", 3), ("G", 3),
    ("A", 6), ("G", 6),

    ("A", 3), ("F#", 3), ("Bm", 6),
    ("Bm", 6), ("A", 6), ("Bm", 6),
    ("F#", 3), ("Bm", 3), ("A", 3), ("G", 3),
    ("A", 6), ("G", 6),

    ("A", 3), ("Bm", 3), ("A", 3), ("G", 3),
    ("A", 6), ("Bm", 6),
    ("A", 3), ("Bm", 3), ("A", 3), ("G", 3),
    ("A", 3), ("G", 3), ("A", 3), ("Bm", 6),
]

def add_bass_line(chord_name, start, dur_beats):
    notes = bass_line[chord_name]
    note_duration = (dur_beats * beat) / len(notes)
    t = start
    for n in notes:
        add_note(n, t, note_duration * 0.9, velocity=75)
        t += note_duration

def add_melody_notes(notes, start, dur_beats, base_vel=85):
    note_dur = (dur_beats * beat) / len(notes)
    t = start
    for i, pitch in enumerate(notes):
        velocity = max(60, min(110, base_vel + (i * 3)))
        add_note(pitch, t, note_dur * 0.8, velocity)
        t += note_dur * 0.9

add_pedal(0, sum(d * beat for _, d in progression))

for chord_name, dur in progression:
    # Bajo rítmico y sólido
    add_bass_line(chord_name, time, dur)
    # Acordes en registro medio para cuerpo
    add_chord(chords[chord_name][2:], time, dur * beat, velocity=50)
    # Melodía expresiva y variada
    melody_notes = melody_map[chord_name]
    add_melody_notes(melody_notes, time + beat*0.5, dur, base_vel=80)
    time += dur * beat

midi.instruments.append(piano)
midi.write("tema_finalfantasy_profundo.mid")
print("🎼 Archivo 'tema_finalfantasy_profundo.mid' generado con bajos profundos y textura rica.")

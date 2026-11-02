# tracks

Start/finish lines of race tracks and timed routes for the lap timing of
[PitLogger](https://github.com/PitLogger) and the PitLog Viewer. Copy the files of the tracks you
drive into the folder `tracks` on the PitLogger's SD card; it picks the one you are at. Tracks of
your own you can also save on the PitLogger itself.

| | |
|---|---|
| [tracks/](tracks) | one file per track, `<id>.json` |
| [tools/check_tracks.py](tools/check_tracks.py) | checks every file; also writes all tracks into one `tracks.json` |

## Using a track

Load its file (e.g. `tracks/de-some-track.json`) in the PitLogger's web interface: Live → Lap
timing → menu → *Load track files…* (several at once). The PitLogger checks it and keeps it in
the folder `tracks` on its SD card. Copying the file into that folder with a card reader works as
well; the PitLogger reads the folder when the card is inserted. The track appears under "On the SD
card"; with "Automatic" it is used as soon as you are within 3 km of its start. Deleting it there
removes the file from the card.

## Track types

- **circuit** – a closed track. One line is start and finish; every crossing ends a lap.
- **sprint** – a route from a start line to a different finish line, for example
  Nürburgring Nordschleife *Bridge to Gate*, hill climbs or a stage. The time runs from crossing
  the start to crossing the finish; then the next run can start.

## Format

```json
{
  "id": "de-example-sprint",
  "name": "Example hill climb",
  "country": "DE",
  "type": "sprint",
  "start":  { "lat": 50.3318550, "lon": 7.9934328, "course": 66.1 },
  "finish": { "lat": 50.3401200, "lon": 8.0012300, "course": 12.5 },
  "length_m": 2300,
  "source": "measured with a PitLogger, 2026-11"
}
```

| Field | Meaning |
|---|---|
| `id` | lowercase letters, digits and `-`, starting with the country code; the file name without `.json` |
| `name` | as shown to the user (up to 47 characters) |
| `country` | ISO 3166-1 alpha-2 |
| `type` | `circuit` or `sprint` |
| `start` | a point on the track (WGS84, degrees, 7 decimals) and the direction of travel there (`course`, degrees, 0 = north, clockwise). The line runs across that direction, 25 m to each side. For a circuit this is the start/finish line |
| `finish` | sprint only: the finish line, like `start` |
| `length_m` | optional: length of a lap or run, for display |
| `source` | where the lines come from (a measured drive, official data, …) |

A crossing counts when the way between two GPS fixes passes the line in its direction (the rule
of the `.pitlog` format, record LAP). Put the point in the middle of the track and take the course
from GPS data driven there, not from a map: a few metres off are fine, a wrong direction is not.

## Adding a track

1. Drive it with a PitLogger and set the lines there (Live → Lap timing), or open a recording in the
   PitLog Viewer and set the lines on the map.
2. "Export track" in the viewer gives the file. Check name, id and source.
3. `python tools/check_tracks.py`, then a pull request.

## License

The track data is CC0 (public domain); the tools are MIT, see [LICENSE](LICENSE).

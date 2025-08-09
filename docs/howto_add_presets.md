# Presets toevoegen (HOWTO)

Dankjewel voor je bijdrage! Volg deze stappen om een preset (alleen JSON) toe te voegen.

## 1) Bestandslocatie
Plaats je bestand in de map: `presets/` of `presets/community_examples/`

## 2) Bestandsnaam
Gebruik een duidelijke naam, bv. `guitar_sweetened_vintage.json`

## 3) Structuur
```json
{
  "name": "Guitar - Sweetened (Vintage)",
  "instrument": "Guitar",
  "tuning": "Standard (E2 A2 D3 G3 B3 E4)",
  "sweetened": true,
  "A4": 440.0,
  "offsets": { "E2": 1.5, "A2": 0.8, "D3": 0.0, "G3": -0.4, "B3": 1.6, "E4": 1.8 }
}
```

**Uitleg velden**
- `name`: Preset naam die in de app verschijnt
- `instrument`: Moet overeenkomen met een instrument in `instruments/instruments.json`
- `tuning`: Exacte tekst van de gewenste tuning binnen dat instrument
- `sweetened`: `true` als er offsets worden gebruikt
- `A4`: Referentiefrequentie (optioneel, standaard 440.0)
- `offsets`: (optioneel) per snaar/toets in cent, overschrijft instrument-defaults

## 4) Pull Request
1. Fork de repo
2. Voeg jouw `.json` toe in `presets/`
3. Maak een Pull Request met een korte beschrijving
4. Alleen wijzigingen in `presets/` worden standaard overwogen; codewijzigingen vereisen expliciete toestemming

## 5) Tips
- Test je preset lokaal in de app
- Voeg een korte motivatie toe (waarvoor is de preset bedoeld)
- Gebruik *sweetened* spaarzaam: ±0.5–2.0 cent is vaak voldoende

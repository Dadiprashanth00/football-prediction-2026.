# Football Prediction 2026

Statistical football prediction platform for the 2026/27 season.
Desktop website, mobile website and Android app share one codebase (`web/index.html`).

Competitions: Premier League, La Liga, Serie A, Ligue 1, Primeira Liga,
UEFA Champions League, Europa League and Conference League (real 2026/27 participants).

## What's inside

```
web/index.html        Complete app: dashboard, prediction engine, data layer (no build step)
android/              Android Studio project – WebView shell that bundles web/index.html
.github/workflows/    GitHub Actions job that builds the APK in the cloud
```

## Run the website

* Open `web/index.html` in any browser, or
* upload it to any static host (Azure Static Web Apps, GitHub Pages, Netlify, an IIS/Nginx site). One file, no server code.

## Get the APK (no Android Studio needed)

1. Create a new GitHub repository and upload this whole folder (keep the `.github` folder).
2. Open the **Actions** tab → **Build Android APK** → **Run workflow** (it also runs on every push to `main`).
3. After ~4 minutes, download **FootballPrediction2026-apk** from the run's *Artifacts* section and unzip it.
4. Copy `app-debug.apk` to the phone and install it (allow "Install unknown apps" for your file manager).

### Or build locally with Android Studio
Open the `android` folder in Android Studio (Ladybug or newer), let Gradle sync, then
**Build → Build App Bundle(s)/APK(s) → Build APK(s)**. Requires JDK 17.

Whenever you change `web/index.html`, copy it to `android/app/src/main/assets/www/index.html`
(the GitHub workflow does this automatically).

### Signed release build (Play Store)
Set `FP_KEYSTORE`, `FP_KEYSTORE_PASSWORD`, `FP_KEY_ALIAS`, `FP_KEY_PASSWORD` and run
`./gradlew assembleRelease` (or `bundleRelease` for an .aab).

## Data sources

| Mode | Coverage | Notes |
|---|---|---|
| Demo (default) | All 8 | Real 2026/27 line-ups; fixture dates and results are simulated. Works offline. |
| football-data.org | PL, La Liga, Serie A, Ligue 1, Primeira, UCL | Free key at football-data.org. 10 requests/min. |
| API-Football (api-sports.io) | All 8 incl. UEL, UECL | Free plan does **not** include current seasons; a paid plan is needed for 2026/27. |

Set the provider and key from the ⚙ settings button. Keys are stored only on the device (localStorage).
If a provider blocks browser calls (CORS) on the website, add a CORS proxy prefix in settings;
the Android app and a file opened locally usually work without one.

## Prediction engine

1. **Prior strength** – per-club Elo-style ratings (pre-season estimates) give baseline expected goals, with a 60-point home advantage.
2. **Recent form** – last 10 matches, exponentially weighted (0.88 per match back), converted into attack and defence multipliers *relative to what each opponent's strength implied*, shrunk towards 1 when the sample is small.
3. **Home/away split** – home team's home record and away team's away record count 40%.
4. **Momentum** – last-5 vs last-10 points per game, capped at ±5%.
5. **Head-to-head** – lightly weighted (30% on goal rate, ±3% result tilt).
6. **Dixon–Coles Poisson** score grid (0–10 goals each, ρ = −0.07) → every market:
   1X2, double chance, draw no bet, over/under 0.5–3.5, BTTS, correct score, half-time result,
   HT/FT (44% / 56% goal split by half), expected goals and predicted score.
7. **Confidence** – High ≥ 70%, Medium 55–70%, Low < 55%; capped at Medium with under 3 matches of data.
8. **Accuracy tab** – walk-forward backtest: each finished match is re-predicted using only data available before kick-off.

Predictions are probabilities, never guarantees. 18+ only where betting is involved; gamble responsibly.
Club names are used for identification; badges are generic monograms, not official crests.

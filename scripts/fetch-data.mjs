// Downloads real 2026/27 fixtures, results and scores from ESPN's public soccer feed
// for all 12 competitions and writes web/data.json (used by the website and the APK).
import { writeFileSync } from 'node:fs';
const LEAGUES = { PL:'eng.1', PD:'esp.1', SA:'ita.1', FL1:'fra.1', PPL:'por.1', CL:'uefa.champions', EL:'uefa.europa', ECL:'uefa.europa.conf', BL1:'ger.1', DED:'ned.1', SPL:'sco.1', TSL:'tur.1' };
const months = [];
for (let d = new Date(Date.UTC(2026, 6, 1)); d < new Date(Date.UTC(2027, 6, 1)); d.setUTCMonth(d.getUTCMonth() + 1)) months.push(new Date(d));
const pad = n => String(n).padStart(2, '0');
function status(ev) {
  const t = ev.status?.type || {};
  if (t.state === 'in') return { status: 'LIVE', minute: t.name === 'STATUS_HALFTIME' ? 'HT' : (ev.status.displayClock || '').replace(/'/g, '') };
  if (t.state === 'post') return { status: t.completed ? 'FT' : (/CANCEL|ABANDON/.test(t.name) ? 'CANC' : 'PST') };
  if (/POSTPONED/.test(t.name || '')) return { status: 'PST' };
  return { status: 'NS' };
}
function norm(ev, comp) {
  const c = ev.competitions?.[0]; if (!c) return null;
  const h = c.competitors.find(x => x.homeAway === 'home'), a = c.competitors.find(x => x.homeAway === 'away');
  if (!h || !a) return null;
  const s = status(ev), played = s.status === 'FT' || s.status === 'LIVE';
  const ht = x => x.linescores?.[0]?.value;
  return {
    id: 'es' + ev.id, comp, round: ev.week?.number ? 'Matchday ' + ev.week.number : (c.notes?.[0]?.headline || ev.season?.slug || '').replace(/-/g, ' '),
    home: h.team.displayName, away: a.team.displayName, hc: h.team.logo || '', ac: a.team.logo || '',
    utc: ev.date, ...s,
    hg: played ? +h.score : null, ag: played ? +a.score : null,
    hth: s.status === 'FT' && ht(h) != null ? +ht(h) : null, hta: s.status === 'FT' && ht(a) != null ? +ht(a) : null
  };
}
const out = []; const report = {}; const errs = [];
for (const [comp, code] of Object.entries(LEAGUES)) {
  report[comp] = 0;
  for (const m of months) {
    const range = `${m.getUTCFullYear()}${pad(m.getUTCMonth() + 1)}`;
    const url = `https://site.api.espn.com/apis/site/v2/sports/soccer/${code}/scoreboard?dates=${range}&limit=300`;
    try {
      const r = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0 FootballPrediction2026' } }); if (!r.ok) { errs.push(`${comp} ${range} HTTP ${r.status}`); continue; }
      const j = await r.json();
      for (const ev of j.events || []) { const n = norm(ev, comp); if (n) { out.push(n); report[comp]++; } }
    } catch (e) { errs.push(`${comp} ${range} ${e.message} ${e.cause?.code||''}`); }
  }
}
const seen = new Set(); const matches = out.filter(m => !seen.has(m.id) && seen.add(m.id)).sort((a, b) => a.utc < b.utc ? -1 : 1);
console.log(`::notice::matches per competition ${JSON.stringify(report)} total ${matches.length}`);
errs.slice(0, 8).forEach(e => console.log(`::warning::${e}`));
if (matches.length < 200) { console.error('Too few matches fetched, keeping previous data'); process.exit(1); }
writeFileSync('web/data.json', JSON.stringify({ source: 'ESPN', updated: new Date().toISOString(), matches }));

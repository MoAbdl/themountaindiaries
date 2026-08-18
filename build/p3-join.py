import io, re

import os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
_OUT = os.environ.get('MD_OUT') or REPO
SRC = os.path.join(_OUT, 'index.html')
OUT = os.path.join(_OUT, 'join.html')

s = io.open(SRC, encoding='utf-8').read()
style = re.search(r'<style>(.*?)</style>', s, re.S).group(1)

extra_css = """
  /* ─── JOIN PAGE ─── */
  /* body already reserves the fixed nav's strip, so no offset needed here */
  .join-main { padding-top: 0; }
  .join-hero { position: relative; height: min(32vh, 280px); }
  .join-grid {
    display: grid; grid-template-columns: 0.95fr 1.05fr;
    gap: var(--s-7); padding: var(--s-6) 0 var(--s-7);
    align-items: start;
  }
  .join-panel {
    background: var(--card); border: 1px solid var(--rule);
    border-radius: var(--radius-lg); box-shadow: var(--shadow-card);
    padding: var(--s-6);
  }
  .join-points { list-style: none; margin-top: var(--s-5); display: flex; flex-direction: column; gap: var(--s-3); }
  .join-points li { display: flex; gap: var(--s-3); font-size: var(--t-base); color: var(--ink-2); }
  .join-points li::before { content: '\\2726'; color: var(--sienna); }
  .check-row { display: flex; align-items: flex-start; gap: var(--s-3); margin-bottom: var(--s-4); }
  .check-row input { width: 18px; height: 18px; flex-shrink: 0; margin-top: 3px; accent-color: var(--sienna); }
  .check-row label {
    font-family: var(--font-body); font-size: var(--t-base);
    letter-spacing: 0; text-transform: none; font-weight: 400;
    color: var(--ink-2); margin: 0;
  }
  .join-success { display: none; text-align: center; padding: var(--s-6) 0; }
  .join-success.is-visible { display: block; animation: fadeIn 0.25s ease-out; }
  .join-success h2 { font-family: var(--font-head); font-size: var(--t-2xl); font-weight: 700; color: var(--ink); }
  .join-success p { font-size: var(--t-lg); color: var(--ink-2); margin: var(--s-3) 0 var(--s-6); }
  @media (max-width: 900px) {
    .join-grid { grid-template-columns: 1fr; gap: var(--s-6); padding-top: var(--s-6); }
    .join-panel { padding: var(--s-5); }
  }
"""

page = """<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Join the Community &middot; The Mountain Diaries</title>
<link rel="icon" href="favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" type="image/png" href="assets/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Lato:wght@400;700;900&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<script>document.documentElement.classList.replace("no-js","js");</script>
<style>
""" + style.rstrip('\n') + extra_css + """</style>
</head>
<body>

<nav class="site-nav" id="navbar">
  <div class="nav-inner">
    <a class="wordmark" href="index.html#hero"><svg class="wordmark-svg" viewBox="0 0 492.44 202.48" role="img" aria-label="The Mountain Diaries"><path d="M8.12 31.6V5.46H0.0V0.0H22.6V5.46H14.5V31.6Z M232.96 31.6V0.0H239.34V12.8H248.92V0.0H255.27V31.6H248.92V18.25H239.34V31.6Z M467.58 31.6V0.0H488.0V5.38H473.96V12.83H486.21V18.19H473.96V26.22H488.24V31.6Z M4.21 132.03V45.34H35.96L40.62 75.96Q41.0 78.48 41.5 82.14Q42.01 85.79 42.57 89.51Q43.14 93.22 43.52 96.12H44.78Q45.16 93.73 45.66 90.2Q46.16 86.67 46.67 82.96Q47.17 79.24 47.55 76.09L51.96 45.34H82.96V132.03H61.16V107.08Q61.16 100.28 61.41 94.61Q61.66 88.94 61.91 84.85Q62.17 80.75 62.17 78.99H61.03Q60.78 80.5 60.4 82.58Q60.02 84.66 59.71 86.55Q59.39 88.44 59.14 89.7L52.34 132.03H34.82L28.02 89.7Q27.89 88.44 27.52 86.55Q27.14 84.66 26.82 82.58Q26.51 80.5 26.26 78.99H25.12Q25.37 82.14 25.56 86.86Q25.75 91.59 25.88 96.88Q26.0 102.17 26.0 107.08V132.03Z M120.9 133.54Q110.31 133.54 103.45 129.01Q96.58 124.47 93.18 114.58Q89.78 104.69 89.78 88.69Q89.78 72.69 93.18 62.8Q96.58 52.9 103.45 48.37Q110.31 43.83 120.9 43.83Q131.48 43.83 138.41 48.37Q145.34 52.9 148.68 62.8Q152.02 72.69 152.02 88.69Q152.02 104.69 148.68 114.58Q145.34 124.47 138.41 129.01Q131.48 133.54 120.9 133.54ZM120.9 113.76Q123.54 113.76 125.06 112.63Q126.57 111.49 127.32 109.42Q128.08 107.34 128.33 104.38Q128.58 101.41 128.58 97.76V79.62Q128.58 75.96 128.33 73.06Q128.08 70.17 127.32 68.02Q126.57 65.88 125.06 64.75Q123.54 63.61 120.9 63.61Q118.25 63.61 116.74 64.75Q115.23 65.88 114.47 68.02Q113.72 70.17 113.46 73.06Q113.21 75.96 113.21 79.62V97.76Q113.21 101.41 113.46 104.38Q113.72 107.34 114.47 109.42Q115.23 111.49 116.74 112.63Q118.25 113.76 120.9 113.76Z M185.55 133.54Q177.11 133.54 170.94 130.71Q164.76 127.87 161.49 121.2Q158.21 114.52 158.21 103.05V45.34H181.27V104.31Q181.27 108.72 181.9 111.31Q182.53 113.89 185.3 113.89Q188.2 113.89 188.95 111.31Q189.71 108.72 189.71 104.31V45.34H212.77V103.05Q212.77 114.52 209.49 121.2Q206.22 127.87 200.17 130.71Q194.12 133.54 185.55 133.54Z M220.22 132.03V45.34H242.39L250.08 71.43Q250.46 72.81 250.9 74.2Q251.34 75.58 251.78 77.16Q252.22 78.73 252.6 80.5H253.23Q253.23 78.23 253.23 75.96Q253.23 73.69 253.23 71.43V45.34H275.41V132.03H253.1L245.54 105.82Q244.79 103.3 244.16 100.66Q243.53 98.01 242.9 95.49H242.27Q242.27 98.01 242.27 100.66Q242.27 103.3 242.27 105.82V132.03Z M296.97 132.03V65.25H280.34V45.34H336.41V65.25H320.03V132.03Z M336.3 132.03 353.56 45.34H385.81L403.08 132.03H378.76L376.99 119.31H361.62L359.98 132.03ZM364.27 100.15H374.47L371.83 80.75Q371.7 79.62 371.51 77.73Q371.32 75.84 371.07 73.51Q370.82 71.17 370.51 68.84Q370.19 66.51 369.94 64.62H368.8Q368.55 67.02 368.24 69.98Q367.92 72.94 367.61 75.77Q367.29 78.61 366.91 80.75Z M406.12 132.03V45.34H429.17V132.03Z M437.25 132.03V45.34H459.43L467.12 71.43Q467.49 72.81 467.94 74.2Q468.38 75.58 468.82 77.16Q469.26 78.73 469.64 80.5H470.27Q470.27 78.23 470.27 75.96Q470.27 73.69 470.27 71.43V45.34H492.44V132.03H470.14L462.58 105.82Q461.82 103.3 461.19 100.66Q460.56 98.01 459.93 95.49H459.3Q459.3 98.01 459.3 100.66Q459.3 103.3 459.3 105.82V132.03Z M2.71 201.54V147.91H19.06Q25.47 147.91 29.15 150.72Q32.82 153.54 34.37 159.4Q35.92 165.27 35.92 174.55Q35.92 183.74 34.31 189.73Q32.7 195.72 28.97 198.63Q25.23 201.54 18.78 201.54ZM14.6 191.28H17.89Q19.56 191.28 20.71 190.69Q21.85 190.09 22.54 188.69Q23.22 187.29 23.53 184.93Q23.84 182.57 23.84 179.09V171.39Q23.84 167.87 23.53 165.37Q23.22 162.87 22.55 161.27Q21.89 159.68 20.72 158.93Q19.56 158.17 17.89 158.17H14.6Z M86.53 201.54V147.91H98.42V201.54Z M146.53 201.54 157.89 147.91H174.12L185.52 201.54H173.03L171.19 191.6H160.42L158.66 201.54ZM161.88 181.66H169.77L167.35 167.34Q167.27 166.74 167.14 165.72Q167.0 164.69 166.83 163.42Q166.65 162.16 166.48 160.89Q166.3 159.63 166.14 158.56H165.55Q165.39 159.87 165.18 161.51Q164.97 163.14 164.75 164.7Q164.54 166.26 164.34 167.34Z M233.66 201.54V147.91H251.62Q257.56 147.91 260.84 150.04Q264.12 152.17 265.45 155.79Q266.78 159.41 266.78 163.87Q266.78 168.55 265.66 172.36Q264.53 176.17 261.7 178.51L268.59 201.54H256.27L251.14 182.53H245.55V201.54ZM245.55 172.82H250.0Q252.8 172.82 253.83 170.62Q254.86 168.41 254.86 165.03Q254.86 162.74 254.41 161.14Q253.96 159.55 252.89 158.69Q251.82 157.83 249.79 157.83H245.55Z M317.09 201.54V147.91H328.98V201.54Z M380.63 201.54V147.91H410.23V158.17H392.52V169.15H407.53V179.45H392.52V191.28H410.59V201.54Z M475.02 202.48Q471.62 202.48 468.7 201.77Q465.78 201.07 463.58 199.26Q461.39 197.44 460.15 194.22Q458.91 191.0 458.91 185.91Q458.91 185.65 458.91 185.15Q458.91 184.66 458.95 184.35H470.32Q470.32 184.74 470.32 185.15Q470.32 185.56 470.32 185.95Q470.32 188.48 470.82 189.86Q471.31 191.25 472.27 191.8Q473.24 192.35 474.66 192.35Q475.52 192.35 476.18 192.14Q476.84 191.93 477.36 191.47Q477.89 191.02 478.23 190.35Q478.56 189.69 478.71 188.78Q478.86 187.87 478.86 186.74Q478.86 184.94 478.05 183.69Q477.23 182.45 475.86 181.54Q474.48 180.64 472.77 179.85Q471.06 179.05 469.22 178.18Q467.37 177.3 465.66 176.11Q463.96 174.92 462.58 173.18Q461.2 171.44 460.39 168.99Q459.57 166.55 459.57 163.12Q459.57 158.72 460.83 155.65Q462.08 152.57 464.28 150.65Q466.48 148.73 469.26 147.83Q472.04 146.93 475.1 146.93Q478.3 146.93 481.01 147.71Q483.73 148.49 485.73 150.21Q487.73 151.93 488.85 154.78Q489.97 157.63 489.97 161.77V163.74H478.76V162.67Q478.76 160.88 478.47 159.66Q478.17 158.44 477.43 157.8Q476.68 157.15 475.21 157.15Q474.07 157.15 473.25 157.65Q472.43 158.14 472.02 159.15Q471.62 160.15 471.62 161.72Q471.62 163.65 472.43 164.98Q473.25 166.31 474.64 167.23Q476.04 168.16 477.75 168.95Q479.46 169.75 481.28 170.61Q483.11 171.46 484.81 172.63Q486.52 173.8 487.92 175.5Q489.32 177.2 490.13 179.62Q490.95 182.04 490.95 185.43Q490.95 191.24 489.01 195.02Q487.08 198.79 483.52 200.63Q479.96 202.48 475.02 202.48Z"/></svg></a>
    <button class="nav-toggle" type="button" id="nav-toggle"
            aria-expanded="false" aria-controls="nav-menu" aria-label="Open menu">
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
    </button>
    <ul class="nav-menu" id="nav-menu">
      <li><a href="explore.html">Explore</a></li>
      <li><a href="index.html#community" data-spy="community">Community</a></li>
      <li><a href="know.html">Know the Mountain</a></li>
      <!-- re-target to the About Us section once it is written; #story is a stand in -->
      <li><a href="index.html#story" data-spy="story">About Us</a></li>
    </ul>
  </div>
</nav>

<main class="join-main">
  <div class="join-hero">
    <div class="photo-slot"
         style="--photo:url('assets/images/join-hero.jpg');--pos:center 68%"></div>
  </div>

  <div class="wrap">
    <div class="join-grid">
      <div>
        <div class="section-head" style="margin-bottom:var(--s-4)">
          <p class="section-kicker">Walk with people</p>
          <h1 class="section-title">Join the Community</h1>
        </div>
        <p class="section-lede">We run local hikes across the UAE most months, and put together small expedition groups for the bigger routes.</p>
        <p class="section-lede">Join the list and you will hear about dates first, meet the people going, and read the stories that come back.</p>
        <ul class="join-points">
          <li>Local UAE hikes, from easy wadi walks to long days in Ras Al Khaimah</li>
          <li>Expedition groups for Nepal, the Alps, Patagonia and Kilimanjaro</li>
          <li>Shared stories from people who have walked the route before you</li>
        </ul>
      </div>

      <div class="join-panel">
        <div class="join-success" id="join-success">
          <div class="inquiry-success-icon" style="margin:0 auto var(--s-4)">&#10022;</div>
          <h2>You are in. One more step</h2>
          <p>Come and say hello. The group is where the dates, the lifts and the last-minute plans actually happen.</p>
          <a class="btn btn-primary" id="whatsapp-link" href="#" target="_blank" rel="noopener">
            Join our WhatsApp Community <span aria-hidden="true">&rarr;</span>
          </a>
        </div>

        <form id="join-form">
          <p class="inquiry-form-label">Your details</p>
          <p class="inquiry-form-hint">We keep your information private and never share it.</p>

          <div class="field">
            <label for="join-name">Full name</label>
            <input type="text" id="join-name" name="name" placeholder="Your full name" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="join-email">Email address</label>
            <input type="email" id="join-email" name="email" placeholder="you@email.com" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="join-mobile">Mobile number</label>
            <input type="tel" id="join-mobile" name="mobile" placeholder="+971 50 000 0000"
                   autocomplete="tel" required>
            <p class="form-note">Include your country code, for example +971.</p>
          </div>
          <div class="field">
            <label for="join-experience">Your experience level</label>
            <select id="join-experience" name="experience" required>
              <option value="">Select your background</option>
              <option>Beginner, new to multi-day trekking</option>
              <option>Intermediate, several treks completed</option>
              <option>Experienced, high-altitude background</option>
              <option>Expert, technical mountaineering</option>
            </select>
          </div>

          <div class="check-row">
            <input type="checkbox" id="join-local" name="local_hikes" value="yes">
            <label for="join-local">I am interested in local UAE hikes</label>
          </div>

          <div class="hp-field" aria-hidden="true">
            <label for="join-hp">Leave this field empty</label>
            <input type="text" id="join-hp" name="_gotcha" tabindex="-1" autocomplete="off">
          </div>

          <p class="form-error" id="join-error" role="alert"></p>
          <button class="btn btn-primary" type="submit" style="width:100%">
            Join the community <span aria-hidden="true">&rarr;</span>
          </button>
          <p class="form-note">By joining you agree to be contacted about hikes and expeditions.</p>
        </form>
      </div>
    </div>
  </div>
</main>

<footer class="site-footer">
  <div class="footer-ridge" aria-hidden="true"></div>
  <div class="footer-veil" aria-hidden="true"></div>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="wordmark wordmark-inverse" href="index.html#hero"><svg class="wordmark-svg" viewBox="0 0 492.44 202.48" role="img" aria-label="The Mountain Diaries"><path d="M8.12 31.6V5.46H0.0V0.0H22.6V5.46H14.5V31.6Z M232.96 31.6V0.0H239.34V12.8H248.92V0.0H255.27V31.6H248.92V18.25H239.34V31.6Z M467.58 31.6V0.0H488.0V5.38H473.96V12.83H486.21V18.19H473.96V26.22H488.24V31.6Z M4.21 132.03V45.34H35.96L40.62 75.96Q41.0 78.48 41.5 82.14Q42.01 85.79 42.57 89.51Q43.14 93.22 43.52 96.12H44.78Q45.16 93.73 45.66 90.2Q46.16 86.67 46.67 82.96Q47.17 79.24 47.55 76.09L51.96 45.34H82.96V132.03H61.16V107.08Q61.16 100.28 61.41 94.61Q61.66 88.94 61.91 84.85Q62.17 80.75 62.17 78.99H61.03Q60.78 80.5 60.4 82.58Q60.02 84.66 59.71 86.55Q59.39 88.44 59.14 89.7L52.34 132.03H34.82L28.02 89.7Q27.89 88.44 27.52 86.55Q27.14 84.66 26.82 82.58Q26.51 80.5 26.26 78.99H25.12Q25.37 82.14 25.56 86.86Q25.75 91.59 25.88 96.88Q26.0 102.17 26.0 107.08V132.03Z M120.9 133.54Q110.31 133.54 103.45 129.01Q96.58 124.47 93.18 114.58Q89.78 104.69 89.78 88.69Q89.78 72.69 93.18 62.8Q96.58 52.9 103.45 48.37Q110.31 43.83 120.9 43.83Q131.48 43.83 138.41 48.37Q145.34 52.9 148.68 62.8Q152.02 72.69 152.02 88.69Q152.02 104.69 148.68 114.58Q145.34 124.47 138.41 129.01Q131.48 133.54 120.9 133.54ZM120.9 113.76Q123.54 113.76 125.06 112.63Q126.57 111.49 127.32 109.42Q128.08 107.34 128.33 104.38Q128.58 101.41 128.58 97.76V79.62Q128.58 75.96 128.33 73.06Q128.08 70.17 127.32 68.02Q126.57 65.88 125.06 64.75Q123.54 63.61 120.9 63.61Q118.25 63.61 116.74 64.75Q115.23 65.88 114.47 68.02Q113.72 70.17 113.46 73.06Q113.21 75.96 113.21 79.62V97.76Q113.21 101.41 113.46 104.38Q113.72 107.34 114.47 109.42Q115.23 111.49 116.74 112.63Q118.25 113.76 120.9 113.76Z M185.55 133.54Q177.11 133.54 170.94 130.71Q164.76 127.87 161.49 121.2Q158.21 114.52 158.21 103.05V45.34H181.27V104.31Q181.27 108.72 181.9 111.31Q182.53 113.89 185.3 113.89Q188.2 113.89 188.95 111.31Q189.71 108.72 189.71 104.31V45.34H212.77V103.05Q212.77 114.52 209.49 121.2Q206.22 127.87 200.17 130.71Q194.12 133.54 185.55 133.54Z M220.22 132.03V45.34H242.39L250.08 71.43Q250.46 72.81 250.9 74.2Q251.34 75.58 251.78 77.16Q252.22 78.73 252.6 80.5H253.23Q253.23 78.23 253.23 75.96Q253.23 73.69 253.23 71.43V45.34H275.41V132.03H253.1L245.54 105.82Q244.79 103.3 244.16 100.66Q243.53 98.01 242.9 95.49H242.27Q242.27 98.01 242.27 100.66Q242.27 103.3 242.27 105.82V132.03Z M296.97 132.03V65.25H280.34V45.34H336.41V65.25H320.03V132.03Z M336.3 132.03 353.56 45.34H385.81L403.08 132.03H378.76L376.99 119.31H361.62L359.98 132.03ZM364.27 100.15H374.47L371.83 80.75Q371.7 79.62 371.51 77.73Q371.32 75.84 371.07 73.51Q370.82 71.17 370.51 68.84Q370.19 66.51 369.94 64.62H368.8Q368.55 67.02 368.24 69.98Q367.92 72.94 367.61 75.77Q367.29 78.61 366.91 80.75Z M406.12 132.03V45.34H429.17V132.03Z M437.25 132.03V45.34H459.43L467.12 71.43Q467.49 72.81 467.94 74.2Q468.38 75.58 468.82 77.16Q469.26 78.73 469.64 80.5H470.27Q470.27 78.23 470.27 75.96Q470.27 73.69 470.27 71.43V45.34H492.44V132.03H470.14L462.58 105.82Q461.82 103.3 461.19 100.66Q460.56 98.01 459.93 95.49H459.3Q459.3 98.01 459.3 100.66Q459.3 103.3 459.3 105.82V132.03Z M2.71 201.54V147.91H19.06Q25.47 147.91 29.15 150.72Q32.82 153.54 34.37 159.4Q35.92 165.27 35.92 174.55Q35.92 183.74 34.31 189.73Q32.7 195.72 28.97 198.63Q25.23 201.54 18.78 201.54ZM14.6 191.28H17.89Q19.56 191.28 20.71 190.69Q21.85 190.09 22.54 188.69Q23.22 187.29 23.53 184.93Q23.84 182.57 23.84 179.09V171.39Q23.84 167.87 23.53 165.37Q23.22 162.87 22.55 161.27Q21.89 159.68 20.72 158.93Q19.56 158.17 17.89 158.17H14.6Z M86.53 201.54V147.91H98.42V201.54Z M146.53 201.54 157.89 147.91H174.12L185.52 201.54H173.03L171.19 191.6H160.42L158.66 201.54ZM161.88 181.66H169.77L167.35 167.34Q167.27 166.74 167.14 165.72Q167.0 164.69 166.83 163.42Q166.65 162.16 166.48 160.89Q166.3 159.63 166.14 158.56H165.55Q165.39 159.87 165.18 161.51Q164.97 163.14 164.75 164.7Q164.54 166.26 164.34 167.34Z M233.66 201.54V147.91H251.62Q257.56 147.91 260.84 150.04Q264.12 152.17 265.45 155.79Q266.78 159.41 266.78 163.87Q266.78 168.55 265.66 172.36Q264.53 176.17 261.7 178.51L268.59 201.54H256.27L251.14 182.53H245.55V201.54ZM245.55 172.82H250.0Q252.8 172.82 253.83 170.62Q254.86 168.41 254.86 165.03Q254.86 162.74 254.41 161.14Q253.96 159.55 252.89 158.69Q251.82 157.83 249.79 157.83H245.55Z M317.09 201.54V147.91H328.98V201.54Z M380.63 201.54V147.91H410.23V158.17H392.52V169.15H407.53V179.45H392.52V191.28H410.59V201.54Z M475.02 202.48Q471.62 202.48 468.7 201.77Q465.78 201.07 463.58 199.26Q461.39 197.44 460.15 194.22Q458.91 191.0 458.91 185.91Q458.91 185.65 458.91 185.15Q458.91 184.66 458.95 184.35H470.32Q470.32 184.74 470.32 185.15Q470.32 185.56 470.32 185.95Q470.32 188.48 470.82 189.86Q471.31 191.25 472.27 191.8Q473.24 192.35 474.66 192.35Q475.52 192.35 476.18 192.14Q476.84 191.93 477.36 191.47Q477.89 191.02 478.23 190.35Q478.56 189.69 478.71 188.78Q478.86 187.87 478.86 186.74Q478.86 184.94 478.05 183.69Q477.23 182.45 475.86 181.54Q474.48 180.64 472.77 179.85Q471.06 179.05 469.22 178.18Q467.37 177.3 465.66 176.11Q463.96 174.92 462.58 173.18Q461.2 171.44 460.39 168.99Q459.57 166.55 459.57 163.12Q459.57 158.72 460.83 155.65Q462.08 152.57 464.28 150.65Q466.48 148.73 469.26 147.83Q472.04 146.93 475.1 146.93Q478.3 146.93 481.01 147.71Q483.73 148.49 485.73 150.21Q487.73 151.93 488.85 154.78Q489.97 157.63 489.97 161.77V163.74H478.76V162.67Q478.76 160.88 478.47 159.66Q478.17 158.44 477.43 157.8Q476.68 157.15 475.21 157.15Q474.07 157.15 473.25 157.65Q472.43 158.14 472.02 159.15Q471.62 160.15 471.62 161.72Q471.62 163.65 472.43 164.98Q473.25 166.31 474.64 167.23Q476.04 168.16 477.75 168.95Q479.46 169.75 481.28 170.61Q483.11 171.46 484.81 172.63Q486.52 173.8 487.92 175.5Q489.32 177.2 490.13 179.62Q490.95 182.04 490.95 185.43Q490.95 191.24 489.01 195.02Q487.08 198.79 483.52 200.63Q479.96 202.48 475.02 202.48Z"/></svg></a>
        <p class="footer-mission">A community that answers the mountains and treks them together.</p>
      </div>
      <div>
        <p class="footer-col-title">Explore</p>
        <ul class="footer-links">
          <li><a href="explore.html">Expeditions &amp; Trekking</a></li>
          <li><a href="index.html#community">Community</a></li>
          <li><a href="know.html">Know the Mountain</a></li>
          <li><a href="know.html#news">Mountain news</a></li>
          <!-- re-target to the About Us section once it is written; #story is a stand in -->
          <li><a href="index.html#story">About Us</a></li>
        </ul>
      </div>
      <div>
        <p class="footer-col-title">Community</p>
        <ul class="footer-links">
          <li><a href="join.html">Join the community</a></li>
          <li><a href="index.html#community">Share your story</a></li>
        </ul>
      </div>
      <div>
        <p class="footer-col-title">Let&rsquo;s connect</p>
        <div class="footer-primary">
        <a class="fcircle fcircle-solid" href="mailto:hello@themountaindiaries.com" aria-label="Email us"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 6.5h18v11H3z"/><path d="M3 7l9 6.5L21 7"/></svg></a>
        <a class="fcircle fcircle-solid" href="https://chat.whatsapp.com/LuY03kcNWuf0dvSUTZ9Vq2" aria-label="Join our WhatsApp group" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3.2a8.8 8.8 0 0 0-7.6 13.2L3.2 20.8l4.5-1.15A8.8 8.8 0 1 0 12 3.2Z"/><path d="M9.1 8.1c.3-.05.5.05.7.45l.6 1.3c.1.25.06.45-.1.65l-.4.5c-.15.2-.15.35 0 .6a6.3 6.3 0 0 0 2.6 2.35c.25.1.4.05.55-.15l.5-.6c.2-.2.4-.25.65-.15l1.35.6c.35.15.45.35.4.7-.15.9-.95 1.5-1.95 1.5-2.9 0-6.05-3.2-6.05-6.1 0-1 .6-1.6 1.15-1.65Z"/></svg></a>
        </div>
        <div class="footer-social">
        <a class="fcircle fcircle-outline" href="#" aria-label="The Mountain Diaries on Facebook"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path class="glyph-fill" d="M10.08 19.5V11.16H8.55V8.73H10.08V7.86Q10.08 6.74 10.46 5.99Q10.84 5.24 11.59 4.87Q12.35 4.5 13.47 4.5Q13.77 4.5 14.14 4.55Q14.51 4.59 14.86 4.67Q15.21 4.75 15.45 4.84V6.93H14.47Q13.9 6.93 13.66 7.18Q13.43 7.42 13.43 7.94V8.73H15.45V11.16H13.43V19.5Z"/></svg></a>
        <a class="fcircle fcircle-outline" href="#" aria-label="The Mountain Diaries on Instagram"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4.1"/><circle cx="17.2" cy="6.8" r="1.15"/></svg></a>
        <a class="fcircle fcircle-outline" href="#" aria-label="The Mountain Diaries on TikTok"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M13.8 3.2v10.6a3.4 3.4 0 1 1-2.6-3.3"/><path d="M13.8 5.4c.7 1.7 2.2 2.8 4.2 3"/></svg></a>
        <a class="fcircle fcircle-outline" href="#" aria-label="The Mountain Diaries on LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3.5" y="3.5" width="17" height="17" rx="3.4"/><path class="glyph-fill" d="M5.96 8.42V6.5H8.45V8.42ZM5.96 17.5V9.49H8.45V17.5Z M10.34 17.5V9.49H12.39L12.57 10.64H12.67Q12.97 10.22 13.37 9.92Q13.77 9.62 14.27 9.47Q14.77 9.31 15.33 9.31Q16.2 9.31 16.8 9.63Q17.4 9.95 17.72 10.59Q18.04 11.23 18.04 12.21V17.5H15.54V12.57Q15.54 12.23 15.46 11.99Q15.38 11.75 15.22 11.59Q15.07 11.43 14.84 11.35Q14.62 11.27 14.32 11.27Q13.89 11.27 13.55 11.47Q13.21 11.68 13.02 12.02Q12.83 12.37 12.83 12.82V17.5Z"/></svg></a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 The Mountain Diaries. We never share your details.</span>
      <!-- re-target once the policy pages exist -->
      <span><a href="#">Privacy</a> &middot; <a href="#">Terms</a></span>
    </div>
  </div>
</footer>

<script>
// ─── BACKEND ──────────────────────────────────────────────────────────────
// All three forms post to one Google Apps Script endpoint, which appends a
// row to the sheet and emails a notification.
//
// The content type MUST stay text/plain. Apps Script cannot answer a CORS
// preflight, and application/json would trigger one, so the request has to
// stay a "simple" request. The body is still JSON.
// ═══ NAV ═══ same behaviour as index: scrolled shadow plus the mobile menu.
(function () {
  const nav = document.getElementById('navbar');
  const syncScrolled = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
  window.addEventListener('scroll', syncScrolled, { passive: true });
  syncScrolled();

  const toggle = document.getElementById('nav-toggle');
  const menu = document.getElementById('nav-menu');
  const setOpen = (open) => {
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  toggle.addEventListener('click', () => setOpen(!menu.classList.contains('is-open')));
  menu.addEventListener('click', (e) => { if (e.target.tagName === 'A') setOpen(false); });
  window.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
  window.addEventListener('resize', () => { if (window.innerWidth > 860) setOpen(false); });
})();

const FORM_ENDPOINT = 'https://script.google.com/macros/s/AKfycbwiFM4_UqnszYUvT4ygUIEr6vm9_3hWwiReikL9OcPfKXLEUALDvtMSnxGnRBjxOHMR/exec';
const FORM_ERROR = 'Something went wrong. Please try again, or email hello@themountaindiaries.com';

async function postForm(payload) {
  const res = await fetch(FORM_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!data || data.ok !== true) throw new Error((data && data.error) || 'rejected');
  return data;
}

// The real group invite, supplied with the footer brief. The placeholder
// branch below is kept: it is what renders if this is ever blanked again.
const WHATSAPP_INVITE_URL = 'https://chat.whatsapp.com/LuY03kcNWuf0dvSUTZ9Vq2';
const isPlaceholderId = (v) => /^[A-Z0-9_]+$/.test(v);

document.getElementById('join-form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const err = document.getElementById('join-error');
  const btn = this.querySelector('button[type="submit"]');

  err.textContent = '';
  const label = btn.innerHTML;
  btn.disabled = true;
  btn.textContent = 'Sending';

  try {
    await postForm({
      formType: 'join',
      name:       document.getElementById('join-name').value.trim(),
      email:      document.getElementById('join-email').value.trim(),
      mobile:     document.getElementById('join-mobile').value.trim(),
      experience: document.getElementById('join-experience').value,
      localHikes: document.getElementById('join-local').checked,
      _gotcha:    document.getElementById('join-hp').value
    });

    const wa = document.getElementById('whatsapp-link');
    if (isPlaceholderId(WHATSAPP_INVITE_URL)) {
      wa.removeAttribute('href');
      wa.setAttribute('aria-disabled', 'true');
      wa.textContent = 'WhatsApp invite coming shortly';
    } else {
      wa.href = WHATSAPP_INVITE_URL;
    }
    this.style.display = 'none';
    document.getElementById('join-success').classList.add('is-visible');
  } catch (_) {
    err.textContent = FORM_ERROR;
    btn.disabled = false;
    btn.innerHTML = label;
  }
});
</script>
</body>
</html>
"""

io.open(OUT, 'w', encoding='utf-8').write(page)
print('join.html written:', len(page.split('\n')), 'lines')

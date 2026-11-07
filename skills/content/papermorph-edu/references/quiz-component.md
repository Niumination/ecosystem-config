# Quiz Component — Reusable HTML/JS Pattern

Self-contained quiz component for Edu Content chapters. No external dependencies (no SurveyJS, no CDN). CSS + vanilla JS, embeddable in any chapter HTML.

## Template

```html
<!-- Insert before </div> closing the beat container, after all beats -->
<div class="quiz-section">
  <h3>Quiz — [Chapter Title]</h3>
  <div id="quiz-container"></div>
  <button class="quiz-btn" onclick="checkQuiz()">Periksa Jawaban</button>
  <div id="quiz-result" class="quiz-result" style="display:none;"></div>
</div>
```

## CSS (add to <style> in <head>)

```css
.quiz-section { max-width: 760px; margin: 2rem auto; padding: 1.5rem; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(31,42,68,0.08); }
.quiz-section h3 { color: #1F2A44; margin-bottom: 1rem; }
.quiz-q { margin-bottom: 1.5rem; padding: 1rem; background: #F5F1E8; border-radius: 8px; }
.quiz-q p { font-weight: 600; margin-bottom: 0.8rem; }
.quiz-opt { display: block; margin: 0.4rem 0; padding: 0.6rem 1rem; background: #fff; border: 1px solid #E8DCC8; border-radius: 6px; cursor: pointer; transition: background 0.2s; }
.quiz-opt:hover { background: #E8DCC8; }
.quiz-opt.correct { background: #d4edda; border-color: #28a745; }
.quiz-opt.wrong { background: #f8d7da; border-color: #dc3545; }
.quiz-result { margin-top: 1rem; padding: 0.8rem; border-radius: 6px; font-weight: 600; }
.quiz-result.pass { background: #d4edda; color: #155724; }
.quiz-result.fail { background: #f8d7da; color: #721c24; }
.quiz-btn { margin-top: 1rem; padding: 0.6rem 1.5rem; background: #C6A75E; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; }
.quiz-btn:hover { background: #b0924e; }
```

## JS (add before </body>)

```javascript
const quizData = [
  { q: "Question text?", opts: ["Option A", "Option B", "Option C", "Option D"], correct: 1 },
  // ... more questions
];

function renderQuiz() {
  const container = document.getElementById('quiz-container');
  let html = '';
  quizData.forEach((item, i) => {
    html += `<div class="quiz-q"><p>${i+1}. ${item.q}</p>`;
    item.opts.forEach((opt, j) => {
      html += `<label class="quiz-opt"><input type="radio" name="q${i}" value="${j}"> ${opt}</label>`;
    });
    html += '</div>';
  });
  container.innerHTML = html;
}

function checkQuiz() {
  let score = 0;
  quizData.forEach((item, i) => {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    const opts = document.querySelectorAll(`input[name="q${i}"]`);
    opts.forEach((opt, j) => {
      const label = opt.parentElement;
      if (j === item.correct) label.classList.add('correct');
      else if (opt.checked) label.classList.add('wrong');
    });
    if (selected && parseInt(selected.value) === item.correct) score++;
  });
  const result = document.getElementById('quiz-result');
  const pct = Math.round(score / quizData.length * 100);
  result.style.display = 'block';
  if (pct >= 70) {
    result.className = 'quiz-result pass';
    result.textContent = `✅ Skor: ${score}/${quizData.length} (${pct}%) — Lulus!`;
  } else {
    result.className = 'quiz-result fail';
    result.textContent = `❌ Skor: ${score}/${quizData.length} (${pct}%) — Coba lagi`;
  }
}

renderQuiz();
```

## Rules

1. **Minimum 3 soal per chapter** — threshold lulus 70%
2. **Bahasa Indonesia** — semua pertanyaan dan opsi dalam Bahasa Indonesia
3. **Soal berbasis konten chapter** — setiap soal harus merujuk ke materi yang diajarkan di chapter tersebut
4. **Self-contained** — tidak memerlukan CDN, SurveyJS, atau library eksternal
5. **Aksesibel** — radio buttons dengan label, feedback visual (hijau/merah)
6. **Quiz ditempatkan setelah semua beats**, sebelum footer
7. **Satu quiz per chapter** — jangan gabungkan quiz antar chapter